from datetime import datetime, date
import dateutil.parser

from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy

# database model
db = SQLAlchemy()


class RiskTypeDefinition(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)

    # name of risk type
    name = db.Column(db.String, nullable=False)

    fields = db.relationship('RiskTypeField')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'fields': [x.serialize for x in self.fields]
        }


class RiskTypeField(db.Model):
    __tablename__ = 'fields'

    id = db.Column(db.Integer, primary_key=True)

    # Risk type definition id to which this field definition belongs
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))

    # Field name
    name = db.Column(db.String, nullable=False)

    # Field data type (text, number, date, enum)
    datatype = db.Column(db.String, nullable=False)

    # comma delimited list of options for enumerable fields
    options = db.Column(db.String, nullable=True)

    type = db.relationship("RiskTypeDefinition", uselist=False)

    @property
    def serialize(self):
        options = []
        if isinstance(self.options, str):
            options = self.options.split(',')
        return {
            'id': self.id,
            'type_id': self.type_id,
            'name': self.name,
            'datatype': self.datatype,
            'options': options
        }


class RiskTypeInstance(db.Model):
    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))

    type = db.relationship("RiskTypeDefinition", uselist=False)


class RiskTypeFieldInstance(db.Model):
    __tablename__ = 'fieldinstances'

    id = db.Column(db.Integer, primary_key=True)

    instance_id = db.Column(db.Integer, db.ForeignKey('instances.id'))
    instance = db.relationship("RiskTypeInstance", uselist=False)

    datatype = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    @property
    def value(self):
        ''' get typed value from internal representation
        '''
        if self.type == 'text':
            return self.text
        elif self.type == 'number':
            return float(self.text)
        elif self.type == 'enum':
            return self.text
        elif self.type == 'date':
            return dateutil.parser.parse(self.text)
        return None

    @value.setter
    def value(self, val):
        ''' encode typed value to internal representation
        '''
        self.text = FieldEncoder().encode(val)


class FieldEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        else:
            return super(FieldEncoder, self).default(obj)

