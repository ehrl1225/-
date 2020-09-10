from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse


class up1:

    def __init__(self, guild):
        self.guild_id = guild["g_id"]
        self.guild_wid = guild["g_wid"]
        self.soup = None

    def get_guild_one(self, num):
        page = num
        url = "https://maplestory.nexon.com/Common/Guild?gid=%d&wid=%d&orderby=1&page=%d"
        res = req.urlopen(url % (self.guild_id, self.guild_wid, page)).read()
        self.soup = BeautifulSoup(res, 'html.parser')
        a = []
        p = self.soup.findChildren("td")
        if p != None:
            for i in range(len(p)):
                if (i % 5) == 1:
                    a.append(p[i].text.strip("\n").split("\n")[0])
                if (i % 5) == 2:
                    a.append(p[i].text.strip("\n"))
            guild = []
            for i in range(int(len(a) / 2)):
                guild.append({
                    "name": a[i * 2],
                    "level": a[i * 2 + 1]
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
    a = input("길드")
    guild["g_name"] = a
    if guild["g_server"] != "":
        url = "maple.gg/guild/%s/%s" % (guild["g_server"], guild["g_name"])
        url = 'http://' + parse.quote(url)
        res = req.urlopen(url).read()
        soup = BeautifulSoup(res, 'html.parser')
        b = soup.select_one(
            "#app > div.card.mt-0 > div.card-header.guild-header > section > div.row.mb-4 > div.col-lg-8 > div "
            "> div:nth-child(1) > span > a")
        if b:
            guild["g_master"] = b.text
            url = "%s" % guild["g_name"]
            url = 'https://maplestory.nexon.com/Ranking/World/Guild?t=1&n=' + parse.quote(url)
            res = req.urlopen(url).read()
            soup = BeautifulSoup(res, 'html.parser')
            data = "1"
            count = 1
            while data:
                data = soup.select_one(
                    "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > "
                    "td:nth-child(4) > a > span" % count)
                if data.text == guild["g_master"]:
                    break
                count += 1

            if data != None:
                data2 = soup.select_one(
                    "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > "
                    "td:nth-child(2) > span > a" % count)
                guild_data = data2['href'].strip('/Common/Guild?gid=')
                for i in range(len(guild_data)):
                    if guild_data[i] == "&":
                        guild["g_id"] = int(guild_data[:i])
                        guild["g_wid"] = int(guild_data[i:].split("=")[-1])
                        break
            else:
                print("길드가 없습니다.")
        else:
            print("서버나 길드 이름 다시 확인해 주세요")
    else:
        print("서버가 없습니다.")
    new = []
    crawl = up1(guild)
    data = '1'
    count = 1
    while data:
        data = crawl.get_guild_one(count)
        if data is not None:
            for i in data:
                new.append(i)
        count += 1

    if new:
        g_po_name = ["길드마스터", "부마스터", "길드원1", "길드원2", "길드원3"]
        new[0]["position"] = "길드마스터"
        new[1]["position"] = "부마스터"
        lv = new[1]["level"]
        count = 1
        po = [1, 1, 0, 0, 0]
        for i in new[2:]:
            if lv < i["level"]:
                count += 1
            else:
                po[count] += 1
            i["position"] = g_po_name[count]
            lv = i["level"]
        if 0 in po:
            for i in new:
                print("%s %s" % (i["name"], i["level"]))
        else:
            for i in new:
                print("%s %s %s" % (i["name"], i["level"], i["position"]))
    input()
