import pytest
import allure

from config.data import Data
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.personal_page import PersonalPage

class BaseTest:
    login_page: LoginPage
    dashboard_page: DashboardPage
    personal_page: PersonalPage

    data: Data

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver
        request.cls.data = Data

        request.cls.login_page = LoginPage(driver)
        request.cls.dashboard_page = DashboardPage(driver)
        request.cls.personal_page = PersonalPage(driver)