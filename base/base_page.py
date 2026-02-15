import  allure
from allure_commons.types import AttachmentType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10, poll_frequency=1.0)

    def open(self):
        with allure.step(f'Open {self.PAGE_URL} page'):
            self.driver.get(self.PAGE_URL)

    def is_opened(self):
        with allure.step(f'Page {self.PAGE_URL} is opened'):
            # allow URL to have extra query/fragment parts in CI; check prefix
            try:
                self.wait.until(lambda d: d.current_url.startswith(self.PAGE_URL))
            except Exception as exc:
                try:
                    allure.attach(self.driver.get_screenshot_as_png(), name='page-open-failure', attachment_type=allure.attachment_type.PNG)
                except Exception:
                    pass
                try:
                    allure.attach(self.driver.page_source, name='page-open-dom', attachment_type=allure.attachment_type.TEXT)
                except Exception:
                    pass
                current = None
                try:
                    current = self.driver.current_url
                except Exception:
                    pass
                raise AssertionError(f'Page did not open: expected prefix "{self.PAGE_URL}", current "{current}"') from exc

    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG,)
