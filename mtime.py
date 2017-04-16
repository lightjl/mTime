from lxml import etree
import requests
import calendar
import sendMail
import time
import datetime

def checkToday():  #
    url = 'http://movie.mtime.com/recent/#hottest'
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class="movietopmod"]')
    num = 20
    for each in content_field:

        syrq = each.xpath('div[@class="txtbox"]/p[@class="showday"]//text()')[0]
        #dq = each.xpath('//p[contains(text(),"国家地区：")]/a/text()')[0]
        dq = each.xpath('div[@class="txtbox"]/p[3]/a/text()')[0]
        #print(each.xpath('div[@class="txtbox"]/h3//text()')[0])
        #print(dq)
        sydq = syrq.split(' ')[1].split('(')[1].split(')')[0]
        syrq = syrq.split(' ')[1].split('(')[0]
        if (sydq) != '中国':
            continue
        if syrq[-1] == '年' or syrq[-1] == '月':
            continue
        '''
        print(syrq)
        print(dq)
        print(each.xpath('div[@class="txtbox"]/h3//text()')[0])
        '''
        t = (time.strptime(syrq, '%Y年%m月%d日'))
        day_time = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        while day_time.weekday() != calendar.SATURDAY:
            day_time += oneday
        withinAWeek = day_time.timetuple()
        if t <= withinAWeek and dq != '中国':
            jqUrl = each.xpath('div[@class="txtbox"]/h3//@href')[0]
            jqHtml = requests.get(jqUrl + '/plots.html')
            print(jqUrl + '/plots.html')
            jqSelector = etree.HTML(jqHtml.text)
            jqDivs = jqSelector.xpath('//div[@id="paragraphRegion"]/div/div')

            jqText = ''
            for txt in jqDivs[1:]:
                texts = (txt.xpath('div[2]/p'))
                for textP in texts:
                    txt = textP.xpath('string(.)')
                    jqText += txt + '\n'
                    #print(txt)
            dym = each.xpath('div[@class="txtbox"]/h3//text()')[0]
            print(dym)
            print(jqUrl)
            print(jqText)
            print(syrq)
            sentTxt = '%s\n上映时间%s\n%s\n' %(jqUrl, syrq, jqText)
            print(sentTxt)
            sendMail.sendMail('电影：'+dym, sentTxt)

        num -= 1
        if num < 0:
            break

checkToday()