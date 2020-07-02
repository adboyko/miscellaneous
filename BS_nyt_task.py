import requests
from bs4 import BeautifulSoup as bs


def main():
    nyt = bs(requests.get('https://www.nytimes.com/').text, 'html.parser')
    for headline in nyt.select('#site-content > div.css-189d5rw.e6b6cmu0 > div.css-698um9 > div h2'):
        try:
            if isinstance(headline.contents[-1], str) and str(headline.contents[-1]).strip(' '):
                print('-', headline.contents[-1])
            elif isinstance(headline.contents[-1].contents, list):
                print('-', headline.contents[-1].contents[-1])
        except AttributeError:
            continue


if __name__ == '__main__':
    main()
