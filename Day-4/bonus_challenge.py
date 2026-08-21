# Bonus Challenge
# I used ChatGPT to generate a script that calls an API
# then I tried to understand each part of it

# Prompt I gave: "write a python script that calls a public API and shows the results"
# API it used: https://jsonplaceholder.typicode.com/posts

import requests

url = "https://jsonplaceholder.typicode.com/posts"  # this is the API endpoint

response = requests.get(url)  # sending a GET request to that URL

if response.status_code == 200:  # 200 means the request was successful
    posts = response.json()  # .json() converts the response text into a python list

    print(f"Total posts: {len(posts)}\n")

    for post in posts[:5]:  # only showing first 5 so the output isn't too long
        print("ID:", post['id'])
        print("User ID:", post['userId'])
        print("Title:", post['title'])
        print("Body:", post['body'][:80])  # cutting the body short since its long
        print("-" * 40)

else:
    print("Request failed:", response.status_code)


# My understanding of how this works:
#
# The requests.get() sends a GET request to the URL - basically asking the server
# for data without changing anything.
#
# The server responds with JSON which looks like a list of dictionaries in python.
# Each post has keys like 'id', 'userId', 'title', 'body'.
#
# response.json() converts that JSON text into actual python objects so I can
# access values like post['title'] normally.
#
# I also learned that status_code tells you if the request worked or not.
# 200 = success, anything else means something went wrong.
