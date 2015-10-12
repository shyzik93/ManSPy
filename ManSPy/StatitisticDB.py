# -*- coding: utf-8 -*-
import sqlite3 as sql, GeneralForDB

class StatisticDB():
  def __init__(self, language):
    self.c, self.cu = GeneralForDB.create_bd_file(language, 'static.db')
    self.cu.executescript('''
      CREATE TABLE IF NOT EXISTS nl (
        direction TEXT,
        interface TEXT,
        message TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP);
      CREATE TABLE IF NOT EXISTS arguments (
        name TEXT,
        information TEXT);
      CREATE TABLE IF NOT EXISTS analysys (
        name TEXT,
        analyse TEXT);''')
