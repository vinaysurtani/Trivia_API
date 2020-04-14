import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:1234@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['categories']))

    def test_404_no_category(self):
        res=self.client().get('/categories/1234')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')




    def test_get_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_404_no_questions(self):
        res=self.client().get('/questions?page=1000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)#----------------
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')




    def test_delete_question(self):
        question=Question(question='a',answer='a',difficulty=1,category=1)
        question.insert()
        question_id=question.id
        res=self.client().delete(f'/questions/{question_id}')
        data=json.loads(res.data)
        query=Question.query.filter(Question.id==question_id).one_or_none()
        self.assertEqual(res.status_code,200)#----------------
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],question_id)
        self.assertEqual(query,None)

    def test_404_no_delete_question(self):
        res=self.client().delete('/questions/c')
        data=json.loads(res.data)#----------------
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')



    def test_new_question(self):
        new_question={
            'question':'a',
            'answer':'a',
            'difficulty':1,
            'category':1
        }
        res=self.client().post('/questions',json=new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_422_missing_info_question(self):
        new_question={
            'question':'a',
            'difficulty':1
        }
        res=self.client().post('/questions',json=new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')




    def test_search_questions(self):
        new_search={'searchTerm':'a'}
        res=self.client().post('/questionSearch',json=new_search)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_no_search_question(self):
        new_search={'searchTerm':''}
        res=self.client().post('/questionSearch',json=new_search)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')




    def test_category_questions(self):
        res=self.client().get('/categories/1/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])        
        self.assertTrue(data['current_category'])

    def test_404_not_found_category_question(self):
        res=self.client().get('categories/999/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)#----------------
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')



    def test_quiz(self):
        new_quiz={
            'previous_questions':[],
            'quiz_category':{
                'id':1,
                'type':'Math'
            }
        }
        res=self.client().post('/quizzes',json=new_quiz)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)#----------------
        self.assertEqual(data['success'],True)


    def test_422_missing_info_quiz(self):
        new_quiz={
            'previous_questions':[]
        }
        res=self.client().post('/quizzes',json=new_quiz)#----------------
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)#----------------
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()