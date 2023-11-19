#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

# from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
# from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
# import json
# import os
import pycodestyle
import unittest
DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pycodestyle_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conform to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_doc_string(self):
        """ tests docstrings for module, class, & class methods """
        self.assertTrue(len(DBStorage.__doc__) > 0)
        self.assertTrue(len(DBStorage.all.__doc__) > 0)
        self.assertTrue(len(DBStorage.new.__doc__) > 0)
        self.assertTrue(len(DBStorage.save.__doc__) > 0)
        self.assertTrue(len(DBStorage.reload.__doc__) > 0)
        self.assertTrue(len(DBStorage.delete.__doc__) > 0)
        self.assertTrue(len(DBStorage.get.__doc__) > 0)
        self.assertTrue(len(DBStorage.count.__doc__) > 0)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get properly retrieves expected key"""
        obj = User(
            first_name='James',
            last_name='Franco',
            email='test@test.com',
            password='pwd'
        )
        models.storage.new(obj)
        models.storage.save()
        grab = models.storage.get(User, obj.id)
        self.assertEqual(grab, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count properly retrieves number of requested objects"""
        count1 = models.storage.count()
        user_count1 = models.storage.count(User)
        obj1 = User(
            first_name='James',
            last_name='Franco',
            email='test@test.com',
            password='pwd'
        )
        models.storage.new(obj1)
        models.storage.save()
        count2 = models.storage.count()
        user_count2 = models.storage.count(User)
        self.assertTrue(type(count1) is int)
        self.assertTrue(type(user_count1) is int)
        self.assertTrue(type(count2) is int)
        self.assertTrue(type(user_count2) is int)
        self.assertGreater(count2, count1)
        self.assertGreater(user_count2, user_count1)
        obj2 = User(
            first_name='Vin',
            last_name='Diesel',
            email='test@test1.com',
            password='pwd1'
        )
        models.storage.new(obj2)
        models.storage.save()
        count3 = models.storage.count()
        user_count3 = models.storage.count(User)
        self.assertEqual(len(models.storage.all()), count3)
        self.assertEqual(len(models.storage.all(User)), user_count3)
        self.assertTrue(type(count2) is int)
        self.assertTrue(type(user_count2) is int)
        self.assertTrue(type(count3) is int)
        self.assertTrue(type(user_count3) is int)
        self.assertGreater(count3, count2)
        self.assertGreater(user_count3, user_count2)
        models.storage.delete(obj2)
        count4 = models.storage.count()
        user_count4 = models.storage.count(User)
        self.assertTrue(type(count4) is int)
        self.assertTrue(type(user_count4) is int)
        self.assertEqual(count4, count2)
        self.assertEqual(user_count4, user_count2)
        self.assertLess(count4, count3)
        self.assertLess(user_count4, user_count3)
        models.storage.delete(obj1)
        count5 = models.storage.count()
        user_count5 = models.storage.count(User)
        self.assertTrue(type(count5) is int)
        self.assertTrue(type(user_count5) is int)
        self.assertEqual(count5, count1)
        self.assertEqual(user_count5, user_count1)
        self.assertLess(count5, count4)
        self.assertLess(user_count5, user_count4)
