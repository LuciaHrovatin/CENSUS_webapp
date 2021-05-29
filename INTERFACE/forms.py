from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

HOUR_CHOICES = [('1', '8am'), ('2', '10am')]
class CensusData(FlaskForm):
    eta = IntegerField('Anno di nascita', validators=[DataRequired()])
    genere = RadioField('Genere', choices = ['machile', 'femminile'])
    residenza2= SelectField('Provincia di residenza', choices=HOUR_CHOICES) 
    eta2 = DateField('Start Date', format='%Y')   
    submit = SubmitField('Vai!')
