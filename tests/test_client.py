import unittest
from flask import url_for
from wolfstudy import create_app, db
from wolfstudy.models import Question, Tag, User

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Log in' in response.data)

    def test_register_confirm_logout_login(self):
        # Register a new account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'person@example.com',
            'username': 'person',
            'password': 'cat',
            'password_retype': 'cat'
        }, follow_redirects=True)
        self.assertTrue('Logged in as person' in response.data)
        self.assertTrue('You have not confirmed your account yet' in response.data)

        # Get a confirmation token
        user = User.query.filter_by(email='person@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        self.assertTrue('You have confirmed your account' in response.data)

        # Log out
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue('You have been logged out' in response.data)

        # Log in
        response = self.client.post(url_for('auth.login'), data={
            'username': 'person',
            'password': 'cat'
        }, follow_redirects=True)
        self.assertTrue('Logged in as person' in response.data)

    def test_get_question(self):
        q = Question(title='test_get_question title', content='test_get_question content')

        q.tags.append(Tag(tag_name='tag1'))
        q.tags.append(Tag(tag_name='tag2'))
        q.tags.append(Tag(tag_name='tag3'))

        db.session.add(q)
        db.session.commit()

        # Make sure we can get the question
        response = self.client.get(url_for('main.get_question', question_id=q.id))
        self.assertTrue('test_get_question title' in response.data)
        self.assertTrue('test_get_question content' in response.data)
        self.assertTrue('tag1' in response.data)
        self.assertTrue('tag2' in response.data)
        self.assertTrue('tag3' in response.data)

        # We're not logged in, so make sure we can't answer the question
        self.assertTrue('to answer this question' in response.data)
        # "Log in or     ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
        #       register to answer this question."

        # Make a user and log in
        u = User(username='person', password='cat')
        db.session.add(u)
        db.session.commit()
        self.client.post(url_for('auth.login'), data={
            'username': 'person',
            'password': 'cat'
        })

        response = self.client.get(url_for('main.get_question', question_id=q.id))
        # Make sure we can answer the question
        self.assertFalse('to answer this question' in response.data)

    def test_show_user(self):
        u = User(username='person', password='cat', email='person@example.com')
        db.session.add(u)
        db.session.commit()
        response = self.client.get(url_for('main.show_user', username=u.username))
        self.assertTrue(('Username: ' + u.username) in response.data)

    def test_ask_question(self):
        # While logged out, we should be redirected from the ask question page
        response = self.client.get(url_for('main.ask_question'), follow_redirects=True)
        self.assertTrue('Please log in to access this page.' in response.data)

        # Make a user and log in
        u = User(username='person', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()
        self.client.post(url_for('auth.login'), data={
            'username': 'person',
            'password': 'cat'
        })

        # While logged in, we should be able to get to the ask question page
        response = self.client.get(url_for('main.ask_question'), follow_redirects=True)
        self.assertTrue('Ask a question' in response.data)

        # Ask a question
        response = self.client.post(url_for('main.ask_question'), data={
            'title': 'test_ask_question title',
            'content': 'test_ask_question content'
        }, follow_redirects=True)
        self.assertTrue('test_ask_question title' in response.data)
        self.assertTrue('test_ask_question content' in response.data)

    def test_answer_question(self):
        # Make and add a question
        q = Question(title='test_answer_question title', content='test_answer_question content')
        db.session.add(q)
        db.session.commit()

        # While not logged in, we should not be able to answer a question
        response = self.client.post(url_for('main.answer_question', question_id=q.id), data={
            'content': 'test_answer_question content'
        })
        self.assertTrue(response.status_code == 302) # Redirect

        # Make a user and log in
        u = User(username='person', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()
        self.client.post(url_for('auth.login'), data={
            'username': 'person',
            'password': 'cat'
        })

        response = self.client.post(url_for('main.answer_question', question_id=q.id), data={
            'content': 'test_answer_question content'
        }, follow_redirects=True)
        self.assertTrue('test_answer_question content' in response.data)
