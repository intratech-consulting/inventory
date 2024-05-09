import requests

def health_check(url):
    try:
        token = 'MY-TOKEN-VALUE-HERE'
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic cm9vdDpyb2JiZQ=='
            }
        url= "http://10.2.160.51:880/api/stock/remove/"
        payload = {
            "items": [
                {
                    "batch": "string",
                    "packaging": "string",
                    "pk": 1,
                    "quantity": 5,
                    "status": ""
                }
            ],
            "notes": "string"
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Connection to {url} is established.")
            
        else:
            print(f"Connection to {url} returned status code {response.status_code}.")
            return False
    except Exception as e:
        print(f"Connection to {url} failed: {e}")
        return False  # Return False if any exception occurs
 
