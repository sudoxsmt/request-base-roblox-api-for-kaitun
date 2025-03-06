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

# Function to open a browser tab, load a cookie, and process game favorite
def open_tab_with_cookie(cookie_value, game_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no UI)
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument("--silent")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(options=options)
    url = f'https://www.roblox.com/games/{game_id}'
    driver.get(url)

    time.sleep(1)  # Wait for page to load

    load_roblosecurity_cookie(driver, cookie_value)
    driver.get(url)  # Reload page after setting cookie

    time.sleep(1)  # Wait after refresh

    script = """
    setTimeout(() => {
        if(!document.querySelector(".icon-favorite.favorited")){
            document.getElementById('game-favorite-icon').click()
        }
    }, 1000);
    """
    
    driver.execute_script(script)
    time.sleep(4)
    driver.refresh()
    time.sleep(1)
    driver.execute_script(script)
    time.sleep(4)

    driver.quit()

# Main function to process all cookies with 6 game IDs each
def execute_batches(cookie_file, game_ids, batch_size=6, wait_time=5):
    cookies = get_cookies(cookie_file)  # Get cookies from file

    for cookie in cookies:
        print(f"Processing cookie: {cookie[-10:]}...")  # Prints last 10 characters
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            executor.map(lambda game_id: open_tab_with_cookie(cookie, game_id), game_ids)

        print(f"Waiting {wait_time} seconds before using the next cookie...")
        time.sleep(wait_time)

# List of 6 game IDs
game_ids = [2753915549, 8304191830, 18901165922, 17017769292, 16146832113, 8737899170]

# Run the script using all cookies in cookies.txt
execute_batches(cookie_file='cookies.txt', game_ids=game_ids)
