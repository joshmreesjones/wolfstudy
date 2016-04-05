from flask import flash, redirect, render_template, session, url_for
from flask.ext.login import login_required
from . import main
from .. import db
from .forms import AnswerQuestionForm, AskQuestionForm
from ..models import Answer, Question, User

@main.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@main.route('/question/<int:question_id>/')
def get_question(question_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    answers = question.answers
    form = AnswerQuestionForm()
    return render_template('question.html', question=question, answers=answers, form=form)

@main.route('/question/<int:question_id>/answer/', methods=['POST'])
@login_required
def answer_question(question_id):
    form = AnswerQuestionForm()
    if form.validate_on_submit():
        question = Question.query.filter_by(id=question_id).first_or_404()
        content = form.content.data
        new_answer = Answer(content, question)

        db.session.add(new_answer)
        db.session.commit()

        return redirect(url_for('.get_question', question_id=question.id))
    else:
        question = Question.query.filter_by(id=question_id).first_or_404()
        answers = question.answers
        return render_template('question.html', question=question, answers = answers, form=form)

@main.route('/ask/', methods=['GET', 'POST'])
@login_required
def ask_question():
    form = AskQuestionForm()
    if form.validate_on_submit():
        new_question = Question(form.title.data, form.content.data)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('.get_question', question_id=new_question.id))
    else:
        return render_template('ask.html', form=form)

@main.route('/user/<username>/')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
