from io import BytesIO
from zipfile import ZipFile
import requests
import pandas as pd

# Download and extract the GeoNames ZIP data
url = "https://download.geonames.org/export/zip/US.zip"
response = requests.get(url)

with ZipFile(BytesIO(response.content)) as z:
    with z.open('US.txt') as f:
        df = pd.read_csv(
            f, 
            sep='\t', 
            header=None,
            dtype={1: str}  # Keep ZIP codes as strings (for leading zeros)
        )

# Assign column names based on GeoNames's current 12-column format
df.columns = [
    'country_code', 'postal_code', 'place_name', 
    'admin_name1', 'admin_code1', 'admin_name2', 
    'admin_code2', 'admin_name3', 'admin_code3',
    'latitude', 'longitude', 'accuracy'
]

# Group by city and state to find start/end ZIP codes
city_zips = (
    df.groupby(['place_name', 'admin_code1'])
    .agg(
        start_zipcode=('postal_code', 'min'), 
        end_zipcode=('postal_code', 'max')
    )
    .reset_index()
    # Combine state and city into "state-city" (e.g., "CA-Los Angeles")
    .assign(**{'state-city': lambda x: x['admin_code1'] + '-' + x['place_name']})
    # Select and reorder columns
    [['state-city', 'start_zipcode', 'end_zipcode']]
    # Sort by state-city for readability
    .sort_values(by='state-city')
)

# Save to CSV
city_zips.to_csv('state_city_zip_ranges.csv', index=False)
print("File saved: state_city_zip_ranges.csv")