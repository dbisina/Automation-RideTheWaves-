import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


from datetime import datetime
from time import sleep

town = input("Enter Town Name: ")
city = input("Enter City Name: ")
state = input("Enter State Name: ")
country = input("Enter Country Name: ")


group_search = town + " " + city + " " + state + " " + country

path = "/Users/Miflow/Downloads/chromedriver.exe "
service = Service(executable_path=path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")


driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://web.facebook.com/")
driver.maximize_window()
sleep(2)

# cookies = WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, '//button[@class="_42ft _42y0 _9o-t _4jy3 _4jy1 selected _51sy"]'))).click()

email = driver.find_element(By.ID, "email")
email.send_keys("08161656841")
password = driver.find_element(By.ID, "pass")
password.send_keys("Aduragbemi07")
sleep(1)

login = driver.find_element(By.NAME, "login")
login.click()
sleep(3)

'''
searchbar = driver.find_element(
    By.XPATH,
    "//label[@class='x1a2a7pz x1qjc9v5 xnwf7zb x40j3uw x1s7lred x15gyhx8 x9f619 x78zum5 x1fns5xo x1n2onr6 xh8yej3 x1ba4aug xmjcpbm']",
)
searchbar.click()

element = driver.switch_to.active_element
element.send_keys(group_search)
element.send_keys(Keys.ENTER)



groups = driver.find_element(
    By.XPATH, "//a[@class='x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq xljulmy']",
)
groups.click()
'''

driver.get("https://web.facebook.com/search/groups?q=" + town.lower() + "%2C%20" + city.lower() + "%2C%20" + state.lower() + "%2C%20" + country.lower())

sleep(3)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "x6s0dn4")))  # Adjust class name if needed

page_source = driver.page_source
print(page_source)

soup = BeautifulSoup(page_source if page_source else driver.page_source, "html.parser")

private_groups = []
for group_card in soup.find_all("div", class_="x6s0dn4"):
    try:
        group_name = group_card.find("a", href=True).text.strip()
        description = group_card.find("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84").text.strip()
        private_indicator = group_card.find("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6").text.strip()

        if "Private" in private_indicator:
                if "town" in description.lower() or "community" in description.lower():    
                 private_groups.append({"name": group_name, "description": description})
    except AttributeError:
        print(f"Error parsing group card: {group_card}")


with open("facebook_groups.txt", "a", encoding="utf-8") as file:
    for group in private_groups:
        file.write(f"Group Name: {group['name']}\n")
        file.write(f"Description: {group['description']}\n\n")

print("Group information written to facebook_groups.txt")

driver.quit()  # Close the browser