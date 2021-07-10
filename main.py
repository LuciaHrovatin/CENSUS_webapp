from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, CensusData
from collector import number_regions
from classifier import redis_classifier

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = CensusData()
    age=request.args.get('eta')
    gender=request.args.get('genere')
    place=request.args.get('residenza2')
    componenti=request.args.get('componenti')
    stato_civile=request.args.get('stato_civile')

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
        prob = 0
    else:
        region = number_regions("dags/dataset/province-ita.json", province=place)
        prob = redis_classifier(componenti, gender, age, stato_civile, region)

    return render_template('home.html', form=form, age=age, gender=gender, place=place, componenti=componenti, stato_civile=stato_civile, prob=prob)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/line")
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)

if __name__ == '__main__':
    app.run()