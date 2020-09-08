from flask import (Flask, g, render_template, flash, redirect,
                   url_for, abort)

import models
import forms
import datetime

HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

app = Flask(__name__)
app.secret_key = ";fihsef;ohsdfhaouwe;flheos837yv"


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
@app.route('/index')
@app.route('/')
def list_entries():
    """
    List all journal entries, summary view.  Also application home page
    """
    entries = models.Journal.select().limit(100).order_by(-models.Journal.id)
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def create_entry():
    """
    Add a new journal entry
    """
    form = forms.JournalForm()
    if form.validate_on_submit():
        models.Journal.create_entry(
            title=form.title.data,
            date=form.date.data,
            timeSpent=int(form.timeSpent.data),
            resources=form.resources.data.strip(),
            learned=form.learned.data.strip()
        )
        flash("New journal entry successfully created", "success")
        return redirect(url_for('list_entries'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:entry_id>')
def entry_detail(entry_id):
    """
    Show full (detailed) view of a single journal entry
    """
    try:
        entry = models.Journal.get(models.Journal.id == entry_id)
    except models.JournalDoesNotExist:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<int:entry_id>/edit', methods=('GET', 'POST'))
def edit_entry(entry_id):
    """
    Edit a journal entry - form is prepopulated with the existing entry
    and fields can be updated as required
    """
    try:
        entry = models.Journal.get(models.Journal.id == entry_id)
    except models.JournalDoesNotExist:
        abort(404)
    # including obj param in form call to prepopulate fields, credit to
    # goonan.io/flask-wtf-tricks
    form = forms.JournalForm(obj=entry)
    if form.validate_on_submit():
        models.Journal.update(
            title=form.title.data,
            date=form.date.data,
            timeSpent=int(form.timeSpent.data),
            resources=form.resources.data.strip(),
            learned=form.learned.data.strip()
        ).where(models.Journal.id == entry_id).execute()
        flash("Journal entry successfully updated", "success")
        return redirect(url_for('list_entries'))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/<int:entry_id>/delete')
def delete_entry(entry_id):
    """
    Delete a journal entry
    """
    models.Journal.delete_by_id(entry_id)
    flash("Journal entry successfully deleted", "success")
    return redirect(url_for('list_entries'))


@app.errorhandler(404)
def not_found(error):
    """
    Display application custom 404 page if a link returns not found (404) error
    """
    return render_template('404.html'), 404


# dunder main check below commented out as when I am running this project in PyCharm,
# __name__ variable is equal to 'app' (script name), not '__main__'
# Am aware it is best practice to include this check.
# if __name__ == '__main__':
models.initialize()
try:
    models.Journal.create_entry(
        title='Sample Entry 1',
        date=datetime.datetime.now(),
        timeSpent=4,
        learned='''Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis 
        et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia 
        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui 
        ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia 
        dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora 
        incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, 
        quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea 
        commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse 
        quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?''',
        resources='''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
        labore et dolore magna aliqua. Nam libero justo laoreet sit amet. '''
    )
except ValueError:
    pass

app.run(host=HOST, port=PORT, debug=DEBUG)
