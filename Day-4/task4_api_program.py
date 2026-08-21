import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

if response.status_code == 200:
    users = response.json()

    print(f"Got {len(users)} users\n")

    for user in users:
        print("Name:", user['name'])
        print("Email:", user['email'])
        print("Company:", user['company']['name'])
        print("---")

else:
    print("Something went wrong, status code:", response.status_code)
