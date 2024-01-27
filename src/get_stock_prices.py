import requests
from bs4 import BeautifulSoup
import pandas as pd

# Getting the stock price
def get_stock_data():
    try:
        url = 'https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx'
        response = requests.get(url)

    except Exception as e:
        print(e)
        print('No response from the website')
        return None

    if response is None:
        print('No response received')
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    hisse_fiyatlari_tablosu = soup.find('div', class_='single-table')

    data = []

    for row in hisse_fiyatlari_tablosu.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            hisse_adi = cols[0].text.strip()
            fiyat = cols[1].text.strip()
            degisim = cols[2].text.strip()
            hacim_tl = cols[4].text.strip()
            hacim_adet = cols[5].text.strip()
            data.append([hisse_adi, fiyat, degisim, hacim_tl, hacim_adet])

    df = pd.DataFrame(data, columns=['Hisse Adı', 'Fiyat', 'Değişim (%)', 'Hacim(TL)', 'Hacim(Adet)'])
    return df
