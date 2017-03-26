from lxml import etree
import requests
import calendar
import sendMail
import time
import datetime

class xs:
    def __init__(self):
        self.__new = ''

    def update(self, name):
        self.__new = name

    def isNew(self, name):
        return self.__new != name

    def newCharp(self):
        return self.__new

def checkToday(timeWork):  #
    url = 'http://movie.mtime.com/recent/#hottest'
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class="movietopmod"]')
    num = 10
    for each in content_field:

        syrq = each.xpath('div[@class="txtbox"]/p[@class="showday"]//text()')[0]
        dq = each.xpath('div[@class="txtbox"]/p[3]/a/text()')[0]
        #print(each.xpath('div[@class="txtbox"]/h3//text()')[0])
        #print(dq)
        syrq = syrq.split(' ')[1].split('(')[0]
        t = (time.strptime(syrq, '%Y年%m月%d日'))
        day_time = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        while day_time.weekday() != calendar.SATURDAY:
            day_time += oneday
        withinAWeek = day_time.timetuple()
        if t <= withinAWeek and dq != '中国':
            jqUrl = each.xpath('div[@class="txtbox"]/h3//@href')[0]
            jqHtml = requests.get(jqUrl + '/plots.html')
            jqSelector = etree.HTML(jqHtml.text)
            jqTexts = jqSelector.xpath('//div[@id="paragraphRegion"]/div/div')
            print(jqTexts)
            jqText = ''
            for txt in jqTexts[1:]:
                jqText += txt.xpath('div[2]/p[1]/text()')[0] + '\n'
            dym = each.xpath('div[@class="txtbox"]/h3//text()')[0]
            print(dym)
            print(jqUrl)
            print(jqText)
            print(syrq)
            sentTxt = '%s\n上映时间%s\n%s\n' %(jqUrl, syrq, jqText)
            sendMail.sendMail('电影：'+dym, sentTxt)

        num -= 1
        if num < 0:
            break

checkToday(timeWork)