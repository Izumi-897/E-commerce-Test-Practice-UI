import pytest
import allure
from selenium import webdriver

# 测试环境地址配置
USER_URL = "http://localhost:6255"
ADMIN_URL = "http://localhost:9527"


@pytest.fixture(scope="function")
def driver():
    """初始化 WebDriver 并配置移动端仿真参数"""
    options = webdriver.ChromeOptions()
    # 开启移动端仿真模式以适配移动端 UI 组件库的交互逻辑
    mobile_emulation = {"deviceName": "iPhone 12 Pro"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    _driver = webdriver.Chrome(options=options)
    _driver.implicitly_wait(5)
    yield _driver
    _driver.quit()


@pytest.fixture
def user_side(driver):
    """前台用户端页面入口"""
    driver.get(USER_URL)
    return driver


@pytest.fixture
def admin_side(driver):
    """后台管理端页面入口"""
    driver.get(ADMIN_URL)
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子函数：实现测试失败自动捕获截图并集成至 Allure 报告
    """
    outcome = yield
    rep = outcome.get_result()

    # 仅在用例执行阶段 (call) 且结果为失败 (failed) 时触发
    if rep.when == "call" and rep.failed:
        # 从 fixture 上下文中检索 WebDriver 实例
        driver = item.funcargs.get("user_side") or item.funcargs.get("admin_side") or item.funcargs.get("driver")

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure_Context_Screenshot",
                attachment_type=allure.attachment_type.PNG
            )