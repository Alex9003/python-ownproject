from email.policy import default

from flask import Flask, request, session, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os
from datetime import datetime

from sqlalchemy.testing.suite.test_reflection import users

SESSION_USER_ID = 'user_id'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'car_shop.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= 'KeL9KQ_BZnGSoTJsUhMuP8Rrehv7Dit-kpp9KDMIohw'
db = SQLAlchemy(app)



# === MODERLS =================
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f'<User: {self.username}>'

    def check_password(self, password):
        return check_password_hash(self.password,password)


class News(db.Model):
    __tablename__ = 'News'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=0)


# with app.app_context():
#     db.create_all()
# === ROUTES ==================

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    page = request.args.get('page', 1, type = int)
    list_news = News.query.paginate(page=page, per_page=6,)

    for item in list_news:
        if len(item.text) > 250:
            item.text = item.text[:200] + ' ...'

    return render_template('news.html', list_news=list_news)

@app.route('/blog')
def blog():
    return render_template('blog.html')

# ---- Admin ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            message = 'Неправельний Email'
        else:
            if user.check_password(password):
                session[SESSION_USER_ID] = user.id
                return redirect('/')

            message = 'Неправельний пароль'

    return render_template('login.html',message=message)

@app.route('/logout')
def logout():
    session.pop(SESSION_USER_ID, None)
    return render_template('/')

@app.route('/car')
def car():
    return render_template('car.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__=='__main__':
    app.run(debug=True)