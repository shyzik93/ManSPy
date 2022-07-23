class Relation:
    dct_speeches = {'noun': 1, 'verb': 2, 'adjective': 3, 'adverb': 4}
    
    def __init__(self, settings):
        self.c, self.cu = settings.c, settings.c
        self.db = settings.database

    ### Составные функции для таблицы relations (работают с идентификаторами)

    def add_words2samegroup(self, id_type, id_speech, isword, id_word, *id_words):
        ''' Добавляет все id_words в ту группу, в которой находится id_word.
            Если id_word не входит ни в одну группу, то оно добавится в новую группу'''
        id_groups = self.db.get_groups_by_word(id_type, isword, id_word, id_speech)
        if not id_groups:
            self.db.add_words2group(id_type, id_speech, None, isword, id_word)
            id_groups = self.db.get_groups_by_word(id_type, id_speech, isword, id_word)
        for id_group in id_groups:
            self.db.add_words2group(id_type, id_speech, id_group, isword, *id_words)

    def get_words_from_samegroup(self, id_type, id_speech, isword, id_word):
        ''' Возвращает слова из той группы, в которую входит id_word ''' #работает медленно
        id_groups = self.db.get_groups_by_word(id_type, isword, id_word, id_speech)
        id_words = []
        for id_group in id_groups:
            res = self.db.get_words_by_group(id_type, id_group, isword, id_speech)
            if res: id_words.extend(res)
        return list(set(id_words))

    def is_word_in_group(self, id_type, id_group, id_word, isword, id_speech=None):
        ''' Входит ли слово в группу? '''
        id_words = self.db.get_words_by_group(id_type, id_group, isword, id_speech)
        return self.db.word2id(id_word) in id_words

    def get_commongroups(self, id_type, id_speech, *pairs):
        ''' Возвращает общие для всех слов группы '''
        # pair = [id_word, isword]
        list_groups = []
        for pair in pairs:
            list_groups.append(self.db.get_groups_by_word(id_type, pair[1], pair[0], id_speech))

        common_id_groups = set(list_groups.pop(0))
        for list_group in list_groups:
            common_id_groups &= set(list_group)
        return list(common_id_groups)

    # Работа с таблицей descr_relation

    def add_descr_relation(self, **descr):
        self.cu.execute("INSERT INTO descr_relation (count_members, type_relation, name1, name2) VALUES (?,?,?,?)" , (descr['count_members'],descr['type_relation'], descr['name1'], descr['name2']))
        self.c.commit()

    def get_descr_relation(self, relation=None):
        if relation is not None:
            #name = 'name1' if isinstance(relation, (str, unicode)) else 'id_relation'
            #descr = self.cu.execute("SELECT * FROM descr_relation WHERE "+name+"=?", (relation,)).fetchall()
            if isinstance(relation, str): descr = self.cu.execute("SELECT * FROM descr_relation WHERE name1=? OR name2=?", (relation,relation)).fetchall()
            else: descr = self.cu.execute("SELECT * FROM descr_relation WHERE id_relation=?", (relation,)).fetchall()
            descr = [dict(row) for row in descr]
            return descr[0] if descr else {}
        else:
            descr = self.cu.execute("SELECT * FROM descr_relation").fetchall()
            descr = [dict(row) for row in descr]
            return descr if descr else []


class ObjRelation:
    """ Надкласс, реализующий высокий уровень работы с разными группами слов, абстрагируясь от БД.
        Другими словами, он задествует вышеуказанные классы для реализации своих
        функций."""
    def __init__(self, settings):
        self.R = Relation(settings)
        self.db = settings.database

        # Добавление описания семантических отношений
        self.R.add_descr_relation(type_relation='line', count_members='N', type_peak='index', type_child='word',  name1='synonym',   name2=None)
        self.R.add_descr_relation(type_relation='line', count_members=2,   type_peak='index', type_child='group', name1='antonym',   name2=None)
        self.R.add_descr_relation(type_relation='tree', count_members='N', type_peak='word',  type_child='both',  name1='hyperonym', name2='hyponym')

    def get_groups_by_word(self, id_type, isword, id_word, id_speech=None):
        return self.db.get_groups_by_word(id_type, isword, id_word, id_speech)

    def _isRelBetween(self, relation, *words):
      ''' Is the relation 'relation' between word1 and word2 ?
          Являются ли слова word1 и word2 relation'ами (синониами, антонимаими, гиперонимом и гипонимом соответственно, холонимом и меронимом соответственно) ?
      '''
      if isinstance(relation, dict): descr, relation = (relation, relation['id_relation'])
      else: descr = self.R.get_descr_relation(relation)

      if descr['type_relation'] == 'line':
          _words = [[word, 0] for word in words]
          return self.R.get_commongroups(relation, None, *words)
      elif descr['type_relation'] == 'tree':
          #res = {words.pop(0):{'parent': None}}
          for index, word in enumerate(words):
              if index == 0: continue
              if not self.R.is_word_in_group(relation, words[index-1], word, 0, None): return False
          return True

    def _isAnyRelBetween(self, word1, words2):
        ''' Is any relation 'relation' between word1 and word2 ?
            Есть ли какие-либо отношения между словами word1 и word2 ?
        '''
        relations = []
        descrs = self.R.get_descr_relation()
        for descr in descrs:
            relation = descr['id_relation']
            if self.isRelBetween(relation, word1, word2): relations.append(relation)
        return relations

    def _whomRelBetween(self, relation, word1):
      ''' With whom does word1 has relation
      '''
      pass

    def _whatRelBetween(self, word1, word2):
      ''' what relation or relations are between word1 and word2 ?
      '''
      pass

    def _getRelation(self, relation, word1, word2=None):
        ''' Первое слово для иерархиских отношений должно быть выше уровня  '''
        if relation is not None: descr = self.R.get_descr_relation(relation)

        if word1 is not None and word2 is not None:

            if relation is not None: # Is the relation between word1 and word2 ?
                return self.isRelBetween(relation, word1, word2)
            elif relation is None: # Is any relation between word1 and word2 ?
                pass

        elif word1 is not None and word2 is None:

            if relation is not None: # With who does word1 have the relation ?
                pass
            elif relation is None: # With who does word1 have any relation ?
                pass

    def _setRelation(self, relation, word1, word2):
        descr = self.R.get_descr_relation(relation)
        if descr['type_relation'] == 'line':
            if descr['count_members'] == 'N':
                if descr['type_peak'] == 'index':
                    #self.R.is_word_in_group(self, id_type, id_group, id_word, isword, id_speech=None)
                    id_group = self.db.add_words2group(relation, None, None, 0, word1)
                    self.R.add_words2samegroup(relation, None, 0, word1, word2)
                    #self.db.add_words2group('synonym', None, id_group, 0, word2)
        elif descr['type_relation'] == 'tree':
            if descr['count_members'] == 'N':
                pass

    # Временные функции-обёртки, для понимания задачи.
    def isRelBetween(self, relation, word1, word2):
        ''' Is the relation 'relation' between word1 and word2 ?
            Являются ли слова word1 и word2 relation'ами (синониами, антонимаими, гиперонимом и гипонимом соответственно, холонимом и меронимом соответственно) ?
            @return bool
        '''
        if relation == 'hyperonym':
            return self.R.is_word_in_group('hyperonym', word1, word2, 0, None)
        elif relation == 'synonym':
            pass
        elif relation == 'antonym':
            antonyms = self.whomRelBetween('antonym', word1)
            return word2 in antonyms

    def isAnyRelBetween(self, word1, words2):
        ''' Is any relation 'relation' between word1 and word2 ?
            Есть ли какие-либо отношения между словами word1 и word2 ?
            @return bool
        '''
        pass

    def whatRelBetween(self, word1, word2):
        ''' what relation or relations are between word1 and word2 ?
            @return list of relations
        '''
        pass

    def whomRelBetween(self, relation, word1):
        ''' With whom does word1 has relation
            @return list of words
        '''
        if relation == 'synonym':
            return self.db.convert(self.R.get_words_from_samegroup('synonym', None, 0, word1))
        elif relation == 'antonym':
            syn_groups = self.db.get_groups_by_word('synonym', 0, word1, None)
            if not syn_groups: return []
            syn_groups = self.R.get_words_from_samegroup('antonym', None, self.R.dct_types['synonym'], syn_groups[0])
            if not syn_groups: return []
            return self.db.convert(self.db.get_words_by_group('synonym', syn_group, 0, None))


    def setRelation(self, relation, *words):
        """ По умолчанию передаются два слова (корень или идентификатор), но для некоторых отношений можно передовать много слов """
        words = list(words)
        if relation == 'hyperonym': # первое слово - гипероним, остальные- гипонимы. Минимм - два слова.
            word_group = words.pop(0)
            self.db.add_words2group('hyperonym', None, word_group, 0, *words)


        elif relation == 'synonym': # все слова - синонимы. Минимум - одно слово. Возвращает идентификатор синонимичной группы
            ''' Если слово одно, то добавляем его группу и возвращаем её идентификатр. Если слово уже в группе, то возвращаем её идентификатор.
                Если слов несколько, то идентификатор группы, в кторую входит слово, добавляем в список. Если группы нет, то добавляем None.
                  1. Если в списке все группы - None, то первое слово добавляем в новую группу, куда добавляем и остальные слова.
                  2. Если кроме None в списке есть равные идентификаторы групп, то к этой группе добавляем все слова, у которых ещё нет групп.
                  3. Если кроме None в списке есть неравные идентификаторы групп, то слова с отсутсвующии группами добавляем в ту группцу, имеющую большее кол-во повторений в списке.
            '''
            #groups = [self.db.get_groups_by_word('synonym', 0, word, 'verb') for word in words if len(word) != 0]
            #if not groups: group = self.R.add_words2group('synonym', 'verb', None, 0, words.pop(0)) # 1. ...

            # получаем идентификатор группы
            word = words.pop(0)
            _groups = self.db.get_groups_by_word('synonym', 0, word, 'verb')
            if _groups: group = _groups[0]
            else: group = self.db.add_words2group('synonym', 'verb', None, 0, word)

            # добавляем синонимы
            for word in words: 
                self.db.add_words2group('synonym', 'verb', group, 0, word)
            return group

        elif relation == 'antonym': # только два первых слова противопоставляются. Остальные - игнорируются. Всего - ровно два слова.
            word1 = words.pop(0)
            word2 = words.pop(0)
            self.db.add_words2group('antonym', None, word1, 0, word2)
          

if __name__ == '__main__':
    # TODO: Написать тесты для модуля семантических отношений
    # TODO: При сохранении ФАСИФа в базу также сохаранять данные для всех языков.
    # TODO: Для каждого языка заводить не отдельную базу, а отдельную таблицу в базе. Для всех языков одна база
    R = Relation('Esperanto')

    rng = range(1, R.db.relation.get_max_id('id_type')+1)
    for id_type in rng:
        #print R.dct_typesR[id_type]
        res = R.cu.execute('SELECT id_group, id_word, isword FROM relations WHERE id_type=? ORDER BY id_group;', (id_type,)).fetchall()
        #res = list(set(res))
        #print len(res)
        for id_group, id_word, isword in res:
            #if R.dct_typesR[id_type] in ('abstract'): id_group = R.convert(id_group)[0]
            if isword == 0: id_word = R.db.convert(id_word)[0]
            if isword > 0: isword = R.db.dct_typesR[isword]
            else: isword = u'слово'
            print('  ', id_group, id_word, isword)
    
    """list_words = ['dom', 'kot', 'kosxar', 'aparat', 'montr', 'sobak', 'peos']
    R.add_word(list_words)
    print u"Добавили слова в базу. Их id:", R.convert(*list_words)

    lst = ['kot', 'kosxar']
    id_group = R.add_words2group('synonym', 'noun', None, 0, *lst)
    print u"Добавили слова в группу:", lst, id_group

    lst = ['sobak', 'peos']
    id_group = R.add_words2group('synonym', 'noun', None, 0, *lst)
    print u"Добавили слова в группу:", lst, id_group

    word = 'sobak'
    R.add_words2samegroup('synonym', 'noun', 0, word, 'aparat')
    print u"Все слова в группе с %s" % word, R.convert(*R.get_words_from_samegroup('synonym', 'noun', 0, word))
    print u"Все слова в группе %s" % id_group, R.convert(*R.get_words_by_group('synonym', id_group, 0, 'noun'))
    print u"Все группы, куда входит слово %s:" % word, R.get_groups_by_word('synonym', 0, word, 'noun')
    print u"Слово %s в группе %s?" % (word, id_group), R.is_word_in_group('synonym', id_group, word, 0, 'noun')
    print R.get_commongroups('synonym', 'noun', [word, 0], [lst[1],0], [R.convert('aparat')[0], 0])"""
