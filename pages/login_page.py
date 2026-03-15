from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    # --- 页面元素定位 (Locators) ---
    # 用户名输入框
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='请输入测试账号 user123']")
    # 密码输入框
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='请输入测试密码 user123']")
    # 登录提交按钮
    LOGIN_BTN = (By.XPATH, "//span[text()='登录']/ancestor::button")

    def login(self, username, password):
        """
        执行登录业务流程
        :param username: 登录账号
        :param password: 登录密码
        """
        # 输入身份凭证
        self.input_text(self.USERNAME_FIELD, username)
        self.input_text(self.PASSWORD_FIELD, password)

        # 触发登录动作
        self.click(self.LOGIN_BTN)

        # 等待接口鉴权响应及页面跳转渲染
        import time
        time.sleep(1)