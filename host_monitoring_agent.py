import psutil
import requests

BASE_URL = "http://localhost:8000"

print("Local host monitoring agent started...")
print("Sending host metrics to Docker container every second...\n")

try:
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        payload = {"cpu_usage": cpu_usage}
        response = requests.post(f"{BASE_URL}/metrics", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"[Host -> Docker] CPU: {data['cpu_usage']}% | Time: {data['timestamp']} | ID in DB: {data['id']}.")
        else:
            print(f"Container error: {response.status_code}.")

except KeyboardInterrupt:
    print("\nAgent stopped by user.")
except Exception as e:
    print(f"\nConnection error to Docker container: {e}.")