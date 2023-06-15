const fs = require('fs');
const _ = require('lodash');
const assert = require('assert');
const cliProgress = require('cli-progress');

const IN = process.argv[2];
const OUT = process.argv[3];
const DIR = IN;

let sample = 10;

let faulty = 0;
let preview = 1;

const samples = [];

export function getLines(path: string): string[] {
    let text = fs.readFileSync(path, 'utf-8');
    return text.split(/\r?\n/);
}

function mapDiff(diff) {
    const map = ['files', 'lines', 'hits', 'misses', 'partials', 'coverage'];
    const res = diff.reduce((acc, cur, i) => ({...acc, [map[i]]: cur}), {});
    res.coverage = Number(res.coverage);
    delete res.undefined;
    return res;
}

function mapTotals(totals) {
    const res = objectRemap(totals, {
        c: 'coverage',
        f: 'files',
        n: 'lines',
        h: 'hits',
        m: 'missed',
        p: 'partials'
    });
    res["coverage"] = Number(res["coverage"]);
    return res;
}

function objectRemap(obj, map) {
    return Object.keys(map).reduce((acc, cur) => ({...acc, [map[cur]]: obj[cur]}), {})
}

function objectPrefix(obj, prefix) {
    return Object.entries(obj).reduce((previousValue, currentValue) => ({... previousValue, [prefix + currentValue[0]]: currentValue[1]}), {})
}

function calcDiff(before, after) {
    return Object.keys(after).reduce((acc, val) => ({...acc, [val]: after[val] - before[val]}), {})
}

function getCoverageData(row) {
    return {
        patch: row.coverage_diff,
        base: row.coverage_compared_to || row.coverge_base,
        head: row.coverage_head,
        base_updateStamp: row.coverage_compared_to ? row.compared_to_updatestamp: row.base_updatestamp,
        head_updateStamp: row.head_updatestamp
    }
}

function flattenRow(row) {
    const coverage = getCoverageData(row);

    let patch = JSON.parse(coverage.patch);
    assert(patch);
    patch = objectPrefix(mapDiff(patch), 'patch_coverage_');

    const compared_to = coverage.base;
    assert(compared_to && row.coverage_head);
    const before = mapTotals(JSON.parse(compared_to));
    const coverageBefore = objectPrefix(before, 'coverage_before_');

    const after = mapTotals(JSON.parse(coverage.head));
    const coverageAfter = objectPrefix(after, 'coverage_after_');

    const timeToMergeInHours = (new Date(row["merged_at"]).getTime() - new Date(row["created_at"]).getTime()) / 1000 / 3600;
    assert(timeToMergeInHours > 0);
    // const coverageGoesUp = coverageAfter["coverage_after_coverage"] > coverageBefore["coverage_before_coverage"];
    // const coverageDoesntChange = coverageAfter["coverage_after_coverage"] === coverageBefore["coverage_before_coverage"];

    const diff = objectPrefix(calcDiff(before, after), 'diff_coverage_');

    const commitsInPr = row.commit_authors_in_pr.length;
    const authors = new Set(row.commit_authors_in_pr);
    const authorsInPr = authors.size;

    const commitsInProject = row.commit_authors_in_project.length;
    const contributors = new Set(row.commit_authors_in_project);
    const contributorsInProject = contributors.size;

    // const commentAuthors = row.issue_comments_authors.concat(row.pr_review_comment_authors);
    // const numberOfComments = commentAuthors.length;
    // const reviewers = new Set(commentAuthors.filter(a => !authors.has(a)));
    // const numberOfReviewers = reviewers.size;

    const res = {
        project: row.repo,
        pull_id: row.pull_id,
        created_at: row.created_at,
        merged_at: row.merged_at,
        ...patch,
        ...coverageBefore,
        ...coverageAfter,
        ...diff,
        timeToMergeInHours,
        // coverageGoesUp,
        // coverageDoesntChange,
        // sizeOfProjectInBytes,
        commitsInPr,
        authorsInPr,
        commitsInProject,
        contributorsInProject,
        // numberOfComments,
        // numberOfReviewers,
        intraBranch: row.intra_branch,
        issueComments: row.issue_comments_authors,
        prComments: row.pr_review_comment_authors,
        authors: Array.from(new Set(row.commit_authors_in_pr)),
        baseUpdateStamp: coverage.base_updateStamp,
        headUpdateStamp: coverage.head_updateStamp,
    };

    if (sample > 0 && Math.random() < 0.01) {
        samples.push({original: row, transformed: res});
        sample--;
        if (sample == 0) {
            fs.writeFileSync('samples.json', JSON.stringify(samples, null, 4));
        }
    }

    if (preview > 0) {
        console.log(row);
        console.log(res);
        preview--;
    }

    // console.log(`https://github.com/${row.username}/${row.repo_name}/pull/${row.pull_id}`)
    return res;
}

function* generator(lines) {
    for (let line of lines) {
        if (line.length <= 0) continue;
        const json = JSON.parse(line);
        try {
            yield flattenRow(json);
        } catch (e) {
            faulty++;
            if (e.name !== 'AssertionError') {
                console.error(e);
                console.error(line);
                process.exit(1);
            }
        }
    }
}

function runTransform(file) {
    const files = fs.readdirSync(DIR);
    const bars = new cliProgress.MultiBar({hideCursor: true}, cliProgress.Presets.shades_classic);
    const mainBar = bars.create(files.length, 0);
    const innerBar = bars.create(0, 0);
    let writeStream = {write(chunk: any) {}, close() {}, end() {}};
    if (file) {
        const outputFile = file;
        if (fs.existsSync(outputFile)) fs.unlinkSync(outputFile);
        writeStream = fs.createWriteStream(outputFile);
    }
    // writeStream.write('[');
    for (let f of files) {
        const finalFile = f === files[files.length - 1];
        const lines = getLines(DIR + f);
        innerBar.start(lines.length, 0);
        const gen = generator(lines);
        let v = gen.next();
        while (!v.done) {
            writeStream.write(JSON.stringify(v.value));
            v = gen.next();
            if (!v.done || !finalFile) {
                writeStream.write('\n');
            }
            innerBar.increment();
            bars.update();
        }
        mainBar.increment();
        bars.update();
    }
    // writeStream.write(']');
    writeStream.end();
    bars.stop();

    console.info(`Faulty: ${faulty}`)
}

if (require.main === module) {
    runTransform(OUT);
}

