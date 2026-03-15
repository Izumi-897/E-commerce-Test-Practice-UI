import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage


@allure.feature("会员中心")
class TestLogin:
    """会员中心登录模块测试套件"""

    @allure.story("用户登录功能")
    @allure.title("账号密码正确 - 正常登录验证")
    def test_login_success(self, user_side):
        """验证使用合法凭证登录后的页面跳转逻辑"""
        driver = user_side
        wait = WebDriverWait(driver, 10)

        with allure.step("1. 导航至登录鉴权页面"):
            driver.get("http://localhost:6255/#/login")

        with allure.step("2. 提交合法的身份凭证"):
            login_pg = LoginPage(driver)
            login_pg.login("user123", "user123")

        with allure.step("3. 校验登录状态与路由跳转"):
            # 确认当前 URL 已移出登录路径
            is_redirected = wait.until(lambda d: "#/login" not in d.current_url)
            # 记录跳转后的终点 URL 到报告
            allure.attach(driver.current_url, name="Post_Login_URL")
            assert is_redirected, f"登录后页面未发生跳转，当前URL: {driver.current_url}"

    @allure.story("用户登录功能")
    @allure.title("登录异常场景校验: {username}")
    @pytest.mark.parametrize("username, password, expected_msg", [
        ("user123", "wrong_pwd", "账号密码不对"),
        ("", "user123", "账号不存在")
    ])
    def test_login_fail(self, user_side, username, password, expected_msg):
        """验证非法输入或错误凭证下的系统反馈机制"""
        driver = user_side

        with allure.step(f"1. 尝试使用账号 '{username}' 执行登录动作"):
            driver.get("http://localhost:6255/#/login")
            login_pg = LoginPage(driver)
            login_pg.login(username, password)

        with allure.step("2. 捕获 Toast 消息并执行断言"):
            wait = WebDriverWait(driver, 10)
            try:
                # 检索全局悬浮提示组件文本
                toast_el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "van-toast__text")))
                actual_msg = toast_el.text

                allure.attach(actual_msg, name="Captured_Toast_Message")
                assert expected_msg in actual_msg, f"预期提示包含 '{expected_msg}', 但实际弹窗是 '{actual_msg}'"

            except Exception as e:
                # 捕获失败现场并附加截图证供
                driver.save_screenshot(f"no_toast_{username}.png")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Notification_Capture_Failure",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"未能捕获到预期的系统提示信息: {e}")