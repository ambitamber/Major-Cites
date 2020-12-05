import firebase_admin
from firebase_admin import credentials,firestore
import json

class Firestore:

    def __init__(self,keyID):
        self.keyID = keyID
        self.db = self.Firestore_Connection()

    def Firestore_Connection(self):
        filekey = open("key.json",'rb')
        key = json.load(filekey)
        if not firebase_admin._apps:
            cred = credentials.Certificate(key)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db

    def Firestore_Uploader(self,imagelink):
        self.db.collection('Google City Image').document(self.keyID).set({"imagelink":imagelink})
    
    def Exists_In_Firestore(self):
        if self.db.collection('Google City Image').document(self.keyID).get().exists:
            return True
        else:
            return False
    
    def Firestore_Downloader(self):
        collection = self.db.collection('Google City Image').document(self.keyID).get()
        data = collection.to_dict()
        return data['imagelink']
