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

years = [('1', '2002'), ('2', '2001'), ('3', '2000'), ('4', '1999'), ('5', '1998'), ('6', '1997'), ('7', '1996'), ('8', '1995'), ('9', '1994'), ('10', '1993'), 
('11', '1992'), ('12', '1991'), ('13', '1990'), ('14', '1989'), ('15', '1988'), ('16', '1987'), ('17', '1986'), ('18', '1985'), ('19', '1984'), ('20', '1983'),
('21', '1982'), ('22', '1981'), ('23', '1980'), ('24', '1979'), ('25', '1978'), ('26', '1977'), ('27', '1976'), ('28', '1975'), ('29', '1974'), ('30', '1973'),
('31', '1972'), ('32', '1971'), ('33', '1970'), ('34', '1969'), ('35', '1968'), ('36', '1967'), ('37', '1966'), ('38', '1965'), ('39', '1964'), ('40', '1963'),
('41', '1962'), ('42', '1961'), ('43', '1960'), ('44', '1959'), ('45', '1958'), ('46', '1957'), ('47', '1956'), ('48', '1955'), ('49', '1954'), ('50', '1953'),
('51', '1952'), ('52', '1951'), ('53', '1950'), ('54', '1949'), ('55', '1948'), ('56', '1947'), ('57', '1946'), ('58', '1945'), ('59', '1944'), ('60', '1943'),
('61', '1942'), ('62', '1941'), ('63', '1940'), ('64', '1939'), ('65', '1938'), ('66', '1937'), ('67', '1936'), ('68', '1935'), ('69', '1934'), ('70', '1933'),
('71', '1932')]

province = [('1', 'Agrigento'), ('2', 'Alessandria'), ('3', 'Ancona'), ('4', 'Aosta'), ('5', 'Arezzo'), ('6', 'Ascoli Piceno'), ('7', '	Asti'), ('8', '	Avellino'), ('9', '	Bari'), ('10', 'Barletta-Andria-Trani'), 
('11', 'Belluno'), ('12', 'Benevento'), ('13', 'Bergamo'), ('14', 'Biella'), ('15', 'Bologna'), ('16', 'Bolzano'), ('17', 'Brescia'), ('18', 'Brindisi'), ('19', 'Cagliari'), ('20', 'Caltanissetta'), 
('21', 'Campobasso'), ('22', 'Carbonia-Iglesias') , ('23', 'Caserta'), ('24', 'Catania'), ('25', 'Catanzaro'), ('26', 'Chieti'), ('27', 'Como'), ('28', 'Cosenza'), ('29', 'Cremona'), ('30', 'Crotone'),
('31', 'Cuneo'), ('32', 'Enna'), ('33', 'Fermo'), ('34', 'Ferrara'), ('35', 'Firenze'), ('36', 'Foggia'), ('37', 'Forlì-Cesena'), ('38', 'Frosinone'), ('39', 'Genova'), ('40', 'Gorizia'),
('41', 'Grosseto'), ('42', 'Imperia'), ('43', 'Isernia'), ('44', 'La Spezia'), ('45', "L'Aquila"), ('46', 'Latina'), ('47', 'Lecce'), ('48', 'Lecco'), ('49', 'Livorno'), ('50', 'Lodi'),
('51', 'Lucca'), ('52', 'Macerata'), ('53', 'Mantova'), ('54', 'Massa-Carrara'), ('55', 'Matera'), ('56', 'Messina'), ('57', 'Milano'), ('58', 'Modena'), ('59', 'Monza e della Brianza'), ('60', 'Napoli'),
('61', 'Novara'), ('62', 'Nuoro'), ('63', 'Olbia-Tempio'), ('64', 'Oristano'), ('65', 'Padova'), ('66', 'Palermo '), ('67', 'Parma'), ('68', 'Pavia'), ('69', 'Perugia'), ('70', 'Pesaro e Urbino'),
('71', 'Pescara'), ('72', 'Piacenza'), ('73', 'Pisa'), ('74', 'Pistoia'), ('75', 'Pordenone'), ('76', 'Potenza'), ('77', 'Prato'), ('78', 'Ragusa'), ('79', 'Ravenna'), ('80', 'Reggio Calabria'),
('81', 'Reggio Emilia'), ('82', 'Rieti'), ('83', 'Rimini'), ('84', 'Roma'), ('85', 'Rovigo'), ('86', 'Salerno'), ('87', 'Medio Campidano'), ('88', 'Sassari'), ('89', 'Savona'), ('90', 'Siena'),
('91', 'Siracusa'), ('92', 'Sondrio'), ('93', 'Taranto'), ('94', 'Teramo'), ('95', 'Terni'), ('96', 'Torino'), ('97', 'Ogliastra'), ('98', 'Trapani'), ('99', 'Trento'), ('100', 'Treviso'),
('101', 'Trieste'), ('102', 'Udine'), ('103', 'Varese'), ('104', 'Venezia'), ('105', 'Verbano-Cusio-Ossola'), ('106', 'Vercelli'), ('107', 'Verona'), ('108', 'Vibo Valentia'), ('109', 'Vicenza'), ('110', 'Viterbo')]

sex = ['maschile', 'femminile', 'preferisco non specificare']
class CensusData(FlaskForm):
    eta = SelectField('Anno di nascita', choices=years)
    genere = RadioField('Genere', choices=sex)
    residenza2= SelectField('Provincia di residenza', choices=province) 
    eta2 = DateField('Anno di nascita', format='%Y')   
    submit = SubmitField('Vai!')
