import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.address_page import AddressPage
from pages.login_page import LoginPage


@allure.feature("订单模块")
class TestAddress:
    """收货地址业务逻辑测试套件"""

    @allure.story("收货地址管理")
    @allure.title("新增地址异常校验")
    @pytest.mark.parametrize("name, tel, detail, expected_msg", [
        ("", "13800138000", "测试路1号", "请填写姓名"),
        ("张三", "123", "测试路2号", "请输入正确的手机号")
    ])
    def test_address_dynamic_errors(self, user_side, name, tel, detail, expected_msg):
        """测试不同非法输入场景下的表单字段校验逻辑"""
        driver = user_side
        wait = WebDriverWait(driver, 10)

        with allure.step("1. 初始化测试环境：执行登录并导航至地址管理页"):
            driver.get("http://localhost:6255/#/login")
            LoginPage(driver).login("user123", "user123")
            wait.until(lambda d: "#/login" not in d.current_url)
            driver.get("http://localhost:6255/#/user/address")

        addr_pg = AddressPage(driver)

        with allure.step("2. 进入新增地址表单界面"):
            addr_pg.go_to_add_form()

        with allure.step(f"3. 执行异常数据填充: {name}/{tel}"):
            addr_pg.fill_form_and_save(name, tel, detail)

        with allure.step(f"4. 验证错误提示信息: {expected_msg}"):
            # 构造动态 XPATH 定位校验信息元素
            error_xpath = f"//div[contains(@class, 'van-field__error-message') and text()='{expected_msg}']"
            error_el = wait.until(EC.presence_of_element_located((By.XPATH, error_xpath)))
            assert error_el.text == expected_msg

    @allure.story("收货地址管理")
    @allure.title("正常添加地址成功流程")
    def test_add_address_success(self, user_side):
        """验证全字段合法输入时，地址是否能成功保存并展示在列表中"""
        driver = user_side
        wait = WebDriverWait(driver, 10)

        with allure.step("1. 初始化测试环境：执行登录并导航至地址管理页"):
            driver.get("http://localhost:6255/#/login")
            LoginPage(driver).login("user123", "user123")
            wait.until(lambda d: "#/login" not in d.current_url)
            driver.get("http://localhost:6255/#/user/address")

        addr_pg = AddressPage(driver)
        test_name = "自动化测试"

        with allure.step("2. 填充合法地址信息并提交保存"):
            addr_pg.go_to_add_form()
            addr_pg.fill_form_and_save(test_name, "13812345678", "中关村大街1号")

        with allure.step("3. 校验地址列表持久化结果"):
            # 确认页面跳转回地址列表页
            wait.until(EC.url_contains("#/user/address"))
            # 等待 DOM 渲染完成后检索新增记录
            time.sleep(2)
            assert test_name in driver.page_source