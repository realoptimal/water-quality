#!/usr/bin/env python

import unittest

from wq_app import db, app
from wq_app.framework.models import *

class TestSampleModel(unittest.TestCase):
    def setUp(self):
        # db.session.close()
        # db.drop_all()
        # db.create_all()
        pass
    
    def test_get_sample_factor(self):
        sample2 = Sample.query.get(2)
        factor_val = sample2.factor(1)
        self.assertEqual(factor_val, 0.024007)

    def tearDown(self):
        pass
