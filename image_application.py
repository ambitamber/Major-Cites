import requests
import urllib.parse
import random

class get_image:

    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.key = ''

    def download_image(self):
        query = self.p1 + "+" + self.p2 
        fields = 'photos'
        inputtype = 'textquery'
        main_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'

        getparams = {'input':query, 'inputtype':inputtype, 'fields':fields,'key':self.key}
        url = main_url + urllib.parse.urlencode(getparams)
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
        image_url = 'https://maps.googleapis.com/maps/api/place/photo?'
        maxwidth = '400'

        getparams = {'maxwidth': maxwidth, 'photoreference':image_id, 'key':self.key}
        imageurl = image_url +  urllib.parse.urlencode(getparams)

        return imageurl
