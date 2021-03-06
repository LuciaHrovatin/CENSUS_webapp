from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired


years = [('2002'), ('2001'), ('2000'), ('1999'), ('1998'), ('1997'), ('1996'), ('1995'), ('1994'), ('1993'),
('1992'), ('1991'), ('1990'), ('1989'), ('1988'), ('1987'), ('1986'), ('1985'), ('1984'), ('1983'),
('1982'), ('1981'), ('1980'), ('1979'), ('1978'), ('1977'), ('1976'), ('1975'), ('1974'), ('1973'),
('1972'), ('1971'), ('1970'), ('1969'), ('1968'), ('1967'), ('1966'), ('1965'), ('1964'), ('1963'),
('1962'), ('1961'), ('1960'), ('1959'), ('1958'), ('1957'), ('1956'), ('1955'), ('1954'), ('1953'),
('1952'), ('1951'), ('1950'), ('1949'), ('1948'), ('1947'), ('1946'), ('1945'), ('1944'), ('1943'),
('1942'), ('1941'), ('1940'), ('1939'), ('1938'), ('1937'), ('1936'), ('1935'), ('1934'), ('1933'),
('1932')]

province = [('Agrigento'), ('Alessandria'), ('Ancona'), ('Aosta'), ('Arezzo'), ('Ascoli Piceno'), ('Asti'), ('Avellino'), ('Bari'), ('Barletta-Andria-Trani'),
('Belluno'), ('Benevento'), ('Bergamo'), ('Biella'), ('Bologna'), ('Bolzano'), ('Brescia'), ('Brindisi'), ('Cagliari'), ('Caltanissetta'),
('Campobasso'), ('Carbonia-Iglesias') , ('Caserta'), ('Catania'), ('Catanzaro'), ('Chieti'), ('Como'), ('Cosenza'), ('Cremona'), ('Crotone'),
('Cuneo'), ('Enna'), ('Fermo'), ('Ferrara'), ('Firenze'), ('Foggia'), ('Forlì-Cesena'), ('Frosinone'), ('Genova'), ('Gorizia'),
('Grosseto'), ('Imperia'), ('Isernia'), ('La Spezia'), ("L'Aquila"), ('Latina'), ('Lecce'), ('Lecco'), ('Livorno'), ('Lodi'),
('Lucca'), ('Macerata'), ('Mantova'), ('Massa-Carrara'), ('Matera'), ('Messina'), ('Milano'), ('Modena'), ('Monza e della Brianza'), ('Napoli'),
('Novara'), ('Nuoro'), ('Olbia-Tempio'), ('Oristano'), ('Padova'), ('Palermo '), ('Parma'), ('Pavia'), ('Perugia'), ('Pesaro e Urbino'),
('Pescara'), ('Piacenza'), ('Pisa'), ('Pistoia'), ('Pordenone'), ('Potenza'), ('Prato'), ('Ragusa'), ('Ravenna'), ('Reggio Calabria'),
('Reggio Emilia'), ('Rieti'), ('Rimini'), ('Roma'), ('Rovigo'), ('Salerno'), ('Medio Campidano'), ('Sassari'), ('Savona'), ('Siena'),
('Siracusa'), ('Sondrio'), ('Taranto'), ('Teramo'), ('Terni'), ('Torino'), ('Ogliastra'), ('Trapani'), ('Trento'), ('Treviso'),
('Trieste'), ('Udine'), ('Varese'), ('Venezia'), ('Verbano-Cusio-Ossola'), ('Vercelli'), ('Verona'), ('Vibo Valentia'), ('Vicenza'), ('Viterbo')]

n_componenti = [('1'), ('2'), ('3'), ('4'), ('5'), ('6'), ('7'), ('8'), ('9'), ('10'), ('11'), ('12'), ('13'), ('14')]

stato = [('celibe/nubile'), ('convivente'), ('sposato/a'), ('vedovo/a'), ('separato/a'), ('divorziato/a')]

sex = ['maschile', 'femminile', 'preferisco non specificare']

class CensusData(FlaskForm):
    eta = SelectField('Anno di nascita:', choices=years, validators=[DataRequired()])
    genere = RadioField('Genere:', choices=sex, default='preferisco non specificare', validators=[DataRequired()])
    residenza2 = SelectField('Provincia di residenza:', choices=province, validators=[DataRequired()])
    componenti = SelectField('Numero di componenti del nucleo familiare:', choices=n_componenti, validators=[DataRequired()])
    stato_civile = RadioField('Stato civile:', choices=stato, default='celibe/nubile', validators=[DataRequired()])
    submit = SubmitField('Predici fascia di reddito')