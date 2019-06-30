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
        chloroform = Contaminant(name='chloroform', description='CHCl3', default_strength=0.001)
        bromoform = Contaminant(name='bromoform', description='CHBr3', default_strength=0.001)
        bromodichloromethane = Contaminant(name='bromodichloromethane', description='CHBrCl2', default_strength=0.001)
        dibromichloromethane = Contaminant(name='dibromichloromethane', description='CHBr2Cl also', default_strength=0.001)
        db.session.add(chloroform)
        db.session.add(bromoform)
        db.session.add(bromodichloromethane)
        db.session.add(dibromichloromethane)
        db.session.commit()
        sample1 = Sample(site='LA Aquaduct Filteration Plant Effluent')
        sample1_chloroform = SampleContaminantConcentration(contaminant=chloroform, concentration=0.00104)
        sample1_bromoform = SampleContaminantConcentration(contaminant=bromoform, concentration=0.00000)
        sample1_bromodichloromethane = SampleContaminantConcentration(contaminant=bromodichloromethane, concentration=0.00149)
        sample1_dibromichloromethane = SampleContaminantConcentration(contaminant=dibromichloromethane, concentration=0.00275)
        sample1_contaminant_concentrations = [sample1_chloroform, sample1_bromoform, sample1_bromodichloromethane, sample1_dibromichloromethane]
        sample1.contaminant_concentrations.extend(sample1_contaminant_concentrations)
        db.session.add(sample1)
        for cc in sample1_contaminant_concentrations:
            db.session.add(cc)
        db.session.commit()
        sample2 = Sample(site='North Hollywood Pump Station (well blend)')
        sample2_chloroform = SampleContaminantConcentration(contaminant=chloroform, concentration=0.00291)
        sample2_bromoform = SampleContaminantConcentration(contaminant=bromoform, concentration=0.00487)
        sample2_bromodichloromethane = SampleContaminantConcentration(contaminant=bromodichloromethane, concentration=0.00547)
        sample2_dibromichloromethane = SampleContaminantConcentration(contaminant=dibromichloromethane, concentration=0.0109)
        sample2_contaminant_concentrations = [sample2_chloroform, sample2_bromoform, sample2_bromodichloromethane, sample2_dibromichloromethane]
        sample2.contaminant_concentrations.extend(sample2_contaminant_concentrations)
        db.session.add(sample2)
        for cc in sample2_contaminant_concentrations:
            db.session.add(cc)
        db.session.commit()
        factor1 = Factor(description='New filtration factor 1')
        factor1_chloroform = FactorContaminantStrength(contaminant=chloroform, strenth=0.8)
        factor1_bromoform = FactorContaminantStrength(contaminant=bromoform, strength=1.2)
        factor1_bromodichloromethane = FactorContaminantStrength(contaminant=bromodichloromethane, strength=1.5)
        factor1_dibromichloromethane = FactorContaminantStrength(contaminant=dibromichloromethane, strength=0.7)
        factor1_contaminant_strengths = [factor1_chloroform, factor1_bromoform, factor1_bromodichloromethane, factor1_dibromichloromethane]
        factor1.contaminant_strengths.extend(factor1_contaminant_strengths)
        db.session.add(factor1)
        for cs in factor1_contaminant_strengths:
            db.session.add(cs)
        db.session.commit()
