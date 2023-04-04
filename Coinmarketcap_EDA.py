import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager


# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((3,1))

col1.image('https://cdn.dribbble.com/users/1935365/screenshots/7897428/drebbble_coinmarketcap_4x.jpg')
col2.image('https://s2.coinmarketcap.com/static/cloud/img/splash_600x315_1.png?_=6e911e1')
#---------------------------------#
# Sidebar + Main panel
col1.header('Input Options')

## Sidebar - Currency price unit
# currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

@st.cache_data 
def load_data(force_refresh=False):
    
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    chmod +x chromedriver
    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', chrome_options=chrome_options)
    
    
    
    chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
#     driver = webdriver.Chrome(options=chrome_options)
  
    url ="https://coinmarketcap.com/"
    driver.get(url)
    # Send a GET request to the URL
    response = requests.get(url)
    sleep(2)
    # Use BeautifulSoup to parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    coin_name = []
    coin_symbol = []
    price= []
    one_hour= []
    day= []
    seven_days= []
    market_cap= []
    volume_in_day= []
    volume_coins= []

   
    for i in range(1,101):
        sleep(0.5)
        n = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[3]/div/a/div/div/p[@class ="sc-4984dd93-0 kKpPOn"]').text
        coin_name.append(n)

        s = driver.find_element('xpath',f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[3]/div/a/div/div/div/p').text
        coin_symbol.append(s)

        p = driver.find_element('xpath',f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[4]/div/a/span').text
        price.append(p)
#############################################################################
        h = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[5]/span').text
        number_h = float(h.replace(',', '.').replace('%', ''))

        j = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[5]/span/span')
        class_j = j.get_attribute('class')
        # print(class_j)
        if class_j == 'icon-Caret-up':
            one_hour.append(number_h)
        else:
            one_hour.append(number_h * -1)
###############################################################################
        d = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[6]/span').text
        number_d = float(d.replace(',', '.').replace('%', ''))
        q = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[6]/span/span')
        class_q = q.get_attribute('class')
        if class_q == 'icon-Caret-up':
            day.append(number_d)
        else:
            day.append(number_d*-1)
####################################################################################
        b = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[7]/span').text
        number_b = float(b.replace(',', '.').replace('%', ''))
        p = driver.find_element('xpath', f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[7]/span/span')
        class_p = p.get_attribute('class')
        if class_p == 'icon-Caret-up':
            seven_days.append(number_b)
        else:
            seven_days.append(number_b *-1)
#####################################################################################333

        m =  driver.find_element('xpath',f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[8]/p/span[2]').text
        market_cap.append(m)
    
        v = driver.find_element('xpath',f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[9]/div/a/p').text
        volume_in_day.append(v)

        v_c = driver.find_element('xpath',f'/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[9]/div/div/p').text
        volume_coins.append(v_c)

        # print(i)
        try:
            driver.execute_script(f"window.scrollTo(0, {i}00)")
        except:
            pass

        sleep(1)
   


    driver.quit()

    df =pd.DataFrame({
                'name':coin_name,
                'symbol':coin_symbol,
                'price':price,
                'percent_1h' : one_hour,
                'percent_24h': day,
                'percent_7d':seven_days,
                'Market Cap':market_cap,
                'Volume': volume_in_day,
                'Volume coin': volume_coins
                }, columns = ['name', 'symbol', 'price','percent_1h','percent_24h', 'percent_7d', 'Market Cap','Volume', 'Volume coin'])
    
    return df


df = load_data()

if st.sidebar.button('Refresh data'):
    df = load_data(force_refresh=True)
# st.write(df)


## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['symbol'].isin(selected_coin)) ] # Filtering data
# st.write(df_selected_coin)


## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]
# st.write(df_coins)

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percent_7d',"24h":'percent_24h',"1h":'percent_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)


df_change = pd.concat([df_coins.symbol,df_coins.percent_7d,df_coins.percent_24h, df_coins.percent_1h], axis=1)
df_change = df_change.set_index('symbol')

df_change['positive_percent_7d'] = df_change['percent_7d'] > 0
df_change['positive_percent_24h'] = df_change['percent_24h'] > 0
df_change['positive_percent_1h'] = df_change['percent_1h'] > 0
col2.dataframe(df_change)


col3.subheader('Bar plot of % Price Change')
if col3.button('Show Chart'):
    if percent_timeframe == '7d':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_7d'])
        col3.write('*7 days period*')
        plt.figure(figsize=(2,10))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_7d'].plot(kind='barh', color=df_change.positive_percent_7d.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    elif percent_timeframe == '24h':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_24h'])
        col3.write('*24 hour period*')
        plt.figure(figsize=(2,10))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_24h'].plot(kind='barh', color=df_change.positive_percent_24h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    else:
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_1h'])
        col3.write('*1 hour period*')
        plt.figure(figsize=(2,10))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_1h'].plot(kind='barh', color=df_change.positive_percent_1h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
