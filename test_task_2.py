from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.maximize_window()

#task5
import time
from selenium.webdriver.support.ui import WebDriverWait

wait = WebDriverWait(driver, 10)

driver.get("https://the-internet.herokuapp.com/javascript_alerts")

# JS Alert
driver.find_element(By.XPATH,
"//button[text()='Click for JS Alert']").click()

alert = driver.switch_to.alert
time.sleep(5)
alert.accept()

# JS Confirm
driver.find_element(By.XPATH,
"//button[text()='Click for JS Confirm']").click()
alert = driver.switch_to.alert
time.sleep(5)
alert.dismiss()

# JS Prompt
driver.find_element(By.XPATH,
"//button[text()='Click for JS Prompt']").click()
alert = driver.switch_to.alert
alert.send_keys("Hello")
time.sleep(5)
alert.accept()
input()


#task6
from selenium.common.exceptions import NoSuchElementException
# Перейти на сторінку nested_frames
driver.get("https://the-internet.herokuapp.com/nested_frames")

# 1. Отримати список фреймів верхнього рівня ---
top_frames = driver.find_elements(By.CSS_SELECTOR, "frame, iframe")
print(f"Знайдено фреймів верхнього рівня: {len(top_frames)}")

# Очікуємо 2 фрейми: frame-top і frame-bottom
assert len(top_frames) == 2

# 2. Переходимо у frame-top
driver.switch_to.frame("frame-top")

# Отримуємо вкладені фрейми (left, middle, right)
nested_frames = driver.find_elements(By.CSS_SELECTOR, "frame")
print(f"Вкладених фреймів у TOP: {len(nested_frames)}")

# Очікуємо 3 вклад ених фрейми
assert len(nested_frames) == 3

# 3. Перевіряємо текст у кожному вкладеному фреймі ---
test_data = [
    ("frame-left", "LEFT"),
    ("frame-middle", "MIDDLE"),
    ("frame-right", "RIGHT"),
]
for frame_name, expected_text in test_data:
    # кожен раз починаємо з frame-top
    driver.switch_to.default_content()
    driver.switch_to.frame("frame-top")
    driver.switch_to.frame(frame_name)

    actual_text = driver.find_element(By.TAG_NAME, "body").text.strip()
    print(f"{frame_name}: {actual_text}")

    assert expected_text in actual_text

# 4. Демонстрація помилки контексту
# Залишаємося у frame-middle
driver.switch_to.default_content()
driver.switch_to.frame("frame-top")
driver.switch_to.frame("frame-middle")
try:
    # Пробуємо знайти LEFT (який у іншому фреймі)
    driver.find_element(By.XPATH, "//body[text()='LEFT']")
    pytest.fail("Елемент знайдено, але не мав бути доступним у цьому фреймі")

except NoSuchElementException:
    print("✔ Очікувана помилка: неправильний контекст (інший фрейм)")

# 5. Виправлення — повернення до default і перехід у frame-left
driver.switch_to.default_content()
driver.switch_to.frame("frame-top")
driver.switch_to.frame("frame-left")
text = driver.find_element(By.TAG_NAME, "body").text.strip()
assert "LEFT" in text

print("\nКрок 5: Перемикання контексту для доступу до LEFT")
driver.switch_to.default_content()
driver.switch_to.frame("frame-top")
driver.switch_to.frame("frame-left")

left_text = driver.find_element(By.TAG_NAME, "body").text.strip()
print(f"Текст у frame-left: {left_text}")
assert "LEFT" in left_text, f"Очікували 'LEFT', але отримали '{left_text}'"

# 6. Перевірка frame-bottom
driver.switch_to.default_content()
driver.switch_to.frame("frame-bottom")
text = driver.find_element(By.TAG_NAME, "body").text.strip()
assert "BOTTOM" in text

print("\nКрок 6: Перевірка тексту у frame-bottom")
driver.switch_to.default_content()
driver.switch_to.frame("frame-bottom")

bottom_text = driver.find_element(By.TAG_NAME, "body").text.strip()
print(f"Текст у frame-bottom: {bottom_text}")
assert "BOTTOM" in bottom_text, f"Очікували 'BOTTOM', але отримали '{bottom_text}'"

input()

#task7
#flaky
import time
# Перейти на сторінку windows
driver.get("https://the-internet.herokuapp.com/windows")
# Клік
driver.find_element(By.LINK_TEXT, "Click Here").click()
# Переключення
windows = driver.window_handles # <--- список вкладок
driver.switch_to.window(windows[1])
time.sleep(5)
# Перевірка:
assert "New Window" in driver.page_source


#stable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# чекай до 10 секунд, але(!) тільки якщо потрібно
wait = WebDriverWait(driver, 10)
driver.get("https://the-internet.herokuapp.com/windows")

# 1. Рахуємо, скільки вкладок було ДО кліку
initial_count = len(driver.window_handles)
original_window = driver.current_window_handle

# 2. Клікаємо
driver.find_element(By.LINK_TEXT, "Click Here").click()

# 3. Чекаємо, поки кількість вкладок стане більшою, ніж була (initial_count + 1)
wait.until(lambda d: len(d.window_handles) > initial_count)

# 4. Знаходимо нову вкладку
new_window = [w for w in driver.window_handles if w != original_window][-1]
driver.switch_to.window(new_window)

# 5. Перевірка
header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
assert "New Window" in header.text

#task8
import os
from selenium.webdriver.common.by import By

# Перейти на сторінку відновлення пароля
driver.get("https://the-internet.herokuapp.com/forgot_password")

# Створення папки для збереження результатів
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Перелік елементів для пошуку за різними типами селекторів
elements_to_test = [
    (By.ID, "email", "id_email"),                   # Пошук за ID
    (By.NAME, "email", "name_email"),               # Пошук за Name
    (By.CSS_SELECTOR, ".example h2", "css_header"), # Пошук за CSS (заголовок)
    (By.ID, "form_submit", "id_button"),            # Пошук за ID (кнопка)
    (By.ID, "footer", "invalid_element")            # Неіснуючий елемент для тесту помилки
]

for by, value, filename in elements_to_test:
    try:
        # Спроба знайти та зробити скріншот конкретного елемента
        target = driver.find_element(by, value)
        target.screenshot(f"screenshots/{filename}_element.png")
        print(f"Скріншот елемента {filename} успішно збережено.")
    except Exception as e:
        # Скріншот всієї сторінки у разі помилки знаходження
        print(f"Помилка при пошуку {filename}: елемент не знайдено.")
        driver.save_screenshot(f"screenshots/{filename}_error_state.png")

# Фінальний скрін всієї сторінки
driver.save_screenshot("screenshots/full_page_final.png")

input()

driver.quit()