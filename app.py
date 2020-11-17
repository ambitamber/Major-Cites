from Cities import NearbyCites
from flask import Flask
from flask import request 

data = NearbyCites().Cities('weymouth','ma','United States')
print(data)