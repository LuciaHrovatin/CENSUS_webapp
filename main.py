from flask import Flask, render_template, request
from forms import CensusData
from src.collector import number_regions
from src.classifier import redis_classifier
from scr import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = CensusData()
    age = request.args.get('eta')
    gender = request.args.get('genere')
    place = request.args.get('residenza2')
    componenti = request.args.get('componenti')
    stato_civile = request.args.get('stato_civile')

    # mstandardize gender
    if "femminile" == gender:
        gender = 2
    elif "maschile" == gender:
        gender = 1
    else:
        gender = 0

    # modify age
    if isinstance(age, str):
        age = int(age)

    # modify componenti
    if isinstance(componenti, str):
        componenti = int(componenti)

    # standardize stato civile
    if isinstance(stato_civile, str):
        status = {
            "celibe/nubile": 1,
            "convivente": 2,
            "sposato/a": 3,
            "vedovo/a": 4,
            "separato/a": 5
        }
        if stato_civile in status:
            stato_civile = status[stato_civile]
        else:
            stato_civile = 6

    if place is None:
        prob2 = 0
    else:
        region = number_regions(province=place, filename="src.province-ita.json")
        prob2 = redis_classifier(ncomp=componenti, sex=gender, age=age, statciv=stato_civile, place=region)

    return render_template('home.html', form=form, age=age, gender=gender, place=place, componenti=componenti, stato_civile=stato_civile, prob=prob2)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/line")
def line():
    return render_template('line_chart.html', title='Graphs', max=17000)


if __name__ == '__main__':
    app.run()