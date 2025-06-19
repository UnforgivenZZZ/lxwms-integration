import pandas as pd
import re
# Load CSV
df = pd.read_csv("~/Desktop/check.csv",encoding='utf-8')  # Replace with your CSV file path
print(df.columns)
# Select specific columns
columns_to_keep = [
    'Outbound Order No/出库单号',

]
filtered_df = df[columns_to_keep]

# Rename columns to remove Chinese (anything after the '/')
filtered_df.columns = [re.sub(r'/.*', '', col) for col in filtered_df.columns]

# Convert to JSON
json_data = filtered_df.to_json(orient="records", indent=2, force_ascii=False)

# Save to file
import json
with open("output.txt", "w", encoding="utf-8") as f:
    for j in json.loads(json_data):
        f.write(j['Outbound Order No']+'\n')

print("✅ JSON saved to output.json (with English-only column names)")
