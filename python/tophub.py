# -*- coding:utf-8 -*-

from selenium import webdriver
import chromedriver_binary
import time


class TopHub:
    def __init__(self):
        self.url = 'https://tophub.today/'

    def watch_by_minutes(self, minutes):
        # chrome_path = r'C:\Code\runner\pyDemo\vender\chromedriver.exe'
        # chrome_driver = webdriver.Chrome(chrome_path)
        chrome_driver = webdriver.Chrome()
        try:
            chrome_driver.get(self.url)
            chrome_driver.maximize_window()
            time.sleep(minutes * 60)
        except ValueError as err:
            print('Handling value error:', err)
        finally:
            # 关闭浏览器
            chrome_driver.close()


def main():
    options = ['3 minutes', '10 minutes']
    print("Please choose:")
    for index, option in enumerate(options):
        print("{}) {}".format(index + 1, option))

    mode = input('Enter number：')
    minutes = 10 if mode == 2 else 3
    print('You can relax for {} minutes'.format(minutes))
    top_hub = TopHub()
    top_hub.watch_by_minutes(minutes)


if __name__ == '__main__':
    main()


