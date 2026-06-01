import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        # 实例化浏览器对象
        self.browser = webdriver.Firefox()
        real_server = os.environ.get('REAL_SERVER')
        if real_server:
            self.live_server_url = 'http://' + real_server

    def tearDown(self):
        # 测试结束后退出浏览器
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > 5:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三听说有一个在线待办事项的应用
        # 他去看了这个应用的首页
        self.browser.get(self.live_server_url)

        # 他注意到网页里包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # 应用有一个输入待办事项的文本输入框
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 他在文本输入框中输入了“Buy flowers”
        inputbox.send_keys('Buy flowers')
        # 当他按下回车键后，页面更新了
        # 待办事项列表中显示了一个“1: Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        # 页面中又显示了一个文本输入框
        # 张三输入了“Give a gift to Lisi”
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，待办事项列表中显示了一个这两个待办事项
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')

        # 张三想知道这个网站是否会记住他的请对
        # 他看到网站为他生成了一个URL
        # 他访问那个URL，发现他的待办事项列表还在
        # 他满意的离开了
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 张三开始了一个新清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        # 他看到他的待办事项列表有一个URL
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+')

        # 现在应该新用户王五访问网站
        # 我们使用一个新浏览器会话
        # 确保张三的信息不会被携带过来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 王五访问首页，页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy milk', page_text)
        self.assertNotIn('Make tea', page_text)

        # 王五输入一个新事项
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Make tea')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Make tea')

        # 王五获得了他的唯一URL
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)

        # 这个页面还是没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy milk', page_text)
        self.assertNotIn('Make tea', page_text)
