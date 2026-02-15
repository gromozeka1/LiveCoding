import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class PersonalPage(BasePage):
    PAGE_URL = Links.PERSONAL_PAGE

    FIRST_NAME_FIELD = ('xpath', '//input[@name="firstName"]')
    SAVE_BUTTON = ('xpath', '//button[@type="submit"][1]')
    FORM_LOADER = ('xpath', '//div[@class="oxd-form-loader"]')
    FORM = ('xpath', '//div[@class="oxd-form"]')
    SPINNER = ('xpath', '//div[@class="oxd-loading-spinner"]')

    def change_first_name_field(self, new_name):
        with allure.step(f'Change First Name to "{new_name}" value'):
            first_name_field = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD))
            try:
                first_name_field.click()
            except Exception:
                pass

            # try clear, then a reliable select-all + delete, then type
            try:
                first_name_field.clear()
            except Exception:
                pass

            try:
                first_name_field.send_keys(Keys.CONTROL, 'a')
                first_name_field.send_keys(Keys.DELETE)
            except Exception:
                pass

            first_name_field.send_keys(new_name)

            # if the input did not update as expected, force it via JS and dispatch events
            try:
                current = first_name_field.get_attribute('value')
            except Exception:
                current = None
            if current != new_name:
                try:
                    self.driver.execute_script(
                        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",
                        first_name_field, new_name
                    )
                except Exception:
                    pass

            self.name = new_name

    @allure.step('Save changes')
    def save_changes(self):
        # ensure any form loader is gone before clicking
        try:
            self.wait.until(EC.invisibility_of_element_located(self.FORM_LOADER))
        except Exception:
            pass

        btn = self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        try:
            btn.click()
        except Exception:
            # fallback to JS click when an overlay intermittently intercepts the click
            self.driver.execute_script("arguments[0].click();", btn)

        # after clicking, wait for any transient form loader/spinner to finish
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.FORM_LOADER))
        except Exception:
            pass
        try:
            self.wait.until(EC.invisibility_of_element_located(self.FORM_LOADER))
        except Exception:
            pass

    @allure.step('Changes have been saved')
    def is_changes_saved(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.SPINNER))
        except Exception:
            pass

        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_FIELD))
        # explicitly poll the input's value attribute for the new name
        field = self.driver.find_element(By.XPATH, self.FIRST_NAME_FIELD[1])
        actual = None
        for i in range(15):
            try:
                actual = field.get_attribute('value')
            except Exception:
                actual = None
            print(f'is_changes_saved: attempt {i+1}, value="{actual}"')
            if actual == self.name:
                return True
            import time
            time.sleep(1)

        # attach diagnostics for investigation
        try:
            allure.attach(self.driver.get_screenshot_as_png(), name='profile-save-failure', attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
        try:
            allure.attach(self.driver.page_source, name='profile-save-dom', attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

        raise AssertionError(f'First name not saved: expected "{self.name}", actual "{actual}"')
