import requests

def verify_credentials(client_id, client_secret):
    # Get OAuth token
    tracking = input('Enter tracking number: ')
    token_response = requests.post(
        "https://apis-tem.usps.com/oauth2/v3/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    )
    
    if token_response.status_code != 200:
        print(f"❌ Token request failed ({token_response.status_code}):", token_response.text)
        return False

    token_data = token_response.json()
    print("✅ Token obtained:", token_data)
    token = token_data['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Use TESTING endpoint for development
    
    api_url = f"https://apis-tem.usps.com/tracking/v3/tracking/{tracking}"
    
    # Add optional parameters for better results
    params = {
        'expand': 'DETAIL',  # Get full tracking history
        'destinationZIPCode': '90210'  # Example destination ZIP
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        print("📦 Tracking data:")
        print(response.json())
    else:
        print(f"❌ Tracking request failed ({response.status_code}):", response.text)
    
    return True

# Run with your credentials
verify_credentials(
    "fXRar8QhPPRwrODI04YH9JrUI1FidxEkdshur8asNC43KNPU",
    "AvD0DFCdzabBxweuXZle6OzXE6b5epx7UvR5dJmrkhhudA0I5AArV5r2ECeeJdhU"
)