from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sucika_id
from forms import ViewBySID

app = Flask(__name__)
app.config['SECRET_KEY'] = '1cc02622ded9f82327f6dc502f611ed3'
app.config['APPLICATION_ROOT'] = '/sucika'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sucika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sucika(db.Model):
    sid = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100))
    msg = db.Column(db.Text)

    def __init__(self, sid, name, msg):
        self.sid = sid
        self.name = name
        self.msg = msg

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def sucika():
    form = ViewBySID()
    if form.sid.data:
        return redirect(url_for('view_by_sid', sid=form.sid.data))
    return render_template('sucika.html', form=form)

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/createSucika/', methods=['get'])
def create_sucika():
    name = request.args.get('name', None)
    sid = sucika_id.generate_id(name)
    msg = request.args.get('msg', None)
    sucika = Sucika(sid, name, msg)
    db.session.add(sucika)
    db.session.commit()
    sck = Sucika.query.filter_by(sid=sid).first()
    return redirect(url_for('sucika'))

@app.route('/viewAll/')
def view_all_sucika():
    return render_template('view-all.html', values=Sucika.query.all())

@app.route('/sucika/view/<sid>/')
def view_by_sid(sid):
    sucika = Sucika.query.filter_by(sid=sid).first()
    if sucika:
        return render_template('view-by-sid.html', values=sucika)
    else:
        return render_template('404.html')

@app.route('/social/')
def media():
    return render_template('social.html')

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()