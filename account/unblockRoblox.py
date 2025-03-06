import requests
import html
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

class RobloxHelper:
    def __init__(self, cookie):
        self.session = requests.Session()
        self.cookie = cookie
        self.session.headers.update({
            'Cookie': f'.ROBLOSECURITY={self.cookie}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer' : 'https://www.roblox.com/'
        })
        self.csrf_token = None

    def get_csrf(self):
        response = self.session.get("https://www.roblox.com/home")
        
        # Extract CSRF token from the response text
        value_csrf = html.unescape(response.text.split('"csrf-token" data-token="')[1].split('"')[0])
        value_csrf = unquote(value_csrf)
        #self.csrf_token =  html.unescape(value_csrf)
        self.csrf_token =  value_csrf
        self.session.headers["x-csrf-token"] = self.csrf_token
        #print(f"CSRF Token: {self.csrf_token}")

    def get_authenticated_user(self):
        url = 'https://users.roblox.com/v1/users/authenticated'
        response = self.session.get(url)
        
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get('id')
            print(f"Authenticated UserID: {user_id}")
            return user_id
        else:
            print(f"Failed to get user info for cookie. Status: {response.status_code}, Error: {response.text}")
            return None

    def unblock_user(self, target_user_id):
        url = f'https://accountsettings.roblox.com/v1/users/{target_user_id}/unblock'
        response = self.session.post(url)
        
        if response.status_code == 200:
            print(f"User {target_user_id} unblocked successfully!")
        else:
            print(f"Failed to unblock user {target_user_id}. Status: {response.status_code}, Error: {response.text}")

def get_user_ids_from_cookies(cookies):
    user_ids = []
    for cookie in cookies:
        helper = RobloxHelper(cookie)
        helper.get_csrf()  # Retrieve and set the CSRF token
        user_id = helper.get_authenticated_user()
        if user_id:
            user_ids.append(user_id)
    return user_ids

def process_cookies(file_path):
    with open(file_path, 'r') as file:
        cookies = []
        for line in file:
            if line.strip():
                    cookies.append(line.strip())  # Add '_|' back to the second part

    if not cookies:
        print("No cookies found in the file.")
        return

    # Get user IDs from all cookies
    user_ids = get_user_ids_from_cookies(cookies)

    if not user_ids:
        print("No user IDs found.")
        return

    # Use each cookie to block users from remaining cookies
    for i in range(len(cookies)):
        current_cookie = cookies[i]
        ids_to_block = user_ids[:i] + user_ids[i + 1:]  # Block users from other cookies
        print(f"\nProcessing cookie {i + 1}")
        
        helper = RobloxHelper(current_cookie)
        helper.get_csrf()  # Retrieve and set the CSRF token
        # helper.update_private_server_privacy()

        def unblock_user_safe(user_id):
            try:
                helper.unblock_user(user_id)
                #print(f"Successfully blocked user {user_id}")
            except Exception:
                print(f"Unblocking user {user_id} failed")

        # Use multithreading to block users concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust `max_workers` as needed
            futures = {executor.submit(unblock_user_safe, user_id): user_id for user_id in ids_to_block}

            for future in as_completed(futures):
                user_id = futures[future]
                try:
                    future.result()  # Check for any exceptions raised
                except Exception as e:
                    print(f"Error Unblocking user {user_id}: {e}")

# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    process_cookies(file_path)

if __name__ == '__main__':
    main()
