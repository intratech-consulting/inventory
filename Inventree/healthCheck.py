import threading
import requests
import time
 
 
 
# function that performs healthcheck
def health_check(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Connection to {url} is OK.")
        else:
            print(f"Connection to {url} returned status code {response.status_code}.")
    except Exception as e:
        print(f"Connection to {url} failed: {e}")
 
# performs healthcheck every x-amount of time
def periodic_health_check(url, interval):
    while True:
        health_check(url)
        time.sleep(interval)
 
#starts health check
def start_health_check_thread(url, interval):
   
    # healthcheck thread
    health_check_thread = threading.Thread(target=periodic_health_check, args=(url, interval))
   
    # Set the thread as a daemon so it will exit when the main thread exits
    health_check_thread.daemon = True
   
    # Start the health check thread
    health_check_thread.start()
   
    print(f"Health check thread started for {url}. Checking every {interval} seconds.")
 
 
if __name__ == "__main__":
    url = f"http://inventree.localhost/api/stock/1/"
    category_url = "http://inventree.localhost/api/part/category/"
    payload = {}
    headers = {
        'Authorization': 'Basic bHVjYXM6cm9vdA==',
        'Cookie': 'csrftoken=V2WgldExQx0XKqBh7VaEjKQAVdwv4HV2; sessionid=viptlrlxu6uqvfsmdebrqyh0f1n4kvk2'
    }
    time_interval=5
   
    start_health_check_thread(url, time_interval)
   
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

    def stockIdList():
        url = "http://inventree.localhost/api/stock/"
        category_url = "http://inventree.localhost/api/part/category/"
        payload = {}
        headers = {
        'Cookie': 'csrftoken=U4f3aiFMtXqeenAz6du2wfmD9e5ymh1K; sessionid=fnoffjbzoqhv66k0n1zonlsjt0qoqrzj'
    }

    # Get category data
    category_response = requests.request("GET", category_url, headers=headers, data=payload)
    category_data = category_response.json()

    # Create category mapping
    category_mapping = {category["pk"]: category["pathstring"] for category in category_data}

    # Get stock data
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()