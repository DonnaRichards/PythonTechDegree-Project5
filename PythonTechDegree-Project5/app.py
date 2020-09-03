from flask import (Flask, g, render_template, flash, redirect,
                   url_for, abort)

import models
import forms

HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

app = Flask(__name__)


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response



@app.route('/entries')
@app.route('/')
def list_entries():
    entries = models.Journal.select().limit(100)
    return render_template('index.html', entries=entries)


@app.route('/entries/new')
def create_entry():
    form = forms.JournalForm()
    if form.validate_on_submit():
        models.Journal.create_entry(
            title=form.title.data,
            timespent=int(form.timespent.data),
            resources=form.resources.data,
            learned=form.learned.data
        )
        flash("New journal entry successfully created")
        return redirect(url_for('index'))
    return render_template()

@app.route('/entries/<int:entry_id>')
def entry_detail(entry_id):
    entry = models.Journal.select().where(models.Journal.id == entry_id)
    if entry.count() == 0:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<int:entry_id>/edit')
def edit_entry():
    pass

@app.route('/entries/<int:entry_id>/delete')
def delete_entry():
    pass


# dunder main check below commented out as when I am running this project in PyCharm,
# __name__ variable is equal to 'app' (script name), not '__main__'
# Am aware it is best practice to include this check.
#if __name__ == '__main__':
models.initialize()
try:
    models.Journal.create_entry(
        title='Sample Entry 1',
        timespent=4,
        learned="A lot of stuff",
        resources="Dr Google"
    )
except ValueError:
    pass

app.run(host=HOST, port=PORT, debug=DEBUG)
