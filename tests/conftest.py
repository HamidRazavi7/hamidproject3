"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import logging
import os

import pytest
from app import create_app, User
from app.db import db

#this is a good tutorial I used to fix this code to do datbase testing.
#https://xvrdm.github.io/2017/07/03/testing-flask-sqlalchemy-database-with-pytest/

@pytest.fixture()
def application():
    """This makes the app"""
    os.environ['FLASK_ENV'] = 'testing'
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    logdir = os.path.join(root, '../logs')
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    application = create_app()

    with application.app_context():
        db.create_all()
        log = logging.getLogger('myApp')
        log.info(application.config['SQLALCHEMY_DATABASE_URI'])
        yield application
        db.session.remove()
        #drops the database tables after the test runs
        db.drop_all()

@pytest.fixture()
def add_user(application):
    with application.app_context():
        #new record
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()




@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()
