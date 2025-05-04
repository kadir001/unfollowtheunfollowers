import requests

# Replace this with your GitHub personal access token
ACCESS_TOKEN = "your_personal_access_token"

# GitHub API base URL
BASE_URL = "https://api.github.com"

# Headers for authentication
HEADERS = {
    "Authorization": f"token {ACCESS_TOKEN}"
}

def get_following():
    """Fetch the list of users you are following."""
    url = f"{BASE_URL}/user/following"
    following = []
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Error fetching following list:", response.json())
            return []
        following.extend([user['login'] for user in response.json()])
        url = response.links.get('next', {}).get('url')  # Get the next page URL if exists
    return following

def get_followers():
    """Fetch the list of your followers."""
    url = f"{BASE_URL}/user/followers"
    followers = []
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Error fetching followers list:", response.json())
            return []
        followers.extend([user['login'] for user in response.json()])
        url = response.links.get('next', {}).get('url')  # Get the next page URL if exists
    return followers

def unfollow_user(username):
    """Unfollow a user."""
    url = f"{BASE_URL}/user/following/{username}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Unfollowed {username}")
    else:
        print(f"Failed to unfollow {username}: {response.json()}")

def main():
    print("Fetching following list...")
    following = set(get_following())
    print(f"Following: {len(following)} users")

    print("Fetching followers list...")
    followers = set(get_followers())
    print(f"Followers: {len(followers)} users")

    # Find users you follow who don't follow you back
    unfollowers = following - followers
    print(f"Unfollowers: {len(unfollowers)} users")

    if unfollowers:
        print("\nUsers you follow but who do not follow you back:")
        for user in unfollowers:
            print(user)

        # Ask if the user wants to unfollow them
        confirm = input("\nDo you want to unfollow these users? (yes/no): ").strip().lower()
        if confirm == "yes":
            for user in unfollowers:
                unfollow_user(user)
        else:
            print("No users were unfollowed.")
    else:
        print("Everyone you follow follows you back!")

if __name__ == "__main__":
    main()
