matrix_order_3 = ["Every day", "A few times a week", "A few times a month", "A few times a year",
                  "Less than once a year", "Never"][::-1]
DEMOGRAPHIC = {
    "Q8": {
        "title": "Years developing software",
        "kind": "hist",
        "rwidth": 0.8,
        "ylabel": "Number of respondents",
        "xlabel": "Years"
    },
    "Q41": {
        "title": "Years active on open-source development platforms",
        "kind": "hist",
        "rwidth": 0.8,
        "ylabel": "Number of respondents",
        "xlabel": "Years"
    },
    ("Q12_1", "Q12_2", "Q12_3"): {
        "title": "How often do you...",
        "kind": "barh",
        "order": matrix_order_3,
        "columns": [
            "Contribute to my own projects?",
            "Contribute to someone else's projects?",
            "Review other people's contributions?"
        ],
        "xlabel": "Number of respondents",
    },
    "Dev/Maintain choice": {
        "title": "Do you consider yourself more of a contributor or a project maintainer?",
        "kind": "bar",
        "rot": 0,
        "ylabel": "Number of respondents",
    },
    "Q15": {
        "kind": "bar",
        "rot": 0,
        "title": "Do you work in software development?",
        "ylabel": "Number of respondents",
    },
    ("Q17_1", "Q17_2", "Q17_3"): {
        "kind": "barh",
        "title": "How long have you been performing...",
        "columns": ["Automated testings tasks?", "Manual testing tasks?", "Code review of other people's code?"],
        "order": ["<1 year", "1-3 years", "3-5 years", "5-10 years", "10-20 years", "20+ years"],
        "figsize": (10, 5),
        "xlabel": "Number of respondents",
    }
}
matrix_order_1 = ["For each commit", "Every few commits", "For each pull request", "Every few pull requests", "Rarely",
                  "Never"][::-1]
matrix_order_2 = ["Strongly disagree",
                  "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly agree"][::-1]
matrix_order_4 = ["Not at all important", "Slightly important", "Moderately important", "Very important",
                  "Extremely important"][::-1]
QUANTITATIVE = {
    "Q18_1": {
        "kind": "barh",
        "order": matrix_order_4,
        "title": "How important do you find automated software testing?",
        "loc": "best"
    },
    "Q20_1": {
        "kind": "barh",
        "order": matrix_order_1,
        "title": "How often do you use coverage tools outside of Github?"
    },
    "Q43_1": {
        "kind": "barh",
        "order": matrix_order_1,
        "title": "How often do you utilise the information from code coverage tools on Github while contributing?"
    },
    "Q43_2": {
        "kind": "barh",
        "order": matrix_order_1,
        "title": "How often do you utilise the information from code coverage tools on Github while reviewing?"
    },
    "Q30_1": {
        "kind": "barh",
        "title": "Code coverage is a good metric to consider as part of overall code quality",
        "order": matrix_order_2
    },
    "Q30_2": {
        "kind": "barh",
        "title": "Code coverage tools on open-source platforms provide an incentive to improve coverage",
        "order": matrix_order_2
    },
    "Q30_4": {
        "kind": "barh",
        "title": "For contributors: if my pull request improves coverage, I feel it's accepted quicker",
        "order": matrix_order_2,
        "colors": ["tab:blue"],
        "legend": False
    },
    "Q30_3": {
        "kind": "barh",
        "title": "For maintainers: I am more likely to approve a pull request that improves coverage",
        "order": matrix_order_2,
        "colors": ["tab:orange"],
        "legend": False
    },
    "Q23_1": {
        "kind": "barh",
        "order": matrix_order_1,
        "title": "How often do you write tests when contributing?"
    },
    "Q24_1": {
        "kind": "barh",
        "order": matrix_order_3,
        "title": "How often do you write tests with the intent of improving coverage?"
    },
    # "Q26_1": {
    #     "kind": "barh",
    #     "colors": ["tab:blue"],
    #     "order": matrix_order_3,
    #     "title": "How often are you encouraged by a person to improve your coverage?"
    # },
    # "Q26_2": {
    #     "kind": "barh",
    #     "colors": ["tab:blue"],
    #     "order": matrix_order_3,
    #     "title": "How often are you encouraged by a code coverage tool to improve your coverage?"
    # },
    ("Q26_1", "Q26_2"): {
        "kind": "barh",
        "colors": ["tab:blue", "mediumpurple"],
        "order": matrix_order_3,
        "title": "For contributors: how often are you encouraged to improve your coverage?",
        "columns": ["By a human", "By a coverage tool"],
    },
    "Q28_1": {
        "kind": "barh",
        "colors": ["tab:orange"],
        "order": matrix_order_3,
        "title": "For maintainers: how often do you (have to) ask a contributor to improve their coverage?",
        "legend": False
    },
    "Q36_1": {
        "kind": "barh",
        "order": matrix_order_3,
        "title": "How often do you neglect to fix a failing coverage status while contributing?"
    },
    "Q36_2": {
        "kind": "barh",
        "order": matrix_order_3,
        "title": "How often do you neglect to fix a failing coverage status while reviewing?"
    },
    "ranked_first": {
        "kind": "barh",
        "title": "Which functionality of a coverage tool provides the most incentive to improve coverage?",
        "xlabel": "Times ranked first"
    }
}
QUALITATIVE = [
    ("Q20", "What is a good coverage goal?"),
    ("Q27", "For contributors: Do you remember a particularly interesting instance where you were asked to improve coverage?"),
    ("Q29", "For maintainers: Do you remember a particularly interesting instance where you had to ask to improve coverage?"),
    ("Q31", "What is the best way to incetivize improving coverage?"),
    ("Q35", "When would you ignore a failing coverage check?"),
    ("Q42", "Two things you like about coverage tools?"),
    ("Q43", "Two things you dislike about coverage tools?"),
    ("Q44", "Additional comments"),
    ("Q17", "If you don't use coverage on Github, why? (alt. ending)"),
]



