## cli.py
from typing import List
from pathlib import Path
from models import User, Property
from repo import Repository
from utils import list_properties, list_users, next_user_id
from recommender import vectorized_recommend

USERS_PATH = Path("usersownexample.json")
PROPS_PATH = Path("propertiesownexample.json")

def menu_loop() -> None:
    repo = Repository(USERS_PATH, PROPS_PATH)
    properties: List[Property] = repo.load_properties()
    users: List[User] = repo.load_users()

    while True:
        cmd = input(
            "\nCommands:\n"
            "  view_properties  - View all properties\n"
            "  list_users       - View all users\n"
            "  create_user      - Create a new user\n"
            "  edit_profile     - Edit a user's profile\n"
            "  delete_user      - Delete a user\n"
            "  recommend        - Recommend properties for a user\n"
            "  exit             - Exit program\n> "
        ).strip().lower()

        if cmd == "view_properties":
            list_properties(properties)

        elif cmd == "list_users":
            list_users(users)

        elif cmd == "create_user":
            create_user(users, repo)

        elif cmd == "edit_profile":
            edit_profile(users, repo)

        elif cmd == "delete_user":
            delete_user(users, repo)

        elif cmd == "recommend":
            uid = input("Enter user_id (e.g., 1-5): ").strip()
            topn = int((input("How many recommendations? (default 5): ").strip() or "5"))
            vectorized_recommend(properties, users, uid, top_n=topn)

        elif cmd == "exit":
            print("Bye!")
            break

        else:
            print("Unknown command. Please try again.")

def create_user(users: List[User], repo: Repository) -> None:
    print("\n=== Create New User ===")
    new_id = next_user_id(users)
    name = input("Name: ").strip() or f"User{new_id}"
    try:
        group_size = int(input("Group size (default 1): ").strip() or "1")
    except ValueError:
        group_size = 1
    env = input("Preferred environment (mountain/lake/beach/urban, default urban): ").strip().lower() or "urban"
    try:
        budget = float(input("Budget per night (default 150): ").strip() or "150")
    except ValueError:
        budget = 150.0

    users.append(User(user_id=new_id, name=name, group_size=group_size,
                      preferred_environment=env, budget=budget))
    repo.save_users(users)
    print(f"✅ User #{new_id} created.")

def edit_profile(users: List[User], repo: Repository) -> None:
    print("\n=== Edit User Profile ===")
    uid = input("Enter user_id to edit: ").strip()
    if not uid.isdigit():
        print("user_id must be an integer.")
        return
    uid_i = int(uid)
    u = next((x for x in users if x.user_id == uid_i), None)
    if not u:
        print("User not found.")
        return

    name = input(f"Name [{u.name}]: ").strip() or u.name
    gs = input(f"Group size [{u.group_size}]: ").strip()
    env = input(f"Preferred environment [{u.preferred_environment}]: ").strip().lower() or u.preferred_environment
    bdg = input(f"Budget/night [{u.budget}]: ").strip()

    u.name = name
    if gs:
        try:
            u.group_size = int(gs)
        except ValueError:
            print("Invalid group size. Keeping previous value.")
    u.preferred_environment = env
    if bdg:
        try:
            u.budget = float(bdg)
        except ValueError:
            print("Invalid budget. Keeping previous value.")

    repo.save_users(users)
    print("✅ Profile updated.")

def delete_user(users: List[User], repo: Repository) -> None:
    print("\n=== Delete User ===")
    uid = input("Enter user_id to delete: ").strip()
    if not uid.isdigit():
        print("user_id must be an integer.")
        return
    uid_i = int(uid)
    idx = next((i for i, x in enumerate(users) if x.user_id == uid_i), None)
    if idx is None:
        print("User not found.")
        return
    if input(f"Confirm delete user #{uid_i}? (y/n): ").strip().lower() == "y":
        users.pop(idx)
        repo.save_users(users)
        print("🗑️ User deleted.")
    else:
        print("Cancelled.")
