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

years = [('1', '2002'), ('2', '2001'), ('2', '2000'), ('2', '1999')]
province = [('1', 'Trento'), ('2', 'Trieste')]
class CensusData(FlaskForm):
    eta = SelectField('Anno di nascita', choices=years)
    genere = RadioField('Genere', choices = ['maschile', 'femminile'])
    residenza2= SelectField('Provincia di residenza', choices=province) 
    eta2 = DateField('Anno di nascita', format='%Y')   
    submit = SubmitField('Vai!')
