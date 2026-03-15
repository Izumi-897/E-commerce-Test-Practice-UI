import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.search_page import SearchPage
from pages.login_page import LoginPage


@allure.feature("商品模块")
class TestSearch:
    """商品检索业务逻辑测试套件"""

    @allure.story("商品搜索功能")
    @allure.title("通过首页入口执行关键词精准搜索")
    def test_search_and_verify(self, user_side):
        """
        验证全链路搜索流程：
        从首页搜索入口跳转，在搜索页提交关键词，并校验结果列表的准确性
        """
        driver = user_side
        wait = WebDriverWait(driver, 10)

        with allure.step("1. 初始化测试环境：执行身份鉴权并导航至首页"):
            driver.get("http://localhost:6255/#/login")
            LoginPage(driver).login("user123", "user123")
            wait.until(EC.url_contains("#/user"))
            driver.get("http://localhost:6255/#/home")

        search_pg = SearchPage(driver)
        with allure.step("2. 触发首页搜索入口跳转"):
            wait.until(EC.element_to_be_clickable(search_pg.HOME_PLACEHOLDER))
            search_pg.click_home_placeholder()

        with allure.step("3. 在搜索详情页提交关键词"):
            wait.until(EC.visibility_of_element_located(search_pg.REAL_INPUT))
            keyword = "四件套"
            search_pg.search_item(keyword)

        with allure.step(f"4. 验证搜索结果匹配度: '{keyword}'"):
            # 构造包含目标文本的动态 XPATH
            success_xpath = f"//*[contains(@class, 'van-card__title') and contains(text(), '{keyword}')]"
            try:
                # 等待检索结果刷新并捕获目标元素
                target = wait.until(EC.presence_of_element_located((By.XPATH, success_xpath)))
                actual_title = target.text

                # 记录核心断言数据至测试报告
                allure.attach(actual_title, name="Captured_First_Product_Title")
                assert keyword in actual_title, f"搜索结果不匹配！预期包含 {keyword}, 实际看到的是 {actual_title}"

            except Exception as e:
                # 异常处理：捕获失败现场上下文
                try:
                    actual_first = driver.find_element(By.CSS_SELECTOR, ".van-card__title").text
                    allure.attach(actual_first, name="Incorrect_Result_Title")
                except:
                    allure.attach("Element Not Found", name="UI_State_Error")

                # 生成失败现场截图并关联至 Allure
                driver.save_screenshot("search_result_error.png")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Search_Failure_Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"搜索业务验证未通过: {e}")