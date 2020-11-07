import re
from bs4 import BeautifulSoup
import requests

city = 'Tours'
state = 'tx'
country = 'France'

def get_data_from_web(city,state_or_country):

    url = 'https://www.travelmath.com/cities-near/'+ city + '+' + state_or_country
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    leftcolumn = soup.find('div', class_='leftcolumn')
    related = leftcolumn.find_all('ul', class_='related')

    city_list = []
    for i in related:
        for city in i.find_all('li'):
            item = city.text
            city_list.append(item[item.find('to')+3:])

    city_list.pop(0)
    del city_list[9:]

    return city_list


def get_coutry_data(city_list,country):
    for i in range(len(city_list) - 1, -1, -1):
        if country not in city_list[i]:
            del city_list[i]
        print('get_coutry_data: ' + str(city_list))
        return city_list

def get_US_data(city_list):
    for i in range(len(city_list) - 1, -1, -1):
        if "Canada" in city_list[i] or "Mexico" in city_list[i]:
            del city_list[i]
    return city_list

def main():
    if country == "United States":
        city_list = get_data_from_web(city,state)
        data = get_US_data(city_list)
    else:
        city_list = get_data_from_web(city,country)
        data = get_coutry_data(city_list,country)
    print(data)

if __name__ == '__main__':
    main()