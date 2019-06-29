from wq_app import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

class Contaminant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    default_strength = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Contaminant %r>' % self.id


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(80), unique=True, nullable=False)
    contaminant_concentrations = db.relationship('SampleContaminantConcentration',
        backref=db.backref('sample'), 
        lazy=True
    )

    @hybrid_method
    def to_hash(self, include_factors=False):
        sample_hash = {
            'id': self.id, 
            'site': self.site,
            'contaminant_concentrations': [{'contaminant_id': c.contaminant_id, 'contaminant_name': c.contaminant.name, 'concentration': c.concentration} for c in self.contaminant_concentrations]
        }
        if include_factors:
            # insert factors into dict for factor each factor
            all_factors = Factor.query.all()
            sample_hash['factors'] = [{'factor_id': f.id, 'description': f.description, 'value': self.factor(f.id)} for f in all_factors] 
        return sample_hash         

    @hybrid_method
    def factor(self, factor_id):
        factor = Factor.query.get(factor_id)
        retval = 0.0
        for fcs in factor.contaminant_strengths:
            scc = SampleContaminantConcentration.query.filter_by(sample_id=self.id, contaminant_id=fcs.contaminant_id).first()
            retval += fcs.strength*scc.concentration
        return retval

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

    def __repr__(self):
        return '<SampleContaminantConcentration %r:%r>' % (self.sample_id, self.contaminant_id)


class Factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    contaminant_strengths = db.relationship('FactorContaminantStrength', 
        backref=db.backref('factor'), lazy=True
    )

    def __repr__(self):
        return '<Factor %r>' % self.id


class FactorContaminantStrength(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    factor_id = db.Column(db.Integer, db.ForeignKey('factor.id'), nullable=False, primary_key=True)
    contaminant_id = db.Column(db.Integer, db.ForeignKey('contaminant.id'), nullable=False, primary_key=True)
    contaminant = db.relationship('Contaminant', 
        backref=db.backref('factor_contaminant_strength'), 
        lazy=True, uselist=False
    )
    strength = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<FactorContaminantStrength %r:%r>' % (self.factor_id, self.contaminant_id)
