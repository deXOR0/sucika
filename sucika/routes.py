from flask import render_template, url_for, redirect, request, jsonify, flash
from sucika import app, db, sucika_id, bcrypt, csv, upload_directory
from sucika.models import User, Sucika
from sucika.forms import ViewBySID, Login, Register, Upload
from flask_login import login_user, current_user, logout_user, login_required
import os


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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully created account for {}!'.format(
            form.fullname.data), 'success')
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
@login_required
def create_sucika():
    name = request.args.get('name', None)
    sid = sucika_id.generate_id(name)
    msg = request.args.get('msg', None)
    sucika = Sucika(sid, name, msg)
    db.session.add(sucika)
    db.session.commit()
    sck = Sucika.query.filter_by(sid=sid).first()


@app.route('/viewAll/', methods=['GET', 'POST'])
@login_required
def view_all_sucika():
    upload = Upload()

    if upload.validate_on_submit():

        filename = csv.save(upload.file.data)
        create_from_csv(os.path.join(upload_directory, filename))

    return render_template('view-all.html', values=Sucika.query.all(), form=upload)


@app.route('/sucika/view/<sid>/')
def view_by_sid(sid):
    sucika = Sucika.query.filter_by(sid=sid).first()
    if sucika:
        return render_template('view-by-sid.html', values=sucika)
    else:
        return render_template('404.html')

def create_from_csv(filepath):
    file = open(filepath)
    content = file.read().splitlines()
    file.close()
    os.remove(filepath)
    sck = Sucika('', '', '')
    for c in content:
        aktivis = c.split(';')
        sid = sucika_id.generate_id(aktivis[0])
        while sck.query.filter_by(sid=sid).first():
            sid = sucika_id.generate_id(aktivis[0])
        sucika = Sucika(sid, aktivis[0], aktivis[1])
        db.session.add(sucika)
        db.session.commit()