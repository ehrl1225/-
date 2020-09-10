from bs4 import BeautifulSoup
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.common.exceptions import *
import urllib3.exceptions
import os


# 이상함 어디선가 버그가 발생하는데 이유는 못찾겠고 대부분의 상황에서 작동함
class up3:
    def __init__(self, guild):
        self.soup = None
        self.gname = guild["g_name"]
        self.gserver = guild["g_server"]

    def get(self):
        try:
            if not os.path.isdir("chrome"):
                os.mkdir("chrome")
            os.chdir("chrome")
            file = chromedriver_autoinstaller.install(True)
            os.chdir("..")
            driver = webdriver.Chrome(file)
            url = "maple.gg/guild/%s/%s" % (self.gserver, self.gname)
            url = 'http://' + parse.quote(url)
            driver.get(url)
            xpath = "//*[@id='guild-content']/section/div[1]/div[1]/section/div[2]/div/div[1]/b/a"
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                html = driver.page_source
            driver.quit()
            self.soup = BeautifulSoup(html, 'html.parser')

        except SessionNotCreatedException:
            print("error")
            return -1
        except urllib3.exceptions.ProtocolError:
            print("error")
            return -2
        except TimeoutException:
            print("error")
            return -3
        return 0

    def get_first_one(self):
        data = self.soup.findChildren("div")
        a = []
        for i in data[0].text.split("\n"):
            if i != "":
                a.append(i)
        b = []
        for i in range(len(a)):
            if "마지막 활동일" in a[i]:
                b.append([a[i - 2], a[i - 1], a[i]])
        b = b[3:]
        for i in range(len(b)):
            b[i][1] = b[i][1].split("/")[0]
            b[i][2] = b[i][2].split(": ")[1]
        guild = []
        for i in b:
            guild.append({
                "name": i[0],
                "job": i[1],
                "activity": i[2]
            })

        return guild


if __name__ == "__main__":
    server = ["루나 luna",
              "스카니아 scania",
              "엘리시움 elysium",
              "크로아 croa",
              "오로라 aurora",
              "베라 bera",
              "레드 red",
              "유니온 union",
              "제니스 zenith",
              "이노시스 enosis",
              "아케인 arcane",
              "노바 nova",
              "리부트 reboot",
              "리부트2 reboot2",
              ]
    for i in range(len(server)):
        server[i] = server[i].split(" ")
    kor = []
    eng = []
    for i in server:
        kor.append(i[0])
        eng.append(i[1])
    guild = {}
    a = input("서버")
    if a not in eng:
        if a in kor:
            guild["g_server"] = eng[kor.index(a)]
        else:
            guild["g_server"] = ""
    else:
        guild["g_server"] = a
    guild["g_name"] = input("길드 이름")
    crawl = up3(guild)
    stat = crawl.get()
    if stat == -1:
        print("오류")
    elif stat == -2:
        print("콘솔창 닫지 말아주세요.")
    elif stat == -3:
        print("에러")
    else:
        data = crawl.get_first_one()
        for i in data:
            print("%s %s %s" % (i["name"], i["job"], i["activity"]))
    input()
