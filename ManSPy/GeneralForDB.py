# -*- coding: utf-8 -*-
import sqlite3 as sql, os

def create_bd_file(language, name):
  if __name__ == '__main__': db_dir = 'F:\\SourceCode\\DATA_BASE'
  else: db_dir = os.path.abspath('DATA_BASE')
  if not os.path.exists(db_dir) or not os.path.isdir(db_dir):
    os.mkdir(db_dir)
  db_dir = os.path.join(db_dir, language)
  if not os.path.exists(db_dir) or not os.path.isdir(db_dir):
    os.mkdir(db_dir)
  name = os.path.join(db_dir, name)
  c = sql.connect(name)
  cu = c.cursor()
  return c, cu
