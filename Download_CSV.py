# import lib
from requests import get


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