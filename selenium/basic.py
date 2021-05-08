from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# IF USING SELENIUM FOR THE FIRST TIME IN A MAC, TYPE THIS IN THE TERMINAL:
# xattr -d com.apple.quarantine chromedriver 

# Do not open a browser
chrome_options = Options()
chrome_options.add_argument('--headless')

# Go to the url
driver = webdriver.Chrome(executable_path = './chromedriver', options = chrome_options)
driver.get('https://www.duckduckgo.com')

# Fill an input element
search_input = driver.find_element_by_id('search_form_input_homepage')
search_input.send_keys("my user agent")

# Click on an element
# search_btn = driver.find_element_by_id('search_button_homepage')
# search_btn.click()

# Or just click Enter
search_input.send_keys(Keys.ENTER)

# Show the page source
print(driver.page_source)

# It's a good practice getting drivers closed at the end of the script
driver.close()