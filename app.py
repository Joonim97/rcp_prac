from flask import Flask, render_template, request, redirect, url_for
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class GameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_choice = db.Column(db.String(10), nullable=False)
    computer_choice = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(10), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play', methods=['POST'])
def play():
    user_choice = request.form['choice']
    choices = ['가위', '바위', '보']
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = '무'
    elif (user_choice == '가위' and computer_choice == '보') or \
         (user_choice == '바위' and computer_choice == '가위') or \
         (user_choice == '보' and computer_choice == '바위'):
        result = '승'
    else:
        result = '패'

    new_game = GameHistory(user_choice=user_choice,
                           computer_choice=computer_choice, result=result)
    db.session.add(new_game)
    db.session.commit()

    return render_template('result.html', user_choice=user_choice, computer_choice=computer_choice, result=result)


@app.route('/history')
def history():
    games = GameHistory.query.all()
    win_count = GameHistory.query.filter_by(result='승').count()
    draw_count = GameHistory.query.filter_by(result='무').count()
    lose_count = GameHistory.query.filter_by(result='패').count()
    return render_template('history.html', games=games, win_count=win_count, draw_count=draw_count, lose_count=lose_count)


if __name__ == '__main__':
    app.run(debug=True)
