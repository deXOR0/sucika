from flask import render_template, url_for, redirect, request, jsonify, flash
from sucika import app, db, sucika_id, bcrypt
from sucika.models import User, Sucika
from sucika.forms import ViewBySID, Login, Register
from flask_login import login_user, current_user, logout_user, login_required

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def sucika():
    form = ViewBySID()
    if form.sid.data:
        return redirect(url_for('view_by_sid', sid=form.sid.data))
    return render_template('sucika.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_sucika'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully created account for {}!'.format(form.fullname.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_sucika'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('view_all_sucika'))
        else:
            flash('Wrong email or password!', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

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
@login_required
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