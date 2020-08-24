import json
import urllib
import requests
import os
import base64
import re
import shutil
import csv
import uuid
import math
import boto3
import pymongo
import lxml as lh
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
#from firebase_admin import firestore
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.son import SON
import pandas as pd

#db = firestore.Client()
#cred = credentials.Certificate('serviceAccountKey.json')
#firebase_admin.initialize_app(cred)