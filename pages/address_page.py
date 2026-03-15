from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class AddressPage(BasePage):
    # --- 页面元素定位 (Locators) ---
    # 地址列表页：新增地址按钮
    ADD_BTN = (By.CSS_SELECTOR, ".van-address-list__add")

    # 地址编辑页：表单输入字段
    NAME_INPUT = (By.XPATH, "//input[@placeholder='收货人姓名']")
    TEL_INPUT = (By.XPATH, "//input[@placeholder='收货人手机号']")
    AREA_CLICKER = (By.XPATH, "//input[@placeholder='选择省 / 市 / 区']")
    DETAIL_INPUT = (By.XPATH, "//textarea[contains(@placeholder, '街道门牌')]")

    # 地区选择器确认按钮
    PICKER_CONFIRM = (By.CSS_SELECTOR, ".van-picker__confirm")

    # 表单提交按钮
    SAVE_BTN = (By.XPATH, "//span[text()='保存']/ancestor::button")

    def go_to_add_form(self):
        """跳转至新增地址表单页"""
        self.click(self.ADD_BTN)

    def select_default_area(self):
        """处理省市区选择器（默认选择第一项）"""
        # 唤起地区选择弹窗
        self.click(self.AREA_CLICKER)
        # 等待弹窗加载及动画过渡
        time.sleep(0.5)
        # 点击确认完成选择
        self.click(self.PICKER_CONFIRM)
        time.sleep(0.5)

    def fill_form_and_save(self, name, tel, detail):
        """填写地址表单并提交保存"""
        # 填充收货人基础信息
        self.input_text(self.NAME_INPUT, name)
        self.input_text(self.TEL_INPUT, tel)

        # 选择所属行政区域
        self.select_default_area()

        # 填写详细街道地址
        self.input_text(self.DETAIL_INPUT, detail)

        # 提交表单保存地址
        self.click(self.SAVE_BTN)