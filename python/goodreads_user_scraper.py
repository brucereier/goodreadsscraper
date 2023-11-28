from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import csv
from user_ids import user_ids
from info import email, pw

def scrape_user_data(user_id, driver):
    url = f"https://www.goodreads.com/review/list/{user_id}?utf8=%E2%9C%93&shelf=read&per_page=infinite"
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    processed_books = set()


        # Capture the newly loaded data
    try:
        tbody = driver.find_element(By.XPATH, '//*[@id="booksBody"]')
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            title_element = row.find_element(By.CSS_SELECTOR, "td.field.title div.value a")
            full_title = title_element.text

            if full_title in processed_books:
                continue

            processed_books.add(full_title)

            author_element = row.find_element(By.CSS_SELECTOR, "td.field.author div.value a")
            author = author_element.text

            isbn_element = row.find_element(By.CSS_SELECTOR, "td.field.isbn div.value")
            isbn = driver.execute_script("return arguments[0].textContent;", isbn_element).strip()

            #avg_rating_element = row.find_element(By.CSS_SELECTOR, "td.field.avg_rating div.value")
            #avg_rating = avg_rating_element.text

            #date_pub_element = row.find_element(By.CSS_SELECTOR, "td.field.date_pub div.value")
            #date_pub = driver.execute_script("return arguments[0].textContent;", date_pub_element).strip()

            rating_element = row.find_element(By.CSS_SELECTOR, "td.field.rating div.value span.staticStars.notranslate")
            static_stars = rating_element.find_elements(By.CSS_SELECTOR, "span.staticStar.p10")
            rating_count = len(static_stars)
            if rating_count == 0:
                continue
            csv_writer.writerow([user_id, full_title, author, isbn, rating_count])
    except:
        print(f"Error processing user {user_id}")
        return

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
        time.sleep(random.uniform(0.1, 0.3))

send_keys_human_like(email_elem, email)
send_keys_human_like(password_elem, pw)

sign_in__button = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]')
sign_in__button.click()

csv_filename = f'../collections/userRatings.csv'

csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['UserID', 'Title', 'Author', 'ISBN', 'Rating'])

input("Click Enter once you finish the captcha")
i = 0
with open('../collections/userIds.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        scrape_user_data(row[0], driver)
        i += 1
        print(i)

csv_file.close()
driver.quit()
