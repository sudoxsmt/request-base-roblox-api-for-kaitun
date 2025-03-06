import requests
import html
import random
from urllib.parse import unquote
import uuid


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

    def purchase_free_items(self,user_id_before, collectibleProductId, collectibleItemId):
        isDone = False
        for a in range(2): # sometimes even if we buy it once, it doesn't fall into inventory:
            if not isDone:
                try:
                    json_data = {
                        "collectibleItemId": collectibleItemId,
                        "expectedCurrency":1,
                        "expectedPrice":0,
                        "expectedPurchaserId": user_id_before,
                        "expectedPurchaserType":"User",
                        "expectedSellerId":1,
                        "expectedSellerType":"User",
                        "idempotencyKey":str(uuid.uuid4()),
                        "collectibleProductId":collectibleProductId
                    }
                    self.session.headers['authority'] = 'apis.roblox.com'
                    response = self.session.post(
                        f'https://apis.roblox.com/marketplace-sales/v1/item/{collectibleItemId}/purchase-item',
                        json=json_data,
                    )
                    print(response.json())
                    if response.json()["purchased"] or response.json()["errorMessage"] == 'QuantityLimitExceeded':
                        print(f"Buy Success")
                        isDone = True
                    else:
                        print(f"BuyFailed")
                except:
                    print(f"BuyFailed")
                    continue


    def humanize_avatar(self,user_id_before,random_number):
        mapping = {
            "collectibleProductId_1" : "33c7e0b2-9449-41af-ba6b-8ed074484ead",
            "collectibleItemId_1" : "b937b401-d825-4a60-907c-e6ecc0fc11c5",
            "oid_1" : 1481695805697415,
            "collectibleProductId_2" : "799cc52c-8d45-4d7b-9708-2723d7bb493e",
            "collectibleItemId_2" : "d2ac612f-1eab-4615-a82e-e12a3d4214fb",
            "oid_2" : 527480511691630,
            "collectibleProductId_3" : "1cbdaa99-1a31-49e1-89ee-9a80d6f7ed53",
            "collectibleItemId_3" : "15617694-4733-47d9-9da0-f9e81c6d8d14",
            "oid_3" : 1603021546947519,
            "collectibleProductId_4" : "226d2837-4577-45ae-bc7e-9e1847ebd4af",
            "collectibleItemId_4" : "edeb337d-21db-4d28-8340-3cbd936f329b",
            "oid_4" : 1603005150307515,
            "collectibleProductId_5" : "7d18168e-dffe-4b8e-be5a-38999a12564e",
            "collectibleItemId_5" : "144c44c9-81ab-404c-af7a-658345bc3a48",
            "oid_5" : 3062574390541833,
            "collectibleProductId_6" : "c07a7bc5-e334-4e15-96ac-a41ff83a7e06",
            "collectibleItemId_6" : "02f69457-d33d-469c-8c14-ceef07433986",
            "oid_6" : 1393877706095989,
            "collectibleProductId_7" : "fb882c6b-20eb-43be-9f92-f30f0c6cf5b0",
            "collectibleItemId_7" : "990bcff5-5117-4f3a-96f2-45a9af844eff",
            "oid_7" : 4362276636172134,
            "collectibleProductId_8" : "f9b3c845-899a-45a6-97d2-5945ffa96475",
            "collectibleItemId_8" : "d137eb09-7a2b-441c-ab7a-73a33347cc3a",
            "oid_8" : 2951189497115352,
            "collectibleProductId_9" : "d26dc7c6-ac4c-4426-ab6e-9e1e99227a6d",
            "collectibleItemId_9" : "74db195c-f91f-4052-a3b0-3f7389064ba7",
            "oid_9" : 1210660276868709,
            "collectibleProductId_10" : "3d379ec9-ec90-48c8-9035-0f8163f8dd3a",
            "collectibleItemId_10" : "61a6d0be-2ba1-43e2-a9ad-f7ccd5e9f5b2",
            "oid_10" : 3203330161601886
        }
        value = mapping.get(f"collectibleProductId_{random_number}", "Key not found")
        value2 = mapping.get(f"collectibleItemId_{random_number}", "Key not found")
        self.purchase_free_items(user_id_before,value ,value2)
        self.session.headers['authority'] = 'accountsettings.roblox.com'
        self.session.headers['x-bound-auth-token'] = 'pro-roblox-uhq-encrypted'
        try:
            for a in range(2):

                outfit_id = mapping.get(f"oid_{random_number}", "Key not found")
                print(f"Outfit ID : {outfit_id}")

                response = self.session.get(f'https://avatar.roblox.com/v1/outfits/{outfit_id}/details')

                assets = response.json()["assets"]
                bodyscale = response.json()["scale"]
                playerAvatarType = response.json()["playerAvatarType"]

                json_data = {
                    'height': int(bodyscale['height']),
                    'width': int(bodyscale['width']),
                    'head': int(bodyscale['head']),
                    'depth': int(bodyscale['depth']),
                    'proportion': int(bodyscale['proportion']),
                    'bodyType': int(bodyscale['bodyType']),
                }

                response = self.session.post('https://avatar.roblox.com/v1/avatar/set-scales',json=json_data)

                json_data = {
                    'assets':assets
                }

                response = self.session.post(
                    'https://avatar.roblox.com/v2/avatar/set-wearing-assets',
                    json=json_data,
                )

                json_data = {
                    'playerAvatarType': playerAvatarType,
                }

                response = self.session.post(
                    'https://avatar.roblox.com/v1/avatar/set-player-avatar-type',
                    json=json_data,
                )
                if response.status_code == 200:
                    print(response.json())
                    return True
                else:
                    return False
        except:
            return False

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

def process_cookies(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                    cookies = line.strip()
                    print(f'*******************************************************')
                    print(f'  CHANGE AVATAR')
                    proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
                    proxy = test_proxies(proxy)
                    helper = RobloxHelper(cookies, proxy)
                    try:
                        helper.get_csrf()  # Retrieve and set the CSRF token
                    except:
                        print(f'  GET CSRF FAILED BEFORE CHANGE AVATAR')
                        continue
                    user_id_before = helper.get_authenticated_user('NEW')
                    if not user_id_before:
                        print(f'  GET AUTHEN FAILED BEFORE CHANGE AVATAR ID : {user_id_before}')
                        continue
                    random_number = random.randint(1, 10)
                    isAddCollect = helper.humanize_avatar(user_id_before,random_number)
                    if isAddCollect:
                        print(f'  SUCCESS! ID : {user_id_before}')
                    else:
                        print(f'  FAIL CHANGE AVATAR AVATAR ID : {user_id_before}')


# Main function
def main():
    file_path = 'cookies.txt'  # Path to the file containing the cookies
    process_cookies(file_path)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
