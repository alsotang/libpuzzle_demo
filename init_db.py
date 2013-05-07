import os

import pypuzzle

import sqlite3

PUZZLE_IMAGE_DIR = './static/puzzle_images'
DATABASE = './db/puzzle.db'

puzzle = pypuzzle.Puzzle()

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

for image_name in os.listdir(PUZZLE_IMAGE_DIR):
    image_path = os.path.join(PUZZLE_IMAGE_DIR, image_name)
    vec = puzzle.get_cvec_from_file(image_path)
    vec_str = ''.join([str(i) for i in vec])
    conn.execute('insert into \
                 image (name, description, file_path, signature) \
                 values (?, ?, ?, ?)',
                 [image_name, image_name, image_path, vec_str]
                 )
    conn.commit()
    cur.execute('select * from image where signature=?', [vec_str])
    image_id = cur.fetchone()['image_id']

    conn.executemany('insert into \
                     img_sig_words (image_id, sig_word) \
                     values (?, ?)',
                     [(image_id, ("%s__%s" % (i, vec_str[i: 100+i]))) for i in range(100)]
                     )

    conn.commit()


cur.close()
conn.close()
