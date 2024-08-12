from locust import HttpUser, TaskSet, task, between
import json

from prompt import prompt


api = '/v1/chat/completions'

url = "http://0.0.0.0:62027"


class UserBehavior(TaskSet):

    @task
    def send_prompt(self):

        messages = [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        data = {
            "model": '/data1/ziyiliu/llm/OpenRLHF/checkpoint/qwen2-1.5b-sft-pet-1epoch',
            "messages": messages
        }

        with self.client.post(api, json=data, catch_response=True) as response:
            if response.status_code == 200:
                # Print the response for debugging purposes
                try:
                    response.encoding = 'utf-8'
                    # print(response.json())
                    response.success()
                except Exception as e:
                    print(e)
                    response.failure(f"Failed to decode response: {e}")
            else:
                print(f"Failed with status code: {response.status_code}")
                response.failure(f"Failed with status code: {response.status_code}")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(3, 8)
    host = url



if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --headless -u 50 -r 5 -t 1m --html=./report-1min.html")
