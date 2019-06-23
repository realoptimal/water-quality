from wq_app.framework import db

class Contaminant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contaminant_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Contaminant %r' % self.id


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(80), unique=True, nullable=False)
    contaminant_concentrations = db.relationship('SampleContaminantConcentration',
        backref=db.backref('water_sample'), lazy=True
    )

    def __repr__(self):
        return '<Sample %r>' % self.id


class SampleContaminantConcentration(db.Model):
    contaminant_id = db.Column(db.Integer, db.ForeignKey('contaminant.id'))
    contaminant = db.relationship('Contaminant', 
        backref=db.backref('contaminant'), lazy=True
    )
    concentration = db.Column(db.Float, nullable=False)


class Factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    contaminant_strengths = db.relationship('FactorContaminantStrength', 
        backref=db.backref('factor_set'), lazy=True
    )

    def __repr__(self):
        return '<Factor %r>' % self.id


class FactorContaminantStrength(db.Model):
    factor_id = db.Column(db.Integer, db.ForeignKey('factor.id'))
    contaminant_id = db.Column(db.Integer, db.ForeignKey('contaminant.id'))
    contaminant = db.relationship('Contaminant', 
        backref=db.backref('contaminant'), lazy=True
    )
    strength = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<FactorContaminantStrength %r:%r>' % (self.factor_id, self.contaminant_id)
