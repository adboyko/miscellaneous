import json
from pprint import pprint as pp


def main():
    sci_name = None
    with open('bdays.json', 'r') as sci_bdays_i:
        bday_dict = json.load(sci_bdays_i)
        for k, v in bday_dict['Birthdays']['Scientists'].items():
            print(f"{k} born on {v}")
        print("-" * 10, "Add another?", sep="\n")
        if input() is 'y':
            print("Who?")
            sci_name = input()
            bday_dict['Birthdays']['Scientists'][sci_name] = ''
            print("What is their bday")
            bday_dict['Birthdays']['Scientists'][sci_name] = input()
    if sci_name:
        print("updating file")
        with open('bdays.json', 'w') as sci_bdays_o:
            json.dump(bday_dict, sci_bdays_o)


if __name__ == '__main__':
    main()
