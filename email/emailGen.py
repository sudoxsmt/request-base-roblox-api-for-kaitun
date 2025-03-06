import modules.mailtm as mailtm
import random
import string

def process_cookies(max,success_path,pattern):
    with open(success_path, 'a') as success_out:
            for _ in range(max):  # Loop exactly 45 times
                    recursiveEmail(success_out,pattern)
                    

def recursiveEmail(success_out,pattern):
    try:
        mailapi = mailtm.MailTM()
        char_set = string.ascii_letters
        
        while True:
            usermail = f"{pattern}{''.join(random.choice(char_set) for _ in range(5))}"
            password = f"{''.join(random.choice(char_set) for _ in range(7))}"
            mailDomain = mailapi.get_domain()
            maildetails = mailapi.create_account(mailDomain, usermail, password)
            
            if maildetails["status"] == 'OK':
                success_out.write(f'{usermail}@{mailDomain}:{password}\n')
                return True
    except Exception as e :
        recursiveEmail(success_out)
        
# Main function
def main():
    max = 5
    pattern = ""
    success_path = 'result/mailsuccess.txt'
    process_cookies(max, success_path,pattern)
    print(f'*******************************************************')

if __name__ == '__main__':
    main()
