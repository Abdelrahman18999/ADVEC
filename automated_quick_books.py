import requests
from requests.auth import HTTPBasicAuth
import json

# Replace with your QuickBooks API credentials
CLIENT_ID = 'ABUnZM2gK0gKHmTa4MEFW23ueYZXul4LjOHh6jcJHRmi77RXfg'
CLIENT_SECRET = 'UAizwq34h4l13lqHGIDAw0f4D4HHbUA9Lj25090F'
REDIRECT_URI = 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl'

# Replace with your authorization code obtained from QuickBooks
AUTHORIZATION_CODE = 'AB11722939279eOcjtN63VpFXnx5rsHvtVC8r5FNaj45ZJBosq'

# Get Access Token
def get_access_token():
    url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': AUTHORIZATION_CODE,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Error obtaining access token: ' + response.text)

# Get the access token and store it
token_info = get_access_token()
access_token = token_info['access_token']
refresh_token = token_info['refresh_token']


#################################################################################################
#################################################################################################

# Make API Request To Export The Data

def fetch_quickbooks_data(access_token, company_id, report_name='ProfitAndLoss'):
    url = f'https://quickbooks.api.intuit.com/v3/company/{company_id}/reports/{report_name}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'accounting_method': 'Accrual'
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Error fetching data: ' + response.text)

# Example call
company_id = 'your_company_id'
report_data = fetch_quickbooks_data(access_token, company_id)
print(report_data)