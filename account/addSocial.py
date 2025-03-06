import requests
import html
import random
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
        
        value_csrf = html.unescape(response.text.split('"csrf-token" data-token="')[1].split('"')[0])
        value_csrf = unquote(value_csrf)
        self.csrf_token =  value_csrf
        self.session.headers["x-csrf-token"] = self.csrf_token

    def get_authenticated_user(self , phase):
        try:
            url = 'https://users.roblox.com/v1/users/authenticated'
            response = self.session.get(url)
            
            if response.status_code == 200:
                user_data = response.json()
                user_name = user_data.get('name')
                user_id = user_data.get('id')
                print(f'  ADDED SOCIAL : {user_name} ID : {user_id}')
                if phase == 'NEW':

                    random_number = random.randint(0, 10)
                    modified_username = f"{get_random_username()}{random_number}"

                    social_links = {
                        "youtube": f"www.youtube.com/{modified_username}",
                        "facebook": f"www.facebook.com/{modified_username.split('@')[1]}",
                        "twitch": f"www.twitch.tv/{modified_username.split('@')[1]}",
                        "guilded": f"www.guilded.gg/{modified_username.split('@')[1]}"
                    }

                    selected_key = random.choice(list(social_links.keys()))

                    json_data3 = {
                        "promotionChannelsVisibilityPrivacy":"AllUsers",
                        "facebook":"",
                        "twitter":"",
                        "youtube":"",
                        "twitch":"",
                        "guilded":""
                    }

                    json_data3[selected_key] = social_links[selected_key]
                    print(json_data3)
                    self.session.headers["authority"] = "accountinformation.roblox.com"
                    response4 = self.session.post(
                        "https://accountinformation.roblox.com/v1/promotion-channels", json=json_data3
                    )

                    print(response4.json())
                    
                return user_id
            else:
                return None
        except Exception as e:
            print(e)
            return None

def get_random_username(filename="dictionaries/social.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            usernames = [line.strip() for line in file if line.strip()]
        return random.choice(usernames) if usernames else None
    except FileNotFoundError:
        print("File not found!")
        return None

def process_cookies(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                    cookies = line.strip()
                    print(f'*******************************************************')
                    helper = RobloxHelper(cookies)
                    try:
                        helper.get_csrf()  # Retrieve and set the CSRF token
                    except:
                        print(f'  GET CSRF FAILED BEFORE CHANGE DISPLAYNAME')
                        continue
                    user_id_before = helper.get_authenticated_user('NEW')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE ADD SOCIAL')
                        continue


# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    process_cookies(file_path)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
