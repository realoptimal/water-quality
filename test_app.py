#!/usr/bin/env python

import unittest

from wq_app import db, app
from wq_app.framework.models import *

class TestSampleModel(unittest.TestCase):
    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        # add in some illustrative data
        
