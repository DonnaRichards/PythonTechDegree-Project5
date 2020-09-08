import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Journal(Model):
    title = CharField()
    date = DateField(default=datetime.date.today)
    timeSpent = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_entry(cls, title, date, timeSpent, learned, resources):
        """
        Add journal entry to database
        """
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    date=date,
                    timeSpent=timeSpent,
                    learned=learned,
                    resources=resources
                )
        except IntegrityError:
            raise ValueError("Entry already exists")


def initialize():
    """
    initialise the database model
    current functionality is to delete all DB tables and recreate
    at each new run of application.  For "real" use, would not do this
    """
    DATABASE.connect()
    DATABASE.drop_tables([Journal], safe=True)
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()
