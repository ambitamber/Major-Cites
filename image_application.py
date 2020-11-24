import requests
import urllib.parse
import random
import yaml

class get_image:

    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

        configuration = open("configuration.yaml", "r")
        self.configuration = yaml.safe_load(configuration)
    
    def download_image(self):
        query = self.p1 + "+" + self.p2 
        fields = 'photos'
        inputtype = 'textquery'

        getparams = {'input':query, 'inputtype':inputtype, 'fields':fields,'key':self.configuration['googleapis']['key']}
        url = self.configuration['googleapis']['url'] + urllib.parse.urlencode(getparams)
        response = requests.get(url)
        jsondata = response.json()

        image_id_list = []
        for photos in jsondata['candidates']:
            for photo in photos['photos']:
                image_id_list.append(photo['photo_reference'])
        
        if len(image_id_list) == 1:
            image_url = self.build_image_link(image_id_list[0])
            return image_url
        elif len(image_id_list) > 1:
            image_url = self.build_image_link(random.choice(image_id_list))
            return image_url
    
    def build_image_link(self,image_id):
        image_url = self.configuration['googleapis']['photo_url']
        maxwidth = '400'

        getparams = {'maxwidth': maxwidth, 'photoreference':image_id, 'key':self.configuration['googleapis']['key']}
        imageurl = image_url +  urllib.parse.urlencode(getparams)

        return imageurl
