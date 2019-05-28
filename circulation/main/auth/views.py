# -*- coding:utf-8 -*-
from circulation.web import db
from circulation.models import User, Library
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from circulation.main.auth import auth
from circulation.main.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = User.query.filter(User.email.ilike(login_form.email.data)).first()
        if the_user is not None and the_user.verify_password(login_form.password.data):
            login_user(the_user, login_form.remember_me.data)
            flash(u'Login successful. Welcome %s!' % the_user.name, 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'Invalid username or password.', 'danger')
    return render_template("login.html", form=login_form, title=u"Login")


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u'Logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        the_user = User(
            email=form.email.data,
            name=form.name.data,
            password=form.password.data)
        db.session.add(the_user)
        db.session.commit()
        flash(u'Registration successful. Welcome %s!' % form.name.data, 'success')
        login_user(the_user)
        new_library = Library(
            name=form.name.data + str("'s Library"),
            user_id=current_user.id)
        db.session.add(new_library)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('register.html', form=form, title=u"Register")


@auth.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'Password changed succssfully.', 'info')
        return redirect(url_for('user.detail', user_id=current_user.id))
    return render_template('user_edit.html', form=form, user=current_user, title=u"Change password")
