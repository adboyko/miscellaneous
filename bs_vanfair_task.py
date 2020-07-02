import requests
from bs4 import BeautifulSoup


def main():
    vanfair = BeautifulSoup(
        requests.get(
            'http://www.vanityfair.com/society/2014/06/'
            'monica-lewinsky-humiliation-culture'
        ).text, 'html.parser')
    for chunk in vanfair.select('div.article__chunks p'):
        print(str(chunk.contents[-1]))
    return


if __name__ == '__main__':
    main()
