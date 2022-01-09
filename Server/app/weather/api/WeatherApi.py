import pandas as pd
import json

import pandas as pd
import requests
from lxml import etree


def request_weather_info(areaId:int=None,
                         startDate:datetime=datetime.datetime.today, 
                         endDate:datetime=datetime.datetime.today,
                         df=True):
    """[summary]

    Args:
        areaId (int, optional): [description]. Defaults to None.
        startDate (datetime, optional): [description]. Defaults to None.
        endDate (datetime, optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    # 请求url
    url = 'http://tianqi.2345.com/Pc/GetHistory'
    # 设置请求头，可选
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }

    start_year = startDate.year
    start_month = startDate.month
    
    end_year = endDate.year
    end_month = endDate.month
    
    # 结果集
    result = []
    today = datetime.datetime.today()
    current_year = today.year
    current_month = today.month
    # 循环请求数据
    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            if year == start_year and month < start_month:
                continue
            if year==current_year and month> current_month:
                continue
            if year == end_year and month > end_month:
                break
            else:
                # 设置请求参数
                params = {'areaInfo[areaId]': areaId, 'areaInfo[areaType]': 2, 'date[year]': year, 'date[month]': month}
                # 发送get请求
                response = requests.get(url, params=params, headers=headers)
                # 获取请求数据，因为响应结果是json字符串，需要先转换为字典数据结构
                response_data = json.loads(response.content.decode())
                # json.load()
                # 获取天气数据体，之前有分析过
                data = response_data.get('data')
                # 使用lxml中的etree模块将天气数据转换成html树
                html = etree.HTML(data)
                # 使用xpath语法解析数据
                weather_info = html.xpath('//table/tr[position()>1]')
                for item in weather_info:
                    single_day_weather = []
                    # 日期
                    date = item.xpath('./td[1]/text()')[0].split(' ')[0]
                    # 最高温度
                    max_temperature = item.xpath('./td[2]/text()')[0].replace('°', '')
                    # 最低温度
                    min_temperature = item.xpath('./td[3]/text()')[0].replace('°', '')
                    # 天气
                    weather = item.xpath('./td[4]/text()')[0]
                    # 风力
                    wind_power = item.xpath('./td[5]/text()')[0]
                    # 空气质量，测试中发现，有些地方某月份的空气质量数据不存在，会抛出异常，这里捕捉一下，如果不存在就置为空
                    air_quality = ''
                    try:
                        air_quality = item.xpath('./td[6]/span[1]/text()')[0]
                    except:
                        air_quality = ''
                        # print(date)
                        # print(year, month, city_info)
                        # print(air_quality)
                        # print(type(air_quality))
                    single_day_weather.append(date)
                    single_day_weather.append(max_temperature)
                    single_day_weather.append(min_temperature)
                    single_day_weather.append(weather)
                    single_day_weather.append(wind_power)
                    single_day_weather.append(air_quality)
                    result.append(single_day_weather)
    if df == True:
        return pd.DataFrame(result, columns=['日期', '最高温度°', '最低温度°', '天气', '风力风向', '空气质量']).to_json(orient = 'records')
    else:
        return result