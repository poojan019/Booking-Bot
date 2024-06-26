import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values, max_tries=2):
        for attempt in range(max_tries):
            try:
                wait = WebDriverWait(self.driver, 30)
                star_filtration_box = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-filters-group"
                                                                                           "='class']")))
                star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

                for star_value in star_values:
                    for star_element in star_child_elements:
                        if star_element.text.strip() == f'{star_value} stars':
                            print(star_element.text.strip())
                            star_element = wait.until(
                                EC.presence_of_element_located((By.XPATH, f"//*[@data-filters-item"
                                                                          f"='class"
                                                                          f":class={star_value}']")))
                            star_element.click()
                            time.sleep(5)
            except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
                print(f"[+] Attempt {attempt + 1} has failed with error: {e}")
                if attempt < max_tries - 1:
                    time.sleep(3)
                else:
                    print(f"[+] Maximum tries reached. Element could not be clicked.")

    def sort_price_lowest_first(self):
        wait = WebDriverWait(self.driver, 30)
        sort_by_element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='sorters"
                                                                               "-dropdown-trigger']")))
        sort_by_element.click()
        time.sleep(1)
        lowest_price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-id='price']")))
        lowest_price_element.click()
        time.sleep(5)