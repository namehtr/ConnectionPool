import requests
import random
import time
import concurrent.futures

base_url = "http://127.0.0.1:5000"

user_ids = [f"user{random.randint(1, 10000)}" for _ in range(10000)]
def send_heartbeat(user_id):
    data = {
        "userId": user_id
    }

    response = requests.post(f"{base_url}/heartbeat",json=data)

    if response.status_code == 200:
        result = response.json()
        if result.get("success") == 1:
            print(f"Hearbeat sent for user {user_id}")
        else:
            print(f"Hearbeat failed for user {user_id}")
    else:
        print(f"Error sending heartbeat for user {user_id}: {response.text}")
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(send_heartbeat, user_ids)

end_time = time.time()
total_time = end_time - start_time
print(f"Total time taken: {total_time:.2f} seconds")