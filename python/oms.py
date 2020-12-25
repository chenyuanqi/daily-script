# -*- coding:utf-8 -*-

import os
import time
import datetime
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from urllib.parse import quote


class Oms:
    def __init__(self):
        self.username = os.environ.get('OPPO_USER')
        self.password = os.environ.get('OPPO_PASSWORD')

    def punch(self):
        login_url = 'https://ssov2.myoas.com/sso/user/login?from_url=https://oms.myoas.com'
        # punch_url = 'https://oms.myoas.com/'

        # ChromeDriverManager().install()
        # path = 'C:\\Code\\runner\pyDemo\\vender\\chromedriver.exe'
        # driver = webdriver.Chrome(executable_path=path)
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        driver = webdriver.Chrome()

        try:
            driver.get(login_url)
            time.sleep(3)
            username_input = driver.find_element_by_name('username')
            password_input = driver.find_element_by_name('password')
            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            submit_button = driver.find_element_by_id('submitButton')
            submit_button.click()
            time.sleep(6)

            # 显示等待
            wait = WebDriverWait(driver, 10)
            # 显式等待指定某个条件，然后设置最长等待时间
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sign-div')))
            # 根据 id 查找元素，获取到打卡按钮
            button = driver.find_element_by_id('clerk_btn')
            button.click()

            ft_send('Oms success', 'today oms is success.')
        except OSError:
            print("OSError")
            ft_send('Oms failed', 'today oms is failed, OSError.')
        except NoSuchElementException:
            print("NoSuchElementException~")
            ft_send('Oms failed', 'today oms is failed, NoSuchElementException.')
        except ElementNotInteractableException:
            print("ElementNotInteractableException")
            ft_send('Oms failed', 'today oms is failed, ElementNotInteractableException.')
        finally:
            # 关闭浏览器
            driver.quit()


def ft_send(title, content):
        requests.get('http://sc.ftqq.com/SCU46796T4671f0d85ebce91e2c0ec5ee6b5c022e5c91ecec48d87.send?text=' + quote(title) + '&desp=' + quote(content))


def main():
    switch = "off"
    switch_response = requests.get('http://api.chenyuanqi.com')
    if switch_response.status_code == 200:
        switch = switch_response.json().get("oms", 'off')
    else:
        ft_send('api error', 'warning: oms operate failed.')

    now = datetime.datetime.now()
    # 时间点范围
    duration = [9, 18, 21]
    # 周六日不在范围
    no_week_duration = [5, 6]
    if switch == 'on' and now.hour in duration and now.weekday() not in no_week_duration:
        oms = Oms()
        oms.punch()


if __name__ == '__main__':
    main()

