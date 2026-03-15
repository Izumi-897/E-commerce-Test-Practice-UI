from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchPage(BasePage):
    # --- 页面元素定位 (Locators) ---
    # 首页搜索跳转入口 (占位元素)
    HOME_PLACEHOLDER = (By.XPATH, "//input[@placeholder='点击前往搜索']")

    # 搜索页核心输入框
    REAL_INPUT = (By.XPATH, "//input[@placeholder='请输入商品名称']")

    # 搜索结果中的商品标题列表
    GOODS_TITLES = (By.CSS_SELECTOR, ".van-card__title")

    def click_home_placeholder(self):
        """点击首页搜索入口并跳转至搜索详情页"""
        self.click(self.HOME_PLACEHOLDER)

    def search_item(self, keyword):
        """
        根据关键词执行商品搜索
        :param keyword: 待搜索的商品名称
        """
        # 填充搜索关键词
        self.input_text(self.REAL_INPUT, keyword)
        # 触发键盘回车提交搜索
        self.send_enter(self.REAL_INPUT)