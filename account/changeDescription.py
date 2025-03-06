import requests
import html
from urllib.parse import unquote
from faker import Faker


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
                print(f'  CHANGE DESCRIPTION NAME: {user_name} ID : {user_id}')
                if phase == 'NEW':

                    fake = Faker()
                    txx = fake.sentence()
                    json_data = {
                        "description": txx
                    }

                    print(f'description: {txx}')

                    responseX = self.session.post(
                        "https://accountinformation.roblox.com/v1/description", json=json_data
                    )
                    
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
                        print(f'  GET CSRF FAILED BEFORE CHANGE DESCRIPTION')
                        continue
                    user_id_before = helper.get_authenticated_user('NEW')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE CHANGE DESCRIPTION')
                        continue


# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    process_cookies(file_path)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
