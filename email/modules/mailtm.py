import requests

class MailTM:
    def __init__(self ):
        self.session = requests.Session()

        self.session.headers = {
            "authority": "api.mail.tm",
            "accept": "application/json, text/plain, */*",
            "accept-language": "tr-TR,tr;q=0.7",
            "origin": "https://mail.tm",
            "referer": "https://mail.tm/",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

    def get_domain(self):
        r = self.session.get("https://api.mail.tm/domains")
        return r.json()["hydra:member"][0]["domain"]

    def create_account(self, domain,usermail,password):
        mail = usermail.lower()
        passw = password
        json_data = {
            "address": f"{mail}@{domain}",
            "password": f"{passw}",
        }

        r = self.session.post("https://api.mail.tm/accounts", json=json_data)

        if r.status_code == 201:
            print({"status": "OK", "mail": f"{mail}@{domain}", "password": passw})
            return {"status": "OK", "mail": f"{mail}@{domain}", "password": passw}
        if r.status_code != 201:
            print({"status": "ERROR", "response": r.text})
            return {"status": "ERROR", "response": r.text}

    def get_account_token(self, mail, mail_passw):
        json_data = {
            "address": mail.strip(),
            "password": mail_passw.strip(),
        }

        response = self.session.post("https://api.mail.tm/token", json=json_data)
        return response.json()["token"]

    def get_mail(self, bearer_token):
        self.session.headers["authorization"] = f"Bearer {bearer_token}"

        response = self.session.get("https://api.mail.tm/messages")

        del self.session.headers["authorization"]

        return response.json()

    def get_mail_content(self, bearer_token, message_id):
        self.session.headers["authorization"] = f"Bearer {bearer_token}"
        response = self.session.get(f"https://api.mail.tm/messages/{message_id}")

        del self.session.headers["authorization"]

        return response.json()
