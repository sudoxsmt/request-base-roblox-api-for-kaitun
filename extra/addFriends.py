from selenium import webdriver
import time
import re
import concurrent.futures
import random

# Function to extract the ROBLOSECURITY cookie value from the raw cookie string
def extract_roblosecurity_cookie(cookie_str):
    match = re.search(r'(_\|WARNING:-DO-NOT-SHARE-THIS.--.*?\|_)(.*)', cookie_str)
    if match:
        return {"name": ".ROBLOSECURITY", "value": match.group(2), "domain": ".roblox.com"}
    else:
        raise ValueError("ROBLOSECURITY cookie not found in the given string!")

# Function to load the extracted cookie into Selenium
def load_roblosecurity_cookie(driver, cookie_str):
    roblosecurity_cookie = extract_roblosecurity_cookie(cookie_str)
    driver.add_cookie(roblosecurity_cookie)

# Function to open a tab with specific cookies and execute JavaScript
def open_tab_with_cookie_and_profile(cookie_str, user_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument("--silent")  # Ensure quiet operation
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    
    # Navigate to the Roblox profile URL
    url = f'https://www.roblox.com/users/{user_id}/profile'
    driver.get(url)

    # Wait for the page to load completely before adding cookies
    time.sleep(3)

    # Load the ROBLOSECURITY cookie into the session
    load_roblosecurity_cookie(driver, cookie_str)

    # Refresh the page to apply the cookies
    driver.refresh()

    # Wait for the page to load again after refreshing
    time.sleep(3)

    # Execute the JavaScript to click the "Add Friend" button
    script = """
    setTimeout(function() {
        let button = [...document.querySelectorAll('button')]
            .find(b => b.innerText.includes('Add Friend'));

        if (button) {
            button.click();
            setTimeout(() => window.close(), 1000); // Close tab after 1 second
        }
    }, Math.floor(Math.random() * (7000 - 2000 + 1)) + 2000);
    """
    driver.execute_script(script)

    # Wait for the script to execute and the tab to close
    time.sleep(8)

    # Close the browser tab
    driver.quit()

# Read cookies from a file (assuming the cookies are stored in 'cookies.txt') and return a list of cookies
def get_cookies(cookie_file, max_cookies):
    with open(cookie_file, 'r') as f:
        cookie_lines = f.readlines()

    # Extract the first 'max_cookies' cookies (strings in the raw format)
    return cookie_lines[:max_cookies], cookie_lines[max_cookies:]

# Write used cookies to a new file and return the remaining cookies
def save_used_cookies(used_cookies, used_cookie_file='used_cookies.txt'):
    with open(used_cookie_file, 'a') as f:
        f.writelines(used_cookies)

# Main execution function to run 6 tabs at a time for each batch of user IDs and cookies
def execute_batches(cookie_file, user_id_file, max_user_ids, max_cookies, batch_size=10, wait_time=60):
    # Get the user IDs and cookies to use
    with open(user_id_file, 'r') as f:
        user_ids = [line.strip() for line in f.readlines()]

    cookies, remaining_cookies = get_cookies(cookie_file, max_cookies)

    # Execute each batch of user IDs and cookies in parallel (1 user ID, 6 different cookies per batch)
    for i in range(max_user_ids):
        user_id = user_ids[i]
        print(f"ADD FRIEND {user_id}")
        # Get 6 cookies for this user ID batch (for 6 tabs)
        # cookie_batch = cookies[i * batch_size: (i + 1) * batch_size]
        cookie_batch = random.sample(cookies, batch_size)

        # Ensure there are exactly 6 cookies in the batch
        if len(cookie_batch) < batch_size:
            print(f"Not enough cookies for user {user_id}, skipping.")
            continue

        # Execute each tab with the same user ID but different cookies
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            executor.map(lambda args: open_tab_with_cookie_and_profile(args[0], args[1]), zip(cookie_batch, [user_id] * batch_size))

        # After processing a batch, move used cookies to the used file
        save_used_cookies(cookie_batch)

        # Update the cookies file to remove used cookies
        with open(cookie_file, 'w') as f:
            f.writelines(remaining_cookies)

        # Wait for the next batch after each set of 6 tabs
        print(f"Waiting for {wait_time} seconds before processing the next batch...")
        time.sleep(wait_time)
        
max_user_ids = 200
max_cookies = 2000
user_id_file = "user_id_for_add.txt"
cookie_file = "cookies.txt"

# Run the execution with a limit on the number of user IDs and cookies
execute_batches(cookie_file=cookie_file, user_id_file=user_id_file, max_user_ids=max_user_ids, max_cookies=max_cookies)
