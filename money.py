import requests
from bs4 import BeautifulSoup
import re

def currency_rate(country):
    response = requests.get(
        "https://rate.bot.com.tw/xrt?Lang=zh-TW")\

    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup.prettify())

    result = soup.find_all("div", class_="visible-phone print_hide")
    currency = []
    for r in result:
        text = re.sub(r"[^a-zA-Z0-9]","",r.getText())
        currency.append(text)

    #print(currency)
    result = soup.find_all("td", class_="rate-content-cash text-right print_hide")
    rate = []
    count = 1
    for r in result:
        if count % 2 != 0:
            rate.append((r.getText()))
        count += 1

    currency_rate = {}
    for i in range(len(rate)):
        currency_rate [currency[i]] = rate[i]

    #print(currency_rate)
    return currency_rate[country]


def calculate(input, country, rate):
    if rate == '-':
        return '抱歉目前沒有提供該匯率的換算!'
    
    return f'{input} NTD 等於 {round(float(input) / float(rate), 2)} {country}'


#s = calculate(1000, 'USD', currency_rate('USD'))
#print(currency_rate('USD'))