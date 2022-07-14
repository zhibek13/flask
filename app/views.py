from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from . import models
from . import forms
from . import login_manager
from app.models import Post, User

#post functions


def index():
    posts = models.Post.query.all()
    super_post = models.Post.query.filter_by(is_boom_news=True).first()
    return render_template('index.html', posts=posts, super_post=super_post)


@login_required
def post_add():
    form = forms.PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            is_boom_news = True if request.form.get('is_boom_news') == 'y' else False
            post = models.Post(title=request.form.get('title'),
                               content=request.form.get('content'),
                               is_boom_news=is_boom_news,
                               user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Вы успешно добавили новость', category='success')
            return redirect(url_for('index'))
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('add_post.html', form=form)


def post_detail(post_id):
    news = Post.query.filter_by(id=post_id).first()
    if news:
        return render_template('post_detail.html', news=news)
    else:
        flash('Пост не найден', category='danger')
        return redirect(url_for('index'))


@login_required
def post_edit():
    post = models.Post.query.filter_by(id=post_id).first()
    if post:
        if post.user_id == current_user.id:
            form = forms.PostForm(obj=post)
            if request.method == 'POST':
                if form.validate_on_submit():
                    title = request.form.get('title')
                    content = request.form.get('content')
                    post.title = title
                    post.content = content
                    db.session.commit()
                    flash('Новость обновлена', category='success')
                    return redirect(url_for('index'))
                if form.errors:
                    for errors in form.errors.values():
                        for error in errors:
                            flash(error, category='danger')
            return render_template('post_edit.html', post=post, form=form)
        else:
            flash('У вас недостаточно прав', category='danger')
            return redirect(url_for('index'))
    else:
        flash('Новость не найдена', category='danger')
        return redirect(url_for('index'))


@login_required
def post_delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        form = forms.PostForm(obj=post)
        if post.user_id == current_user.id:
            if request.method == 'POST':
                db.session.delete(post)
                db.session.commit()
                flash('Пост успешно удален', category='success')
                return redirect(url_for('index'))
            else:
                return render_template('post_delete.html', post=post, form=form)
        else:
            flash('У вас нет прав для удаления записи', category='danger')
            return redirect(url_for('index'))
    else:
        flash('Пост не найден', category='danger')
        return redirect(url_for('index'))

#user Functions


def register():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User(username=request.form.get('username'), password=request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались', category='success')
            return redirect(url_for('login'))
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('register.html', form=form)


def login():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Вы успешно вошли', category='success')
                return redirect(url_for('index'))
            else:
                flash('Неверный логин или пароль!', category='danger')
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('login.html', form=form)


def logout():
    login_user()
    flash('Вы успешно вышли', category='success')
    return redirect(url_for('index'))

