from selenium import webdriver
import time
import concurrent.futures

# Function to extract and process cookies from file
def get_cookies(file_path):
    cookies = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                cookies.append(line.strip())  # Add back _|
    return cookies

# Function to load the ROBLOSECURITY cookie into Selenium
def load_roblosecurity_cookie(driver, cookie_value):
    roblosecurity_cookie = {"name": ".ROBLOSECURITY", "value": cookie_value, "domain": ".roblox.com"}
    driver.add_cookie(roblosecurity_cookie)

# Function to open a browser tab, load a cookie, and process friend requests
def open_tab_with_cookie(cookie_value):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument("--silent")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    url = 'https://www.roblox.com/users/friends#!/friend-requests'
    driver.get(url)

    time.sleep(1)  # Wait for page to load

    load_roblosecurity_cookie(driver, cookie_value)
    url = 'https://www.roblox.com/users/friends#!/friend-requests'
    driver.get(url)
    # driver.refresh()

    time.sleep(1)  # Wait after refresh

    script = """
    setTimeout(() => {
        document.querySelectorAll('.accept-friend.btn-cta-md.btn-min-width').forEach(button => button.click());
    }, 2000);
    
    setTimeout(() => {
        document.querySelectorAll('.accept-friend.btn-cta-md.btn-min-width').forEach(button => button.click());
    }, 4000);
    """
    
    driver.execute_script(script)
    time.sleep(4)
    driver.refresh()
    time.sleep(1)
    driver.execute_script(script)
    time.sleep(4)

    driver.quit()

# Main function to execute batches of cookies
def execute_batches(cookie_file, batch_size=10, wait_time=10):
    cookies = get_cookies(cookie_file)  # Get cookies using the custom function

    for i in range(0, len(cookies), batch_size):
        cookie_batch = cookies[i:i + batch_size]

        if not cookie_batch:
            print("No more cookies to process.")
            break

        print(f"Processing batch {i // batch_size + 1}...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            executor.map(open_tab_with_cookie, cookie_batch)

        print(f"Waiting {wait_time} seconds before next batch...")
        time.sleep(wait_time)

# Run the script using all cookies in cookies.txt
execute_batches(cookie_file='cookies.txt')
