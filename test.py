import requests

# Define the base URL of your invenTree instance
base_url = "http://inventree.localhost/api/"

# Specify the endpoint for inventory adjustments
endpoint = 'stock/add/'

# Prepare the data for the adjustment
adjustment_data = {
  "items": [
    {
      "pk": 1218,
      "quantity": "5",
      "batch": "string",
      "status": 10,
      "packaging": "string"
    }
  ],
  "notes": "string"
}

# Prepare the API request
url = f'{base_url}{endpoint}'
headers = {
    'Content-Type': 'application/json',
    'Authorization': "Basic cm9vdDpSb2JiZQ==",  # Replace with your API token
    'Cookie':'csrftoken=ymtnbUEffT6QNAothXZwOKHGRd6UxeBU; sessionid=6r2ezqmtp7dx9tfs12rp7vtgvqyax1nv'
}

def checkHealth():
    response = requests.post(url, headers=headers, json=adjustment_data)

    # Check the response status
    if response.status_code == 201:
        print('Stock adjustment successful!')
        return 1
    else:
        print(f'Failed to adjust stock. Status code: {response.status_code}')
        print(f'Response content: {response.text}')
    # Make the POST request to adjust the stock
    return 0
