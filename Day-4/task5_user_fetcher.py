import requests

def get_users():
    url = "https://jsonplaceholder.typicode.com/users"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        print("Failed to load users")
        return []

def show_all_names(users):
    print("\nAll Users:")
    for user in users:
        print(f"  {user['id']}. {user['name']}")

def show_user_by_id(users, uid):
    found = False
    for user in users:
        if user['id'] == uid:
            print("\nUser Details:")
            print(f"  Name     : {user['name']}")
            print(f"  Username : {user['username']}")
            print(f"  Email    : {user['email']}")
            print(f"  Phone    : {user['phone']}")
            print(f"  City     : {user['address']['city']}")
            print(f"  Company  : {user['company']['name']}")
            found = True
            break
    if not found:
        print("No user found with that ID")

def main():
    print("=== User Information Fetcher ===")

    users = get_users()
    if not users:
        return

    show_all_names(users)

    while True:
        choice = input("\nEnter user ID to see details (or 0 to quit): ")

        if not choice.isdigit():
            print("Please enter a number")
            continue

        uid = int(choice)
        if uid == 0:
            print("Bye!")
            break

        show_user_by_id(users, uid)

main()
