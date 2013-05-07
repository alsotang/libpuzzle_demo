drop table if exists image;
CREATE TABLE image (
  image_id INTEGER NOT NULL PRIMARY KEY autoincrement,
  name TEXT,
  description TEXT,
  file_path TEXT NOT NULL,
  signature TEXT NOT NULL
);

drop table if exists img_sig_words;
CREATE TABLE img_sig_words (
  image_id INTEGER NOT NULL,
  sig_word TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS position_sig ON img_sig_words(image_id, sig_word);

