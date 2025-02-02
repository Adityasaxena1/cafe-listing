from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, InputRequired
import csv



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField("Cafe Location on Google Maps (URL)", validators=[URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=[("☕️"),
                                                          ("☕️ ☕️"),
                                                          ("☕️ ☕️ ☕️"),
                                                          ("☕️ ☕️ ☕️ ☕️"),
                                                          ("☕️ ☕️ ☕️ ☕️ ☕️")
                                                          ], validators=[InputRequired()])
    wifi_strength_rating = SelectField("Wifi Strength Rating", choices=[("✘"),
                                                                        ("💪"),
                                                                        ("💪 💪"),
                                                                        ("💪 💪 💪"),
                                                                        ("💪 💪 💪 💪"),
                                                                        ("💪 💪 💪 💪 💪")
                                                                        ], validators=[InputRequired()])
    power_socket = SelectField("Power Socket Availability", choices=[("✘"),
                                                                     ("🔌"),
                                                                     ("🔌 🔌"),
                                                                     ("🔌 🔌 🔌"),
                                                                     ("🔌 🔌 🔌 🔌"),
                                                                     ("🔌 🔌 🔌 🔌 🔌")
                                                                     ], validators=[InputRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        data = [form.cafe.data, form.cafe_location.data, form.opening_time.data, form.closing_time.data, form.coffee_rating.data, form.wifi_strength_rating.data, form.power_socket.data]
        with open('cafe-data.csv', 'a', encoding='utf-8') as fd:
            writer = csv.writer(fd)
            writer.writerow(data)

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
