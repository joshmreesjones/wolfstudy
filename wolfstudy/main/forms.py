import re
from flask.ext.wtf import Form
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.fields import Field
from wtforms.validators import Length, Required
from wtforms.widgets import TextInput

class AskQuestionForm(Form):
    title = StringField('Title', validators=[Required(), Length(min=15, max=200)])
    content = TextAreaField('Content', validators=[Required(), Length(min=50, max=30000)])

    # This is a hidden input. It is not displayed in the browser, but its data is sent to the server.
    # Client-side JavaScript fills the field with a comma-separated list of tags.
    tags = StringField()

    submit = SubmitField('Submit')

    def validate_tags(form, field):
        pattern = re.compile('^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$')
        for tag in field.data.split(','):
            if not pattern.match(tag):
                return False
        return True

class AnswerQuestionForm(Form):
    content = TextAreaField('Content', validators=[Required(), Length(min=50, max=30000)])

    submit = SubmitField('Submit')
