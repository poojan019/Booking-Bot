import time

import constants as const
import os
from booking_filtration import BookingFiltration
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\WebDrivers\chromedriver-win64", teardown=False, experimental_options=None,
                 extension_path=None):
        self.driver_path = driver_path
        self.teardown = teardown
        super(Booking, self).__init__()
        os.environ['PATH'] += self.driver_path

        options = Options()

        if extension_path:
            for extension in extension_path:
                options.add_extension(extension)

        if experimental_options:
            for key, value in experimental_options.items():
                options.add_experimental_option(key, value)

        super().__init__(options=options)

        self.implicitly_wait(30)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def dismiss_sign_in_info(self):
        dismiss_info = WebDriverWait(self, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Dismiss sign-in info."]')))
        dismiss_info.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.XPATH, '//button[@aria-label="Prices in Indian Rupee"]')
        currency_element.click()
        currency_element = self.find_element(By.XPATH, f'//button[@data-testid="selection-item"]//span[contains(text('
                                                       f'), "{currency}")]')
        currency_element.click()
        # time.sleep(7)

    def select_place_to_go(self, place_to_go, max_attempts=3):
        attempts = 0
        while attempts < max_attempts:
            try:
                search_field = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='ss' "
                                                                                                       "and "
                                                                                                       "@placeholder='Where "
                                                                                                       "are you going?']")))
                search_field.clear()
                search_field.click()
                search_field.send_keys(place_to_go)
                break
            except StaleElementReferenceException:
                attempts += 1
                time.sleep(2)
        # raise Exception(f"Failed to click the element after {max_attempts} attempts.")
        first_result = WebDriverWait(self, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@role='button' and @tabindex='-1']/div["
                                                      "@class='b0eaf5262b' and "
                                                      "@data-testid='autocomplete-result']/div["
                                                      "@class='ce5ee7d913']/div[@class='a3332d346a d2f04c9037' and "
                                                      f"text()='{place_to_go}']")))
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = WebDriverWait(self, 25).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@data-date="{check_in_date}"]')))
        check_in_element.click()
        check_out_element = WebDriverWait(self, 25).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@data-date="{check_out_date}"]')))
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(By.XPATH, f'//button[@data-testid="occupancy-config"]')
        selection_element.click()

        while True:
            decrease_adult_element = self.find_element(By.XPATH, "//button[@tabindex='-1' and @aria-hidden='true' and "
                                                                 "@type='button' and contains(@class, 'a83ed08757') "
                                                                 "and contains(@class, 'c21c56c305') and contains("
                                                                 "@class, 'f38b6daa18') and contains(@class, "
                                                                 "'d691166b09') and contains(@class, 'ab98298258') "
                                                                 "and contains(@class, 'deab83296e') and contains("
                                                                 "@class, 'bb803d8689') and contains(@class, "
                                                                 "'e91c91fa93')]")
            decrease_adult_element.click()
            adult_value_element = self.find_element(By.ID, "group_adults")
            adult_value = adult_value_element.get_attribute('value')
            if int(adult_value) == 1:
                break

        increase_adult_element = self.find_element(By.XPATH, "//button[@tabindex='-1' and @aria-hidden='true' and "
                                                             "@type='button' and contains(@class, 'a83ed08757') and "
                                                             "contains(@class, 'c21c56c305') and contains(@class, "
                                                             "'f38b6daa18') and contains(@class, 'd691166b09') and "
                                                             "contains(@class, 'ab98298258') and contains(@class, "
                                                             "'deab83296e') and contains(@class, 'bb803d8689') and "
                                                             "contains(@class, 'f4d78af12a')]")
        for _ in range(count - 1):
            increase_adult_element.click()
        done_element = self.find_element(By.XPATH, "//span[@class='e4adce92df' and text()='Done']")
        done_element.click()

    def search(self):
        search_element = self.find_element(By.XPATH, "//span[@class='e4adce92df' and text()='Search']")
        search_element.click()

    def apply_filters(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(2, 4)
        filtration.sort_price_lowest_first()
