import allure
from selenium.webdriver import Keys

from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC

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
            first_name_field.send_keys(Keys.CONTROL + 'A')
            first_name_field.send_keys(Keys.BACKSPACE)
            first_name_field.send_keys(new_name)
            self.name = new_name

    @allure.step('Save changes')
    def save_changes(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    @allure.step('Changes have been saved')
    def is_changes_saved(self):
        self.wait.until(EC.invisibility_of_element_located(self.SPINNER))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_FIELD))
        self.wait.until(EC.text_to_be_present_in_element_value(self.FIRST_NAME_FIELD, self.name))