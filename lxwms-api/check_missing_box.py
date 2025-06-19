import pandas as pd

# Read CSV
df = pd.read_csv('~/Desktop/5.4.2025_SCAN.csv')

# Combine all non-null values into a set
all_values = set(
    df.fillna('')
    .stack()
    .apply(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace
    .replace('', pd.NA)  # Replace empty strings with NaN
    .dropna()            # Remove NaN values (originally empty after stripping)
    .values
)
arr = list(all_values)
arr.sort()
for a in arr:
    print(a)
try:
    
    with open('box.txt', 'r') as file:
        # Read non-empty lines into a set
        unique_lines = {line.strip() for line in file if line.strip()}
        print(unique_lines - all_values)
except FileNotFoundError:
    print("Error: File not found!")