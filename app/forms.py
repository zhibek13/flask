from flask_wtf import FlaskForm
import wtforms as wf


class UserForm(FlaskForm):
    username = wf.StringField('Пользователь', validators=[wf.validators.DataRequired()])
    password = wf.PasswordField('Пользователь', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=8, max=64)
    ])
    submit = wf.SubmitField('OK')


class PostForm(FlaskForm):
    title = wf.StringField('Заголовок', validators=[wf.validators.DataRequired()])
    content = wf.TextAreaField('Текст Новости', validators=[wf.validators.DataRequired()])
    is_boom_news = wf.BooleanField('Супер новость')
    submit = wf.SubmitField('OK')
