from dotenv import load_dotenv
import os
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
from time import sleep
from places import towns_around_x
import re


load_dotenv()
fb_number = os.getenv("FB_NUMBER")
fb_password = os.getenv("FB_PASSWORD")
ch_driver_path = os.getenv("CH_DRIVER_PATH")


def main():
    # Get user input for reference location
    reference_town = input("Enter Town Name: ")
    reference_state = input("Enter State Name: ")
    reference_country = input("Enter Country Name: ")

    # Get radius in miles and convert to meters
    print("Enter radius circle in miles: ")
    radius_miles = float(input())
    conversion_factor = 1609.34
    radius_meters = radius_miles * conversion_factor

    # Combine reference location for places.py function
    town_of_consideration = (
        reference_town + ", " + reference_state + ", " + reference_country
    )

     # Get nearby towns using places.py
    nearby_towns = towns_around_x(town_of_consideration, radius_meters)

    # Start Chrome driver
    path = ch_driver_path  # Update with your chromedriver path
    service = Service(executable_path=path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://web.facebook.com/")
    driver.maximize_window()
    sleep(2)

    # Login to Facebook (replace with your login logic)
    # cookies = WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, '//button[@class="_42ft _42y0 _9o-t _4jy3 _4jy1 selected _51sy"]'))).click()

    email = driver.find_element(By.ID, "email")
    email.send_keys(fb_number)
    password = driver.find_element(By.ID, "pass")
    password.send_keys(fb_password)
    sleep(1)

    login = driver.find_element(By.NAME, "login")
    login.click()
    sleep(10)


    # Process each town to search for Facebook groups
    for town in nearby_towns:
        # Extract town, state, and country from the dictionary
        town_name = town["town"]
        state_name = town["state"]
        country_name = town["country"]

        # Construct the Facebook group search URL
        search_url = f"https://web.facebook.com/search/groups?q={town_name.lower()}%2C%20{state_name.lower()}%2C%20{country_name.lower()}"

        # Access the search page and scrape group information
        driver.get(search_url)
        sleep(10)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "x6s0dn4"))
        )

        page_source = driver.page_source
        soup = BeautifulSoup(
            page_source if page_source else driver.page_source, "html.parser"
        )

        private_groups = []
        for group_card in soup.find_all("div", class_="x6s0dn4"):
            try:
                group_name = group_card.find("a", href=True).text.strip()
                group_link = group_card.find("a", href=True)["href"]
                description = group_card.find(
                    "span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84"
                ).text.strip()
                private_indicator = group_card.find(
                    "span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6"
                ).text.strip()
                
                # Extract member count using regular expression (only consider 'Xk members' format)
                
                member = re.search(r'\d+(?:\.\d+)?\s*(?:k|K) members', private_indicator)
                if member:
                    member_count = member.group(0)

                if "Private" in private_indicator and member:
                    if "town" in description.lower() or "community" in description.lower() and town_name in description.lower():
                        private_groups.append({"name": group_name, "link": group_link, "state": state_name, "members": member_count})
            except AttributeError:
                print(f"Error parsing group card: {group_card}")

        # Write private group information to a file
        with open("facebook_groups.txt", "a", encoding="utf-8") as file:
            for group in private_groups:
                file.write(f"Group Name: {group['name']}\n")
                file.write(f"Group Link: {group['link']}\n\n")
                file.write(f"Members: {group['members']}\n\n")
                file.write(f"State: {group['state']}\n\n\n")

 
    print("Group information written to facebook_groups.txt")


if __name__ == "__main__":
    main()
