from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os
from user_ids import user_ids

def scrape_user_data(user_id, driver):
    url = f"https://www.goodreads.com/review/list/{user_id}?utf8=%E2%9C%93&shelf=read&per_page=infinite"
    driver.get(url)

    # Make sure "collections" directory exists
    if not os.path.exists('../collections'):
        os.makedirs('../collections')

    csv_filename = f'../collections/{user_id}.csv'

    csv_filename = f'collections/{user_id}.csv'
    csv_file = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Author', 'ISBN', 'Average Rating', 'Publication Date', 'Rating'])

    # Initialize variables for scrolling and duplicate checking
    last_height = driver.execute_script("return document.body.scrollHeight")
    processed_books = set()

    while True:
        # Scroll down by 1000 pixels
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

        # Capture the newly loaded data
        tbody = driver.find_element(By.XPATH, '//*[@id="booksBody"]')
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            title_element = row.find_element(By.CSS_SELECTOR, "td.field.title div.value a")
            full_title = title_element.text

            # Skip this iteration if book has already been processed
            if full_title in processed_books:
                continue

            # Mark the book as processed
            processed_books.add(full_title)

            author_element = row.find_element(By.CSS_SELECTOR, "td.field.author div.value a")
            author = author_element.text

            isbn_element = row.find_element(By.CSS_SELECTOR, "td.field.isbn13 div.value")
            isbn = driver.execute_script("return arguments[0].textContent;", isbn_element).strip()

            avg_rating_element = row.find_element(By.CSS_SELECTOR, "td.field.avg_rating div.value")
            avg_rating = avg_rating_element.text

            date_pub_element = row.find_element(By.CSS_SELECTOR, "td.field.date_pub div.value")
            date_pub = driver.execute_script("return arguments[0].textContent;", date_pub_element).strip()

            rating_element = row.find_element(By.CSS_SELECTOR, "td.field.rating div.value span.staticStars.notranslate")
            static_stars = rating_element.find_elements(By.CSS_SELECTOR, "span.staticStar.p10")
            rating_count = len(static_stars)

            # Write data to CSV
            csv_writer.writerow([full_title, author, isbn, avg_rating, date_pub, rating_count])

        # Check if scrolled to the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    csv_file.close()

driver = webdriver.Firefox()

driver.get("https://www.goodreads.com/user/sign_in")

time.sleep(2)

sign_in_with_email_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/a[5]/button")
sign_in_with_email_button.click()

email_elem = driver.find_element(By.XPATH, "//*[@id='ap_email']")
password_elem = driver.find_element(By.XPATH, "//*[@id='ap_password']")

email_elem.send_keys("email")
password_elem.send_keys("pw")

sign_in__button = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]')
sign_in__button.click()

for user_id in user_ids:
    scrape_user_data(user_id, driver)

driver.quit()
