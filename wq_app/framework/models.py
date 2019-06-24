from wq_app import db

class Contaminant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    default_strength = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Contaminant %r' % self.id


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(80), unique=True, nullable=False)
    contaminant_concentrations = db.relationship('SampleContaminantConcentration',
        backref=db.backref('sample'), 
        lazy=True
    )

    def __repr__(self):
        return '<Sample %r>' % self.id


class SampleContaminantConcentration(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False, primary_key=True)
    contaminant_id = db.Column(db.Integer, db.ForeignKey('contaminant.id'), nullable=False, primary_key=True)
    contaminant = db.relationship('Contaminant', 
        backref=db.backref('sample_contaminant_concentration'), 
        lazy=True, uselist=False
    )
    concentration = db.Column(db.Float, nullable=False)


class Factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    contaminant_strengths = db.relationship('FactorContaminantStrength', 
        backref=db.backref('factor'), lazy=True
    )

    def __repr__(self):
        return '<Factor %r>' % self.id


class FactorContaminantStrength(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factor_id = db.Column(db.Integer, db.ForeignKey('factor.id'), nullable=False)
    contaminant_id = db.Column(db.Integer, db.ForeignKey('contaminant.id'), nullable=False)
    contaminant = db.relationship('Contaminant', 
        backref=db.backref('factor_contaminant_strength'), 
        lazy=True, uselist=False
    )
    strength = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<FactorContaminantStrength %r:%r>' % (self.factor_id, self.contaminant_id)
