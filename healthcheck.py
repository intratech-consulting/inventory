import requests
import time
import threading
import HealthManager.py

# function that performs healthcheck
def health_check(url):
    try:
        token = 'MY-TOKEN-VALUE-HERE'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic bHVjYXM6cm9vdA==',
            'Cookie': 'csrftoken=V2WgldExQx0XKqBh7VaEjKQAVdwv4HV2; sessionid=viptlrlxu6uqvfsmdebrqyh0f1n4kvk2'
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            print(f"Connection to {url} is established.")
            
        else:
            print(f"Connection to {url} returned status code {response.status_code}.")
            return False
    except Exception as e:
        print(f"Connection to {url} failed: {e}")
        return False  # Return False if any exception occurs
 
# performs healthcheck every x-amount of time
def periodic_health_check(url, interval):
    while True:
        health_check(url)
        time.sleep(interval)
 
# starts health check
def start_health_check_thread(url, interval):
    # healthcheck thread
    health_check_thread = threading.Thread(target=periodic_health_check, args=(url, interval))
    # will now exit when the main exits
    health_check_thread.daemon = True
    # Start the health check thread
    health_check_thread.start()
    print(f"Health check thread started for {url}. Checking every {interval} seconds.")
 
if __name__ == "__main__":
    url = 'https://www.kfdemoedigevrenden.be/'
    interval = 5
    start_health_check_thread(url, interval)
   
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
