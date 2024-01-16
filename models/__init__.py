""" This model creates a unique file storage instance for our application
"""
from models.engine.file_storage import FileStorage
from models.engine.file_storage import DBStorage
from os import getenv

storageType = getenv('HBNB_TYPE_STORAGE')
if storageType == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
