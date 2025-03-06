import requests
import html
import time
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
                print(f'NOTIFY NAME: {user_name} ID : {user_id}')
                if phase == 'NEW':

                    game_ids = [994732206, 3183403065, 5578556129,6401952734]  # Replace with actual game IDs
                    #game_ids = [BF, AA, AV, PET GO]  # Replace with actual game IDs

                    for game_id in game_ids:
                        data = {"universeId":game_id,"userId":user_id}
                        url = f"https://followings.roblox.com/v1/users/{user_id}/universes/{game_id}"
                        self.session.headers["authority"] = "followings.roblox.com"
                        response2 = self.session.post(url ,json=data)
                        time.sleep(1)
                        print(f"Game {game_id}: {response2.status_code} - {response2.text}")
                    
                return user_id
            else:
                return None
        except Exception as e:
            print(e)
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
                        print(f'  GET CSRF FAILED BEFORE NOTIFY')
                        continue
                    user_id_before = helper.get_authenticated_user('NEW')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE NOTIFY')
                        continue


# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    process_cookies(file_path)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
