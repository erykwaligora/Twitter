# created on Dec 24, 2020
# @author:          Bo Zhao
# @email:           zhaobo@uw.edu
# @website:         https://hgis.uw.edu
# @organization:    Department of Geography, University of Washington, Seattle
# @description:     Search tweets of a specific topic using a web crawler

from selenium import webdriver
from bs4 import BeautifulSoup
import time,  datetime, json

# url = "https://twitter.com/search?l=&q=near%3A%22houston%22%20within%3A15mi%20since%3A2017-08-24%20until%3A2017-08-31&src=typd&lang=en"  #crawlling all the tweets posted near Houston during the Hurricane Harvey attacked period.
url = "https://twitter.com/usa_china_talk/status/993372193777123329"

# use a chrome core. https://chromedriver.chromium.org/downloads
bot = webdriver.Chrome(executable_path="assets/chromedriver") # if you are a mac user, please use "assets/chromedriver"
bot.get(url)


# Read the Xpath tutorial if you are not familiar with XPath.
# "//" operator indicates Selects nodes in the document from the current node that match the selection no matter where they are.
# while len(bot.find_elements_by_xpath('//div[contains(text(), "Back to top")]')) != 1:
s = 2
i = 0
for i in range(s):
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)




with open("assets/tweets.csv", "w", encoding="utf-8") as fp:
    fp.write("id,name,screenname,time,text\n")

    id = 0
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    tweets = soup.find_all('article', {"role": "article"})[1:]# only process the newly-acquired tweets.
    for tweet in tweets:
        try:
            text = tweet.find("div", {"lang": "zh"}).text.replace("\n"," ").replace("\r"," ").replace("\t"," ").replace("'",'"')
            username = tweet.find("div", {"dir":"ltr"}).text
            screenname = tweet.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
            time = tweet.find("time").attrs['datetime']
            fp.write("%d,%s,%s,%s,'%s'\n"%(id, username, screenname, text))
        except:
            pass

        id += 1


bot.close()
print("finished")

id = 0
