import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Journal(Model):
    title = CharField()
    date = DateField(default=datetime.date.today)
    timespent = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)

    @classmethod
    def create_entry(cls, title, timespent, learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(
                    title = title,
                    timespent = timespent,
                    learned = learned,
                    resources = resources
                )
        except IntegrityError:
            raise ValueError("Entry already exists")




def initialize():
    DATABASE.connect()
    DATABASE.drop_tables([Journal], safe=True)
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()