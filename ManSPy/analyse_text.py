# -*- coding: utf-8 -*-
import sys, os, time
from . import NLModules, relation, extractor, converter, BeautySafe

class LangClass():

    levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert"]

    def __init__(self):
        self.lang_modules = {}

    def get_lang_module(self, language):
        if language not in self.lang_modules:
            #TODO проверить наличие модуля и наличие имён в нём
            self.lang_modules[language] = NLModules.getLangModule(language)

        return self.lang_modules[language]

    def NL2IL(self, msg, levels="graphmath convert", settings=None):
        """ Второй аргумент - диапазон конвертирования от первого до последнего
            включительно через пробел. Если требуется сделать лишь один уровень,
            то можно указать только одно слово. Если указан только 'convert',
            то в качестве первого аргумента передаётся список извлечений."""

        if settings is None:
            settings = msg.IF.settings
            sentences = msg.w_text
        else:
            sentences = msg
            msg = None

        print('\n---------------------------------------')
        print('----', sentences)
        print('---------------------------------------')
        t1 =time.time()

        BeautySafe.fwrite('\n\n'+'#'*100+'\n')
        BeautySafe.fwrite(levels+'\n')

        OR = relation.ObjRelation(settings, settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован

        lang_module = self.get_lang_module(settings['language'])

        # Парсим строку диапазона
        levels = levels.split()
        if len(levels)==1:
            level = levels.pop()
            if level[0] == ':': start_level, end_level = self.levels[0], level[1:]
            elif level[-1] == ':': start_level, end_level = level[:-1], self.levels[-1]
            else: start_level = end_level = level
        else: start_level, end_level = levels

        # Графематический анализ
        if start_level in self.levels[:1]:
            t =time.time()

            BeautySafe.safe_NL(sentences)
            sentences = lang_module.getGraphmathA(sentences)
            BeautySafe.safe_sentences(sentences, 'GraphemathicAnalysis analysis')
            if msg: msg.log('a_graphemath', sentences.getUnit('dict'))

            print('       GM: ', time.time()-t)
            if end_level == self.levels[0]:
                print('    Total: ', time.time()-t1)
                return sentence

        # Морфологический анализ
        if start_level in self.levels[:2]:
            t =time.time()

            sentences = lang_module.getMorphA(sentences)
            with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
                flog.write('\n')
                for index, sentence in sentences: flog.write('sentence: %s\n' % sentence.getUnit('str')['fwords'])
                flog.write('\n')
            BeautySafe.safe_sentences(sentences, 'Morphological analysis')
            if msg: msg.log('a_morph', sentences.getUnit('dict'))

            print('        M: ', time.time()-t)
            if end_level == self.levels[1]:
                print('    Total: ', time.time()-t1)
                return sentences

        # Постморфологичесий
        if start_level in self.levels[:3]: 
            t =time.time()

            sentences = lang_module.getPostMorphA(sentences)
            BeautySafe.safe_sentences(sentences, 'Postmorphological analysis')
            if msg: msg.log('a_postmorph', sentences.getUnit('dict'))

            print('       PM: ', time.time()-t)
            if end_level == self.levels[2]:
                print('    Total: ', time.time()-t1)
                return sentences

        # Синтаксический
        if start_level in self.levels[:4]:
            t =time.time()

            sentences = lang_module.getSyntA(sentences)
            BeautySafe.safe_sentences(sentences, 'Syntactic analysis')
            if msg: msg.log('a_synt', sentences.getUnit('dict'))

            print('        S: ', time.time()-t)
            if end_level == self.levels[3]:
                print('    Total: ', time.time()-t1)
                return sentences

        # извлекаем прямое доп, подл, сказуемое, косв. доп
        if start_level in self.levels[:5]:
            t =time.time()

            #if not isinstance(sentences, ObjUnit.Text): sentences = ObjUnit.Text([sentences])
            for index, sentence in sentences:
                OR.addWordsToDBFromDictSentence(sentence.getUnit('dict'))
                Extract = extractor.Extract(settings['assoc_version'])
                sentences.subunit_info[index] = Extract(sentence) # заменяем объекты предложения на словари извлечений

            print('        E: ', time.time()-t)
            if end_level == self.levels[4]:
                print('    Total: ', time.time()-t1)
                return sentences

        # конвертируем анализы во внутренний язык
        if start_level in self.levels[:6]:
            t =time.time()

            OR = relation.ObjRelation(settings, settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
            _ILs = {}
            for index, sentence in sentences:
                _ILs[index] = []
                Extraction2IL = converter.Extraction2IL(settings['assoc_version'])
                ILs = Extraction2IL(OR, settings, *sentence)
                for IL in ILs: BeautySafe.safe_IL(IL)
                _ILs[index].extend(ILs)

            print('        C: ', time.time()-t)
            if end_level == self.levels[5]:
                print('    Total: ', time.time()-t1)
                return _ILs

    def IL2NL(self, IL):
        #IL = Synthesizer.IL2resultA(IL)
        #result = LangModule.ResultA2NL(IL)
        #return NL
        return IL
