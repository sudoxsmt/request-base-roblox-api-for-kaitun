import requests
import html
from urllib.parse import unquote

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

    def get_authenticated_user(self):
        url = 'https://users.roblox.com/v1/users/authenticated'
        response = self.session.get(url)
        
        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data.get('name')
            user_id = user_data.get('id')
            print(f"Authenticated UserName : {user_name} UserID: {user_id}")
                
            return user_id
        else:
            print(f"Failed to get user info for cookie. Status: {response.status_code}, Error: {response.text}")
            return None

def get_user_ids_from_cookies(cookies):
    user_ids = []
    for cookie in cookies:
        helper = RobloxHelper(cookie)
        helper.get_csrf()  # Retrieve and set the CSRF token
        user_id = helper.get_authenticated_user()
        if user_id:
            user_ids.append(user_id)
    return user_ids

def process_cookies(file_path, success_path, false_path):
    with open(file_path, 'r') as file, \
        open(success_path, 'w') as success_out, \
        open(false_path, 'w') as false_out:
        for line in file:
            if line.strip():
                cookies = line.strip()
                helper = RobloxHelper(cookies)
                helper.get_csrf()  # Retrieve and set the CSRF token
                user_id = helper.get_authenticated_user()
                if user_id:
                    success_out.write(f'{line.strip()}' + '\n')
                else:
                    false_out.write(line.strip() + '\n')

# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    success_path = 'result/validate_success.txt'
    false_path = 'result/validate_false.txt'
    process_cookies(file_path, success_path, false_path)

if __name__ == '__main__':
    main()
