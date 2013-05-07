import os
import tempfile

from sqlite3 import dbapi2 as sqlite3

from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack,\
    safe_join, escape

import pypuzzle

# configuration
DATABASE = 'db/puzzle.db'
PUZZLE_IMAGE_DIR = 'puzzle_images'
IMAGES_PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

puzzle = pypuzzle.Puzzle()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


def get_cursor():
    return get_db().cursor()


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def get_puzzle_images():
    # return [safe_join(app.config['PUZZLE_IMAGE_DIR'], p)
    #         for p in os.listdir('./static/%s' % app.config['PUZZLE_IMAGE_DIR'])]
    cursor = get_cursor()
    cursor.execute('select distinct image.file_path, image.name, image.description from image')
    images = cursor.fetchall()
    cursor.close()
    return images


@app.route("/")
def index():
    return render_template('index.html', result_images=get_puzzle_images(), result_title='Popular Ones')


@app.route('/about')
def about():
    return '<p>about page</p>'


def search_images(request):
    cursor = get_cursor()
    if request.files.get('image'):

        temp = tempfile.NamedTemporaryFile()
        image_file = request.files['image']
        temp.write(image_file.read())
        temp.flush()

        vec_str = ''.join(map(lambda n: str(n), puzzle.get_cvec_from_file(temp.name)))
        vec_strs = [("%s__%s" % (i, vec_str[i: 100+i])) for i in range(100)]

        place_holder = '?'
        place_holders = ','.join(len(vec_strs)*[place_holder])

        cursor.execute('select distinct image.file_path, image.name, image.description from img_sig_words isw left join image on isw.image_id=image.image_id where sig_word in (%s) ' % place_holders, vec_strs)
        similar_images = cursor.fetchall()

    elif request.form.get('search_text'):
        cursor.execute("select * from image where description like ?", ['%' + request.form['search_text'] + '%'])
        print request.form['search_text']
        similar_images = cursor.fetchall()

    cursor.close()

    return similar_images


@app.route("/search", methods=['POST'])
def search():
    similar_images = search_images(request)

    return render_template('index.html', result_images=similar_images, result_title="Search Result")


if __name__ == "__main__":
    app.run()
