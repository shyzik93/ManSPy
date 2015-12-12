# -*- coding: utf-8 -*-

from ManSPy import relation

settings = None

def add_group(arg0, group=0, word=0):
  print "Group is added:", group, "in", word
  print "Getted settings:", settings

list_FASIF = ["""
add_group
group y
word y

Esperanto
dolaro: monero
de cambio: dato
dolaro estas parto de cambio
"""]
