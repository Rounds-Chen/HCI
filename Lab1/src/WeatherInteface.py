import requests
from bs4 import  BeautifulSoup
import time
import re

"""
1. 获取城市编号，拼接成url
2. 查找res中对应的信息，提取有用信息后返回
"""

class CheckWeather():
    def __init__(self,city) -> None:
        self.city=city

    # 获取城市的编号
    def city_code(self):
        url="http://toy1.weather.com.cn/search?cityname={}&callback=success_jsonpCallback&_=1619622006461".format(self.city)
        res=requests.get(url).text
        _begin=r'success_jsonpCallback(['
        _end=r'])'
        res=res[len(_begin):-len(_end)]
        code=re.match('.*?:"(\d+).*',res).group(1)
        return code



    # 获取城市的天气信息
    def weather(self):
        code=self.city_code()
        url="http://www.weather.com.cn/weather/{}.shtml".format(code)

        res=requests.get(url)
        res.raise_for_status()
        res.encoding=res.apparent_encoding
        soup=BeautifulSoup(res.text,"html.parser")
        d7_lists = soup.select('div .c7d ')[0].select('ul > li')

        # 获取7天的日期，天气，最高温度，最低温度
        dates,weathers,highs,lows=[],[],[],[]
        temps=[]
        # 风向，风级
        wind_scale,wind_level=[],[]
        for item in d7_lists[:7]:
            dates.append(item.h1.string)
            weathers.append(item.p['title'])

            tem=item.find('p', class_="tem")
            highs.append(tem.span.string if tem.span else "" )
            lows.append(tem.i.string)

            temps.append(tem.text)

            win=item.find('p',class_="win")
            scales=win.select('em > span')
            if len(scales)==1:
                wind_scale.append(scales[0]["title"])
            else:
                f=[i["title"] for i in scales]
                if f[0]==f[1]:
                    wind_scale.append(f[0])
                else:
                    wind_scale.append('{0}转{1}'.format(f[0],f[1]))
            wind_level.append(win.i.string)
        ans1="{}月{}\n{}\n{}\n".format(str(time.localtime().tm_mon),dates[0],' '*4+weathers[0],' '*4+'~'+lows[0])
        ans2="{}月{}\n{}\n{}".format(str(time.localtime().tm_mon),dates[1],' '*4+weathers[1],' '*2+highs[1]+'~'+lows[0])
        print(ans1+ans2)
        return ans1+ans2



if __name__=="__main__":
    c=CheckWeather("上海")
    c.weather()


