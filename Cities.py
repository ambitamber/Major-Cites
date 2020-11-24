from bs4 import BeautifulSoup
import requests
import json
from image_application import get_image
import yaml

class NearbyCites:

    def __init__(self):
        config = open("configuration.yaml", "r")
        self.configuration = yaml.safe_load(config)

    def get_data_from_web(self,city,state_or_country):

        url = self.configuration['travelmath']['url'] + city + '+' + state_or_country
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        leftcolumn = soup.find('div', class_='leftcolumn')
        related = leftcolumn.find_all('ul', class_='related')
        #check if related is em not
        if related:
            city_list = []
            for i in related:
                for city in i.find_all('li'):
                    item = city.text
                    city_list.append(item[item.find('to')+3:])

            city_list.pop(0)
            del city_list[9:]

            return city_list
        else:
            print('There is no data for this city.')

    def get_country_data(self,city_list,country):
        for i in range(len(city_list) - 1, -1, -1):
            if country not in city_list[i]:
                print('Removing: ' + city_list[i])
                del city_list[i]
        return city_list

    def get_US_data(self,city_list):
        for i in range(len(city_list) - 1, -1, -1):
            if "Canada" in city_list[i] or "Mexico" in city_list[i]:
                del city_list[i]
        return city_list

    def Cities(self,city,state,country):
        print('Getting data for following location: City = ' + city + "State =" + state + "Country =" + country )
        try:
            if country == "United States":
                city_list = self.get_data_from_web(city,state)
                data = self.get_US_data(city_list)
            else:
                city_list = self.get_data_from_web(city,country)
                data = self.get_country_data(city_list,country)
                
                
            json_string = []
            city_id = 1
            for i in data:
                image = get_image(i[:i.find(', ')],i[i.find(', ')+2:]).download_image()
                json_string.append({'city_ID':city_id,'cityName':i,'Image_url':image})
                city_id += 1
                
            output = json.dumps(json_string)
        except:
            print('Error getting data.')
            output = {'No data'}
            
        return output
            