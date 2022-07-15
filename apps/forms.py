
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired
from wtforms import SelectField, FloatField, BooleanField, IntegerRangeField

FL_1 = "PassionFruit"
FL_2 = "Test"
class OrderForm(FlaskForm):
    # Shot #1 BooleanField
    # Shot #2 BooleanField
    # Syrup   Slider
    # Tea Choice 
    # Milk?
    # Pearls? BooleanField
    # Order Name


    ordername = StringField('Name for the Order',
                         id='username_login',
                         validators=[DataRequired()])
    tapioca_pearls = BooleanField('Boba?')
    syrup = IntegerRangeField('Sugar',
                               default = 0)
    shot1 = BooleanField('{} Flavour'.format(FL_1))
    shot2 = BooleanField('{} Flavour'.format(FL_2))
