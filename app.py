import requests
import argparse

re = None
js = []
def set_username(username):
    try:
        global re, js
        re = requests.get(f"https://api.github.com/users/{username}/events")
        js = re.json()
        print("User found")
    except Exception:
        print("User not found")
        print(re.status_code)

def get_newest_push():
    probably_new = 0
    is_there = False
    while probably_new < len(js):
        if js[probably_new]['type'] == "PushEvent":
            newest_repo_pushed = js[probably_new]['repo']['name']
            num_commits_repo = js[probably_new]['payload']['size']
            print(f"    Last repository where it was pushed: {newest_repo_pushed}")
            print(f"    {num_commits_repo} commit(s) with {js[probably_new]['payload']['push_id']} push id")
            is_there = True
            break
        else:
            probably_new+=1
    if not is_there:
        print("    There's no newest push")


def get_n_pushes():
    n = int(input("Enter number of pushes: "))
    counter = 0
    i = 0
    while counter < n:
        try:
            if js[i]['type'] == "PushEvent":
                print(f"        {js[i]['payload']['size']} pushes to {js[i]['repo']['name']} with {js[i]['payload']['push_id']} id")
                counter+=1
            i+=1
        except Exception:
            print("----- End -----")
            break

def get_commits_of_id_push():
    id_push = int(input("Enter id push: "))
    i = 0
    found = False
    while i < len(js):
        if js[i]['type'] == "PushEvent":
            if js[i]['payload']['push_id'] == id_push:
                print(f"    Push on {js[i]['repo']['name']}")
                found = True
                for j in range(js[i]['payload']['size']):
                    print(f"        {j+1} - {js[i]['payload']['commits'][j]['message']}")
                break
        i+=1

    if found == False:
        print("not found")


def get_info():
    print(f"    ID: {js[0]['actor']['id']}")
    print(f"    Username: {js[0]['actor']['login']}")
    print(f"    URL: {js[0]['actor']['url']}")
    print(f"    Image: {js[0]['actor']['avatar_url']}")

def get_newest_creates():
    probably_new = 0
    is_there = False
    while probably_new < len(js):
        if js[probably_new]['type'] == "CreateEvent":
            create_type = js[probably_new]['payload']['ref_type']
            name = js[probably_new]['repo']['name']
            print(f"    {create_type} created - {name} on {js[probably_new]['created_at']}")
            is_there = True
            break
        else:
            probably_new += 1
    if not is_there:
        print("    There's no newest creates")



def get_n_creates():
    n = int(input("Enter number of creates: "))
    counter = 0
    i = 0
    while counter < n:
        try:
            if js[i]['type'] == "CreateEvent":
                print(f"    {js[i]['payload']['ref_type']} created, {js[i]['repo']['name']}")
                counter+=1
            i+=1
        except Exception:
            print("----- End -----")
            break

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser(description="GitHub User Activity")
    # Arguments
    parser.add_argument("username", type=str, help="argument required")
    args = parser.parse_args()

    # Arguments
    if args.username:
        user = args.username
        set_username(user)
        while True:
            print("1. Get newest push")
            print("2. Get n pushes")
            print("3. Get commits from a id push")
            print("4. Get info")
            print("5. Get newest create")
            print("6. Get n creates")
            print("7. Set another user")
            print("8. Exit")
            option = int(input("enter your selection: "))
            options = {1:get_newest_push, 2:get_n_pushes,
                       3: get_commits_of_id_push, 4:get_info,
                       5:get_newest_creates, 6:get_n_creates,
                       7:set_username}
            if option < 7 and option > 0:
                options[option]()
            elif option == 7:
                options[option](input("Enter new user: "))
            elif option == 8:
                break
            else:
                print("Error")