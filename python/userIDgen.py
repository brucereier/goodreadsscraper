from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import csv
import re

bro = [31790427]

driver = webdriver.Firefox()

driver.get("https://www.goodreads.com/user/sign_in")

time.sleep(2)

sign_in_with_email_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/a[5]/button")
sign_in_with_email_button.click()

email_elem = driver.find_element(By.XPATH, "//*[@id='ap_email']")
password_elem = driver.find_element(By.XPATH, "//*[@id='ap_password']")

def send_keys_human_like(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) # waits between 0.1 to 0.3 seconds

# Use the function to send keys
send_keys_human_like(email_elem, "34bpr54@gmail.com")
send_keys_human_like(password_elem, "Bruce11232003!")

sign_in__button = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]')
sign_in__button.click()

csv_filename = f'../collections/userIds2.csv'

csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['UserID'])

input("Click Enter once you finish the captcha")

i = 0
while i < 450:
    try: 
    # Navigate to the page with friends or acquaintances
    # driver.get("URL_of_the_page_with_friends")
        print(i)
        url = f"https://www.goodreads.com/user/show/{bro[i]}"
        driver.get(url)
        # Extract user IDs from the page
        friends = driver.find_elements(By.XPATH, '//div[@class="bigBoxContent containerWithHeaderContent"]//a[@rel="acquaintance"]')
        for friend in friends:
            href = friend.get_attribute('href')
            user_id = re.search(r'/user/show/(\d+)-', href)
            print(href)
            print(user_id)
            if user_id:
                user_id = user_id.group(1)
                if user_id not in bro:
                    csv_writer.writerow([user_id])
                    bro.append(user_id)
    except NoSuchElementException:
        print("hehe")
    finally:
        i += 1
        time.sleep(random.uniform(1, 1.5))  # Random delay to mimic human behavior and avoid being blocked

csv_file.close()
driver.quit()