import pandas as pd

# Step 1: Read in a CSV file using Pandas
# Load your survey responses into a Pandas DataFrame
df = pd.read_csv("data/rq3/censored/censored.csv", header=[0,1,2])

# Step 2: Iterate over the columns
columns_to_discard = []
for col in df.columns:
    # Step 2.1: List the column header(s), and some non-empty example data
    example_data = df[col].dropna().head().tolist()
    print(f"\nColumn: {col}")
    print(f"Example data: {example_data}")

    # Step 2.2: Ask the user if the column should be discarded or not
    discard_column = input("Do you want to discard this column? (yes/no): ").lower()
    if discard_column == 'yes':
        columns_to_discard.append(col)

# Step 3: Output a new file with selected columns removed
df_filtered = df.drop(columns=columns_to_discard)
# Define your output file
output_file = 'data/rq3/censored/censored_2.csv'
df_filtered.to_csv(output_file, index=False)

print(f"\nFiltered data has been saved to {output_file}")
