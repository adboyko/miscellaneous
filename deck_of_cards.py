import requests
from pprint import pprint as pp


def main():
    deck_url = 'https://deckofcardsapi.com/api/deck'
    d_of_c = requests.get(
        f'{deck_url}/new/shuffle/?deck_count=1'
    )
    deck_id = d_of_c.json()['deck_id']
    draw_5 = requests.get(
        f'{deck_url}/{deck_id}/draw/?count=5'
    )
    pp(draw_5.json())
    trash = requests.get(
        f'{deck_url}/{deck_id}/pile/trash/add/?'
        f'cards='
        f'{",".join([card["code"] for card in draw_5.json()["cards"]])}'
    )
    pp(trash.url)
    trash_contents = requests.get(
        f'{deck_url}/{deck_id}/pile/trash/list/'
    )
    pp(trash_contents.json())


if __name__ == '__main__':
    main()
