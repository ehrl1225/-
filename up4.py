from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse


class up4:

    def get_guild(self, name):
        url = "maple.gg/u/%s" % name
        url = 'http://' + parse.quote(url)
        res = req.urlopen(url).read()
        soup = BeautifulSoup(res, 'html.parser')

        notice = soup.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div "
            "> div > div > h1")
        if notice:
            return notice[0].text.split("\n")[0]
        elif not notice:
            return "?"
        else:
            return None

if __name__ =="__main__":
    crawl = up4()
    print(crawl.get_guild(input("닉네임")))
    input()
