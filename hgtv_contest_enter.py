from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


def main():
    urls = [
        'https://www.hgtv.com/sweepstakes/hgtv-smart-home/sweepstakes?'
        'nl=R-HGTV:SH2020_2020-06-01_EnterHGTV&bid=20487513&'
        'c32=9fe32119a60f3f6db9bb338d157f076db0274bc1&'
        'ssid=2018_HGTV_confirmation_API&sni_by=&sni_gn=',
        'https://www.diynetwork.com/hgtv-smart-home?'
        'nl=R-HGTV:SH2020_2020-06-01_EnterDIY&bid=20487513&'
        'c32=9fe32119a60f3f6db9bb338d157f076db0274bc1&'
        'ssid=2018_HGTV_confirmation_API&sni_by=&sni_gn='
    ]
    ffox = webdriver.Firefox(executable_path='drivers/geckodriver.exe')

    for url in urls:
        ffox.get(url)
        assert "HGTV Smart Home 2020" in ffox.title
        iframe_loc = ffox.find_element_by_css_selector(
            'div#mod-engage-sciences-1.o-Capsule iframe').get_attribute('id')
        ffox.switch_to.frame(ffox.find_element_by_xpath(f'//*[@id="{iframe_loc}"]'))
        email_input = ffox.find_element_by_xpath('//*[@id="xReturningUserEmail"]')
        email_input.send_keys("adamnboyko@gmail.com")
        email_input.send_keys(Keys.RETURN)
        sleep(6)
        submit_btn = ffox.find_element_by_css_selector(
            '#xSecondaryForm > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)')
        submit_btn.send_keys(Keys.SPACE)
    sleep(3)
    ffox.close()


if __name__ == '__main__':
    main()
