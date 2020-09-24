from selenium import webdriver
import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
from keys import email, password

driver = webdriver.Chrome('/Users/generalassembly/Downloads/chromedriver')

# got to wallmine.com
driver.get('https://wallmine.com')

if 'Make Smarter Investments' in driver.page_source:
    signin_link = driver.find_element_by_xpath('/html/body/main/header/div/ul/li[1]/ul/li[3]/a')
    signin_link.click()
    time.sleep(3)
    print('Going to signin page')

if 'Sign in here, please.' in driver.page_source:
    login_email = driver.find_element_by_xpath('//*[@id="user_email"]')
    signin_password = driver.find_element_by_xpath('//*[@id="new_user"]/div[5]/div[1]/div[2]')
    signin_password.click()
    time.sleep(0.2)

login_password = driver.find_element_by_xpath('//*[@id="user_password"]')
signin_button = driver.find_element_by_xpath('//*[@id="new_user"]/div[5]/div[2]/div[1]/button')

login_email.send_keys(email)
login_password.send_keys(password)
signin_button.click()
time.sleep(3)

if 'Stock market overview' in driver.page_source:
    print('On the main page')
    heatmap = driver.find_element_by_xpath('//*[@id="homepage-heatmap"]/a/div[2]')
    heatmap.click()
    time.sleep(3)

overview_tab = driver.find_element_by_xpath('/html/body/main/section/div[5]/div/div/div[1]/div/ul/li[1]/a')
overview_tab.click()
time.sleep(3)

if 'Free Stock Screener' in driver.page_source:
    print('Here')
    stock_data = driver.find_element_by_xpath('/html/body/main/section/div[5]/div/div/div[2]').text

stock_list = stock_data.split('\n')

stock_list[28].split(' $')
company_info_parsed = stock_list[28].split(' $')[0]
market_cap = stock_list[28].split(' $')[1]
market_info = stock_list[28].split(' $')[2]
price_info = stock_list[28].split(' $')[3].split(' ')
price = price_info[0]
performance_today = price_info[1]
company_info = company_info_parsed.split(' ')
if 'NASDAQ' in company_info:
    idx = company_info.index('NASDAQ')
    exchange = company_info[idx]
elif 'NYSE'in company_info:
    idx = company_info.index('NYSE')
    exchange = company_info[idx]
elif 'NYSEMKT' in company_info:
    idx = company_info.index('NYSEMKT')
    exchange = company_info[idx]
industry = " ".join(company_info[idx+1:])
symbol = company_info[0]
company_name = " ".join(company_info[1:idx])
company_name
# currently parsed:
# symbol, company_name, exchange, industry, market_cap, price, performance_today
# ebitda, p_e, ev_ebitda, debt_equity, average_volume, institutional_ownership, earnings_date

# parse market info
ebitda = market_info.split(' ')[0]
p_e = market_info.split(' ')[1]
ev_ebitda = market_info.split(' ')[2]
debt_equity = market_info.split(' ')[3]
average_volume = market_info.split(' ')[4]
institutional_ownership = market_info.split(' ')[5]
earnings_date = " ".join(market_info.split(' ')[6:])
earnings_date

x_stock = {
    "symbol": symbol,
    "company_name": company_name,
    "exchange": exchange,
    "industry": industry,
    "market_cap": market_cap,
    "ebitda": ebitda,
    "p_e": p_e,
    "ev_ebitda": ev_ebitda,
    "debt_equity": debt_equity,
    "average_volume": average_volume,
    "institutional_ownership": institutional_ownership,
    "earnings_date": earnings_date,
    "price": price,
    "performance_today": performance_today
}

all_stocks = stock_list[28:]

index_list = []
final_list = []

for i in range(len(all_stocks)):
    each_stock = all_stocks[i]
    
    if 'NT' in each_stock:
        pass
    elif '¥' in each_stock:
        pass
    elif '€' in each_stock:
        pass
    elif 'kr' in each_stock:
        pass
    else:
        final_list.append(each_stock)

driver.get(f"https://wallmine.com/{x.get('exchange')}/{x.get('symbol')}")

for each_stock in final_list:
    x = parse_stock_data(each_stock)
    driver.get(f"https://wallmine.com/{x.get('exchange')}/{x.get('symbol')}")
    time.sleep(3)
    
    if x.get('symbol') in driver.page_source:
        print(f"We are on {x.get('company_name')}'s stock page")


def parse_stock_data(data):
    company_info_parsed = data.split(' $')[0]
    company_info = company_info_parsed.split(' ')
    if 'NASDAQ' in company_info:
        idx = company_info.index('NASDAQ')
        exchange = company_info[idx]
    elif 'NYSE' in company_info:
        idx = company_info.index('NYSE')
        exchange = company_info[idx]
    elif 'NYSEMKT' in company_info:
        idx = company_info.index('NYSEMKT')
        exchange = company_info[idx]
    industry = " ".join(company_info[idx + 1:])
    symbol = company_info[0]
    company_name = " ".join(company_info[1:idx])
    if 'N/A' in data.split(' $')[1]:
        market_cap_1 = data.split(' $')[1].split(' ')
        market_cap = market_cap_1[0]
        ebitda = market_cap_1[1]
        p_e = market_cap_1[2]
        ev_ebitda = market_cap_1[3]
        debt_equity = market_cap_1[4]
        average_volume = market_cap_1[5]
        institutional_ownership = market_cap_1[6]
        earnings_date = " ".join(market_cap_1[7:])
        price_info = data.split(' $')[2].split(' ')
        price = price_info[0]
        performance_today = price_info[1]
    else:
        market_cap = data.split(' $')[1]
        market_info = data.split(' $')[2]
        ebitda = market_info.split(' ')[0]
        p_e = market_info.split(' ')[1]
        ev_ebitda = market_info.split(' ')[2]
        debt_equity = market_info.split(' ')[3]
        average_volume = market_info.split(' ')[4]
        institutional_ownership = market_info.split(' ')[5]
        earnings_date = " ".join(market_info.split(' ')[6:])
        price_info = data.split(' $')[3].split(' ')
        price = price_info[0]
        performance_today = price_info[1]
    result = {
        "symbol": symbol,
        "company_name": company_name,
        "exchange": exchange,
        "industry": industry,
        "market_cap": market_cap,
        "price": price,
        "performance_today": performance_today,
        "ebitda": ebitda,
        "p_e": p_e,
        "ev_ebitda": ev_ebitda,
        "debt_equity": debt_equity,
        "average_volume": average_volume,
        "institutional_ownership": institutional_ownership, 
        "earnings_date": earnings_date
    }
    return result


final_list = []
for i in range(len(stock_list[28:])):
    each_stock = stock_list[28:][i]
    if 'Intel' in each_stock:
        final_list.append(each_stock)
    elif 'NT' in each_stock:
        pass
    elif '¥' in each_stock:
        pass
    elif '€' in each_stock:
        pass
    elif 'kr' in each_stock:
        pass
    elif 'XETRA' in each_stock:
        pass
    else:
        final_list.append(each_stock)


for each_stock in final_list:
    print(parse_stock_data(each_stock))
    time.sleep(1)
