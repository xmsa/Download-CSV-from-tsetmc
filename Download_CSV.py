# import lib
from requests import get
from bs4 import BeautifulSoup
import re
import json
import os


class CSVFile:
    @staticmethod
    def __Get_Content(url):
        # User-Agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        # get requests
        response = get(url, headers=headers)
        # get content
        content = response.text
        return content
    
    @staticmethod
    def __Split_Id_Symbol(content):
        soup = BeautifulSoup(content, 'html.parser')
        # select table
        div = soup.findAll('div', attrs={'class': 'content'})
        # split rows
        tr = div[0].find_all('tr')
        _dict = dict()
        for i in tr[1:]:
            # split Columns
            td = i.find_all('td')
            # select symbol Column
            td_6 = td[6]
            # find symbol
            txt = td_6.text
            # find href
            href = td_6.find('a')['href']
            # find id
            _id = re.findall(r'inscode=([\d]+)', href)[0]
            # add symbol and id to dict
            _dict[txt] = _id
        return _dict


    @staticmethod
    def __Save_Json(_dict):
        path = 'data.json'
        # save json
        with open(path, 'w') as fp:
            json.dump(_dict, fp)

    
    @staticmethod
    def __Load_Json():
        path = 'data.json'
        # load json
        with open(path, 'r') as fp:
            _dict = json.load(fp)
        return _dict


    @staticmethod
    def __Download_Symbols():
        # download Symbols(json file)
        # set url
        url = 'http://www.tsetmc.com/Loader.aspx?ParTree=111C1417'
        # Get Content
        content = CSVFile.__Get_Content(url)
        # Split Id and symbol
        _dict = CSVFile.__Split_Id_Symbol(content)
        # Save Json
        CSVFile.__Save_Json(_dict)

    @staticmethod
    def __CSV_Downloader(symbolID, symbol):
        # set url
        url = 'http://www.tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i={}'.format(symbolID)
        print('Downloading CSV...')
        # send requests
        data = get(url)
        print('Save CSV')
        # save csv
        with open('{}.csv'.format(symbol), 'wb') as f:
            f.write(data.content)
        print('Saved CSV {} to {}.csv'.format(symbol, symbol))

    @staticmethod
    def Download_CSV(symbol):
        # check exist json file
        if not os.path.exists('data.json'):
            # Download json file
            CSVFile.__Download_Symbols()
        # load json file
        symbols = CSVFile.__Load_Json()
        # check symbol in symbols(dict)
        if symbol in symbols:
            # Download CSV file
            CSVFile.__CSV_Downloader(symbols[symbol], symbol)
        else:
            print('not find {}'.format(symbol))