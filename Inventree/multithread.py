import threading
import requests
import time



# function that performs healthcheck
def health_check(api_link):
    try:
        response = requests.get(api_link)
        if response.status_code == 200:
            print(f"Connection to {api_link} is OK.")
        else:
            print(f"Connection to {api_link} returned status code {response.status_code}.")
    except Exception as e:
        print(f"Connection to {api_link} failed: {e}")

# performs healthcheck every x-amount of time
def periodic_health_check(api_link, time_interval):
    while True:
        health_check(api_link)
        time.sleep(time_interval)

#starts health check
def start_health_check_thread(api_link, time_interval):
    
    # healthcheck thread
    health_check_thread = threading.Thread(target=periodic_health_check, args=(api_link, time_interval))
    
    # Set the thread as a daemon so it will exit when the main thread exits
    health_check_thread.daemon = True
    
    # Start the health check thread
    health_check_thread.start()
    
    print(f"Health check thread started for {api_link}. Checking every {time_interval} seconds.")


if __name__ == "__main__":
    api_link='https://www.kfdemoedigevrienden.be/'
    time_interval=30
    
    start_health_check_thread(api_link, time_interval)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
