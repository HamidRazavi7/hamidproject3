import logging

from app import db
from app.db.models import User, Song
from faker import Faker


def test_adding_user(application, add_user):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 1
        assert db.session.query(Song).count() == 0
        # showing how to add a record
        # create a record
        # user = User('keith@webizly.com', 'testtest')
        # add it to get ready to be committed
        # db.session.add(user)
        # call the commit
        # db.session.commit()
        # assert that we now have a new user
        # assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(email='keith@webizly.com').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'keith@webizly.com'
        # this is how you get a related record ready for insert
        user.songs = [
            Song("all i want for christmas is you", "Mariah Karey", "Pop", 2015),
            Song("yummy", "Justin Bieber", "Hip Hop", 2019)
        ]
        # commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='all i want for christmas is you').first()
        assert song1.title == "all i want for christmas is you"
        assert song1.genre == "Pop"
        # changing the title of the song
        song1.title = "SuperSongTitle"
        # saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        assert song2.year == 2015
        assert song2.artist == "Mariah Karey"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0