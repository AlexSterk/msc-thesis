import json
import os

import pandas as pd
from PyInquirer import prompt
from PyInquirer import style_from_dict, Token

from _questions import QUALITATIVE

QUALITATIVE = [q[0] for q in QUALITATIVE]

# Customize the PyInquirer style
style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

# Function to interactively review and flag responses
def flag_responses(df, last_reviewed_index, flagged_responses, save_interval):
    idx = last_reviewed_index + 1
    while idx < len(df):
        os.system('clear' if os.name == 'posix' else 'cls')  # Clear the console

        # Find the next unreviewed response
        row = df.iloc[idx]
        print(f"Response #{idx + 1}/{len(df)} (Press 'm' to flag as containing personal data, 'n' to go to next):")
        print()
        cont = False
        for column, value in row.items():
            if column[0] not in QUALITATIVE or pd.isnull(value):
                continue
            print(f"{value}")
            cont = True
        print()

        if not cont:
            idx = idx + 1
            continue

        # Prompt for flagging
        answers = prompt([
            {
                'type': 'list',
                'name': 'action',
                'message': 'Action:',
                'choices': [
                    {'name': 'Go to next', 'value': 'n'},
                    {'name': 'Mark as containing personal data', 'value': 'm'},
                    {'name': 'Exit and save', 'value': 'e'},
                ]
            }
        ], style=style)

        if answers['action'] == 'm':
            flagged_responses[idx] = True
            save_progress(idx, flagged_responses)
        elif answers['action'] == 'e':
            # Save progress before exiting
            save_progress(idx-1, flagged_responses)
            return
        elif answers['action'] == 'n':
            # Save progress if save_interval is reached
            if idx % save_interval == 0:
                save_progress(idx, flagged_responses)
        idx = idx + 1

    print("All responses have been reviewed.")

# Function to save progress
PROGRESS = 'data/rq3/censored/progress.json'
def save_progress(last_reviewed_index, flagged_responses):
    progress = {
        'last_reviewed_index': last_reviewed_index,
        'flagged_responses': flagged_responses.tolist()
    }
    with open(PROGRESS, 'w') as progress_file:
        json.dump(progress, progress_file)

# Load your survey responses into a Pandas DataFrame
df = pd.read_csv("data/rq3/results/survey_with_codes.csv", header=[0,1,2])

# Define your output file
output_file = 'data/rq3/censored/flagged_responses.csv'

# Define the interval at which progress is saved
save_interval = 5  # Change to your preferred value

# Load the progress information if it exists
if os.path.exists(PROGRESS):
    with open(PROGRESS, 'r') as progress_file:
        progress = json.load(progress_file)
    last_reviewed_index = progress['last_reviewed_index']
    flagged_responses = pd.Series(progress['flagged_responses'])
else:
    last_reviewed_index = -1
    flagged_responses = pd.Series(index=df.index, dtype=bool, data=False)

flag_responses(df, last_reviewed_index, flagged_responses, save_interval)

# Save flagged responses when all responses have been reviewed
df['Flagged'] = flagged_responses
df.to_csv(output_file, index=False)

# Remove progress file after completion
# os.remove('progress.json')