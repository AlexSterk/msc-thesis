const {getLines} = require("./json-to-csv");

const TEMP = 'data/rq1_export1/part_000000000000.json';
const DIR = 'data/rq1_export1/'

const parseFile1 = getLines(TEMP);
const x = parseFile1.map(x => [].concat(x.pr_labels, x.project_topics)).filter(x => x.length > 0);
console.log(x);
