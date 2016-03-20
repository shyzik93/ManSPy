#! /usr/bin/env python
# -*- coding: utf-8 -*-
import NLModules, eonums

E = NLModules.getLangModule("Esperanto")
print dir(E)

# FALSE unu duiliardo mil 1000000000000000 1000000000001000

#for i in range(1000000000000000, 1000000001000000):
for i in range(100001):
  eo = eonums.int2eo(i)
  #print eo.encode('utf-8')
  sentences = E.getGraphmathA(eo)
  sentences = E.getMorphA(sentences)
  sentences = E.getPostMorphA(sentences)
  text = E.getSyntA(sentences)

  sentence = text(0)
  nv = sentence.getByPos(-1, "number_value")
  if i != nv: print 'FALSE', eo.encode('utf-8'), nv, i