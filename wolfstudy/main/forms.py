from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, Required

class AskQuestionForm(Form):
    title = StringField('Title', validators=[Required(), Length(min=15, max=200)])
    content = TextAreaField('Content', validators=[Required(), Length(min=50, max=30000)])

    submit = SubmitField('Submit')

class AnswerQuestionForm(Form):
    content = TextAreaField('Content', validators=[Required(), Length(min=50, max=30000)])

    submit = SubmitField('Submit')
