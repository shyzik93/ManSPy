import eonums

from manspy import NLModules

E = NLModules.getLangModule("Esperanto")

# FALSE unu duiliardo mil 1000000000000000 1000000000001000

# for i in range(1000000000000000, 1000000001000000):
for i in range(100001):
    eo = eonums.int2eo(i)
    # print eo.encode('utf-8')
    sentences = E.get_analysis(eo)
    sentences = E.get_analysis(sentences)
    sentences = E.get_analysis(sentences)
    text = E.get_analysis(sentences)

    sentence = text(0)
    nv = sentence.getByPos(-1, "number_value")
    if i != nv:
        print('FALSE', eo.encode('utf-8'), nv, i)