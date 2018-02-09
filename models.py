from datetime import datetime, date
import dateutil.parser

from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy

# database model
db = SQLAlchemy()


class RiskTypeDefinition(db.Model):
    ''' Definition of a risk type
    '''
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)

    # name of risk type
    name = db.Column(db.String, nullable=False)

    # description of risk type
    description = db.Column(db.String, nullable=False)

    fields = db.relationship('RiskTypeField')

    # JSON serialization helper
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'fields': [x.serialize for x in sorted(self.fields, key=lambda x: x.id)]
        }


class RiskTypeField(db.Model):
    ''' Definition of a risk type field
    '''
    __tablename__ = 'fields'

    id = db.Column(db.Integer, primary_key=True)

    # Risk type definition id to which this field definition belongs
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    type = db.relationship("RiskTypeDefinition", uselist=False)

    # Field name
    name = db.Column(db.String, nullable=False)

    # Field hint
    hint = db.Column(db.String)

    # Field data type (text, number, date, enum)
    datatype = db.Column(db.String, nullable=False)

    # comma delimited list of options for enumerable fields
    options = db.Column(db.String, nullable=True)

    # required flag
    required = db.Column(db.Boolean)

    # JSON serialization helper
    @property
    def serialize(self):
        options = []
        if isinstance(self.options, str):
            options = self.options.split(',')
        return {
            'id': self.id,
            'type_id': self.type_id,
            'name': self.name,
            'hint': self.hint,
            'required': self.required is True,
            'datatype': self.datatype,
            'options': options
        }


class RiskTypeInstance(db.Model):
    ''' instance of a risk type
    '''
    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True)

    # risk type definition reference
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    type = db.relationship("RiskTypeDefinition", uselist=False)

    date = db.Column(db.Date, nullable=False)


class RiskTypeFieldInstance(db.Model):
    ''' instance of a risk type field
    '''
    __tablename__ = 'fieldinstances'

    id = db.Column(db.Integer, primary_key=True)

    # risk type instance associated with the field instance
    instance_id = db.Column(db.Integer, db.ForeignKey('instances.id'))
    instance = db.relationship("RiskTypeInstance", uselist=False)

    # field definition associated with the field instance
    field_definition_id = db.Column(db.Integer, db.ForeignKey('fields.id'))
    field_definition = db.relationship("RiskTypeField", uselist=False)

    # internal text representation of the field value
    text = db.Column(db.String, nullable=False)

    @property
    def value(self):
        ''' get typed value from internal representation
        '''
        datatype = self.field_definition.datatype
        if datatype == 'text':
            return self.text
        elif datatype == 'number':
            return float(self.text)
        elif datatype == 'enum':
            return self.text
        elif datatype == 'date':
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

