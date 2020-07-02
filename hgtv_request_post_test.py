import requests
import bs4


url = 'https://www.hgtv.com/sweepstakes/hgtv-smart-home/sweepstakes?' \
      'nl=R-HGTV:SH2020_2020-06-01_EnterHGTV&bid=20487513&' \
      'c32=9fe32119a60f3f6db9bb338d157f076db0274bc1&' \
      'ssid=2018_HGTV_confirmation_API&sni_by=&sni_gn='
email = 'adamnboyko@gmail.com'
hgtv = requests.get(url)
hgtv = bs4.BeautifulSoup(hgtv.text, 'html.parser')
hgtv_form = hgtv.find(id='xReturningUserEmail')
print(hgtv)
