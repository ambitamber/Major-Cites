import requests
import urllib.parse
import random
import yaml
import firebase_admin
from firebase_admin import credentials,firestore
import json


class get_image:

    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

        configuration = open("configuration.yaml", "r")
        self.configuration = yaml.safe_load(configuration)
    
    def Get_Image_Link(self):
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
    
    def Build_Image_Link(self,image_id):
        image_url = self.configuration['googleapis']['photo_url']
        maxwidth = '400'

        getparams = {'maxwidth': maxwidth, 'photoreference':image_id, 'key':self.configuration['googleapis']['key']}
        imageurl = image_url +  urllib.parse.urlencode(getparams)

        return imageurl


    def Save_to_Firestore(self,cityname,image_url):
        cred = credentials.Certificate('path/to/serviceAccount.json')
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        doc_ref = db.collection(u'users').document(u'alovelace')
        doc_ref.set({
            u'first': u'Ada',
            u'last': u'Lovelace',
            u'born': 1815
        })

    def _Check(self):
        listnum = []
        for char in self.p1+self.p2.lower():
            listnum.append(str(ord(char)))
        
        db = self.Firestore_Connection()
        keyID = self.p1 + self.p2 + ":" + '-'.join(listnum)
        if db.collection('Google City Image').document(keyID).get().exists:
            return
    
    def Firestore_Connection(self):
        filekey = open("key.json",'rb')
        key = json.load(filekey)
        if not firebase_admin._apps:
            cred = credentials.Certificate(key)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db

