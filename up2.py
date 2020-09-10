from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.common.exceptions import *
import urllib3.exceptions
import os


class up2:

    def __init__(self, guild):
        self.g_account_type = guild["g_account_type"]
        self.g_account = guild["g_account"]
        self.g_password = guild["g_password"]
        self.soup = None

    def get(self):
        try:
            if not os.path.isdir("chrome"):
                os.mkdir("chrome")
            os.chdir("chrome")
            file = chromedriver_autoinstaller.install(True)
            os.chdir("..")
            driver = webdriver.Chrome(file)
            driver.get("https://maplestory.nexon.com/Authentication/Login#a")
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'eid'))
                )

            finally:
                if self.g_account_type == 0:
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.ID, 'eid'))
                        )

                    finally:
                        element.send_keys(self.g_account)
                        element = driver.find_element_by_id("epw")
                        element.send_keys(self.g_password)

                elif self.guild:
                    xpath = "//*[@id='wrap']/div[3]/div/div[1]/ul/li[2]/a/img"
                    driver.find_element_by_xpath(xpath).click()
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.ID, 'mid'))
                        )

                    finally:
                        element.send_keys(self.g_account)
                        element = driver.find_element_by_id("mpw")
                        element.send_keys(self.g_password)

            xpath = "//*[@id='wrap']/div[3]/div/div[2]/div[3]/a/img"
            driver.find_element_by_xpath(xpath).click()
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="gnbMyInfo"]/a/span[1]'))
                )
            except TimeoutException:
                driver.quit()
                return -3

            if driver.current_url == "https://maplestory.nexon.com/Authentication/Login#a":
                driver.quit()
                return -3
            else:
                driver.get("https://maplestory.nexon.com/MyMaple/Profile")

            xpath = "//*[@id='container']/div/div/div/div[1]/div[2]/a/img"
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                driver.find_element_by_xpath(xpath).click()
            try:
                driver.switch_to.window(driver.window_handles[1])

            except:
                if driver.current_url == "https://maplestory.nexon.com/MyMaple/Profile":
                    driver.quit()
                    return -4

            xpath = "//*[@id='wrap']/div[2]/div[1]/span[1]/a/img"
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                driver.find_element_by_xpath(xpath).click()

            xpath = "//*[@id='container']/div[2]/div[2]/div/div[1]/ul/li[2]/a/img"
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                driver.find_element_by_xpath(xpath).click()
            xpath = "//*[@id='container']/div[2]/div[2]/div/div[2]/div[1]/ul/li[4]/a/img"
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                html = driver.page_source

            driver.quit()
            self.soup = BeautifulSoup(html, 'html.parser')
        except SessionNotCreatedException:
            return -1
        except urllib3.exceptions.ProtocolError:
            return -2
        except WebDriverException:
            return -1
        return 0

    def get_guild(self):
        notice = self.soup.findChildren("ul")
        a = []
        if notice is not None:
            guild = []
            for i in notice[-1].text.split("\n"):
                if i != "":
                    a.append(i)
            for i in range(len(a)):
                if i % 2 == 1:
                    a[i] = a[i].split("기여도 ")[1]
            for i in range(int(len(a) / 2)):
                guild.append({
                    "name": a[i * 2],
                    "contribution": a[i * 2 + 1]
                })
        return guild


if __name__ == "__main__":
    guild = {}
    guild["g_account_type"] = int(input("넥슨계정이면 0\n 메이플 계정이면 1"))
    guild["g_account"] = input("계정 아이디")
    guild["g_password"] = input("계정 비밀번호")
    crawl = up2(guild)
    stat = crawl.get()
    if stat == -1:
        print("오류")
    elif stat == -2:
        print("오류2")
    elif stat == -3:
        print("로그인 실패")
    elif stat == -4:
        print("대표 캐릭터 변경해주세요.")
    else:
        data = crawl.get_guild()
        for i in data:
            print("%s %s" % (i["name"], i["contribution"]))
    input()
