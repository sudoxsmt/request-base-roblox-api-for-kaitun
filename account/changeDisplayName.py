import requests
import html
from urllib.parse import unquote
from markov_word_generator import MarkovWordGenerator, WordType, AllowedLanguages


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
                print(f'  CHANGE NAME NAME: {user_name} ID : {user_id}')
                if phase == 'NEW':

                    generator = MarkovWordGenerator(
                        markov_length=3,
                        language=AllowedLanguages.EN,
                        word_type=WordType.NAME,
                    )
                    tx1 = generator.generate_word()
                    print(f'  CHANGE NAME TO : {tx1}')
                    json_data = {"userId":user_id,"newDisplayName":tx1,"showAgedUpDisplayName":"false"}

                    response2 = self.session.patch(
                        f"https://users.roblox.com/v1/users/{user_id}/display-names", json=json_data
                    )

                    print(response2.json())
                    
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
                        print(f'  GET CSRF FAILED BEFORE CHANGE DISPLAYNAME')
                        continue
                    user_id_before = helper.get_authenticated_user('NEW')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE CHANGE DISPLAYNAME')
                        continue


# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    process_cookies(file_path)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
