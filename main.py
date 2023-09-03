import os
import math
import random
import requests
from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

birthday = os.environ['BIRTHDAY']
app_secret = os.environ['APP_SECRET']
user_id = os.environ['USER_ID']
start_date = os.environ['START_DATE']
city = os.environ['CITY']
app_id = os.environ["APP_ID"]
template_id = os.environ["TEMPLATE_ID"]
weather_url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city

def get_weather():
  res = requests.get(weather_url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  today = datetime.now()
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  today = datetime.now()
  next_birthday = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next_birthday < today:
    next_birthday = next_birthday.replace(year=next_birthday.year + 1)
  return (next_birthday - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
