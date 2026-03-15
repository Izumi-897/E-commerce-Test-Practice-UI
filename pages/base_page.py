from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    """页面基础类，封装底层交互逻辑"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, locator):
        """显式等待并获取单个元素"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def input_text(self, locator, text):
        """
        向目标元素输入文本
        针对动态渲染架构增加了重试机制与 JS 事件分发，确保数据绑定生效
        """
        for i in range(3):
            try:
                el = self.wait.until(EC.element_to_be_clickable(locator))

                # 清理影响交互的全局遮罩层或弱提示组件
                self.driver.execute_script("""
                    var masks = document.querySelectorAll('.van-overlay, .van-toast');
                    masks.forEach(m => m.remove());
                """)

                # 通过 JavaScript 强制赋值并触发框架监听的 input/change 事件
                js_code = """
                    var input = arguments[0];
                    input.value = arguments[1];
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                """
                self.driver.execute_script(js_code, el, text)
                return

            except StaleElementReferenceException:
                if i == 2: raise
                # 捕获 DOM 刷新导致的陈旧引用，进行重试补救
                import time
                time.sleep(0.5)

    def click(self, locator):
        """元素点击操作"""
        self.find_element(locator).click()

    def send_enter(self, locator):
        """模拟键盘回车事件"""
        self.find_element(locator).send_keys(Keys.ENTER)