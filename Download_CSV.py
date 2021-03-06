# import lib
from requests import get
from bs4 import BeautifulSoup
import re
import json


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