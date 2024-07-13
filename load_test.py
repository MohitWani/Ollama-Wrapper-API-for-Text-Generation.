import requests
import concurrent.futures
import time

URL = 'http://localhost:5000/generate'
PAYLOAD = {'prompt': 'Hello, Ollama!'}
HEADERS = {'Content-Type': 'application/json'}

def send_request():
    response = requests.post(URL, json=PAYLOAD, headers=HEADERS)
    return response.status_code, response.elapsed.total_seconds()

def load_test(concurrent_requests):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        future_to_request = {executor.submit(send_request): i for i in range(concurrent_requests)}
        for future in concurrent.futures.as_completed(future_to_request):
            try:
                status_code, response_time = future.result()
                print(f'Status Code: {status_code}, Response Time: {response_time}s')
            except Exception as e:
                print(f'Request generated an exception: {e}')

if __name__ == '__main__':
    start_time = time.time()
    load_test(10)  
    end_time = time.time()
    print(f'Load test completed in {end_time - start_time} seconds')
