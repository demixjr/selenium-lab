#use this command to pause the script
#input("press enter to continue")


#task1
# Імпорт webdriver
from selenium import webdriver
import pytest
# Імпорт класу By для пошуку елементів на веб-сторінці
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.maximize_window()


#task 2: Open page
# Відкрити головну сторінку
driver.get("https://the-internet.herokuapp.com")
# Отримати заголовок
title = driver.title
#Перевірити:
assert "The Internet" in title, f"Title does not contain 'The Internet'. Actual title: {title}"
#task 3:login

#incorrect credentials
driver.get("https://the-internet.herokuapp.com/login")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

username.send_keys("wrong_user")
password.send_keys("wrong_pass")
login_btn.click()

flash = driver.find_element(By.ID, "flash")
print(f"message: {flash.text}")

assert "invalid" in flash.text


#correct credentials
driver.get("https://the-internet.herokuapp.com/login")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

username.send_keys("tomsmith")
password.send_keys("SuperSecretPassword!")
login_btn.click()

flash = driver.find_element(By.ID, "flash")
print(f"Message: {flash.text}")

assert "You logged into a secure area" in flash.text
print("Тест з коректними даними пройдено")

#task 4

driver.get("https://the-internet.herokuapp.com/checkboxes")
checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

for cb in checkboxes:
    if not cb.is_selected():
        cb.click()

for cb in checkboxes:
    assert cb.is_selected()

driver.quit()