from flask import Flask, render_template, url_for, flash, redirect, Markup, request 
from forms import RegistrationForm, LoginForm, CensusData
# from classifier import RandomForest

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
    if gender == "femminile":
        gender = 2
    else:
        gender = 1
    
    if isinstance(age, str) == True:
        age = int(age)
    if stato_civile == "celibe/nubile":
        stato_civile = 1
    elif stato_civile == "convivente":
        stato_civile = 2
    elif stato_civile == "sposato/a":
        stato_civile = 3
    elif stato_civile == "vedovo/a":
        stato_civile = 4
    elif stato_civile == "separato/a":
        stato_civile = 5
    else:
        gender = 6
    return render_template('home.html', form=form, age=age, gender=gender, place=place, componenti=componenti, stato_civile=stato_civile)


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
    app.run(debug=True)