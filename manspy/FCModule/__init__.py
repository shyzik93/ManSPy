# -*- coding: utf-8 -*-
''' Модуль-обёртка для интеллекта'''
import time

class LogicKernel():
    def __init__(self):
        pass

    def run_assoc_func(self, arg0, subject, action, arguments, msg):
        """ Вызывает функцию, согласно обстоятелствам вызова """

        r_texts = []

        if action['wcomb_verb_function'] is not None: assoc_type = 'wcomb_verb_function'
        else: assoc_type = 'wcomb_function'

        if action['args_as_list'] == 'l':
            res = action[assoc_type](arg0, *arguments)
            r_texts.append(res)
        else:
            for argument in arguments:
                res = action[assoc_type](arg0, **argument)
                r_texts.append(res)

        r_texts = [r_text for r_text in r_texts if r_text is not None]

        msg.r_texts.extend(r_texts)

    def run_common_func(self, arg0, subject, action, arguments, msg):
        if action['wcomb_verb_function'] is not None:
            for r_text in msg.r_texts: msg.to_IF(r_text)
        else:
            res = action['common_verb_function'](arg0, *msg.r_texts)
            if res is not None: msg.to_IF(res)

    def LogicKernel(self, ILs, msg):
      ''' Главная функция. Работает только с ВЯ '''

      for IL in ILs:
          if IL['error_convert']['argument']: continue
          if not IL: continue

          IL['arg0']['to_IF'] = msg.to_IF

          action = IL['action']
          subject = IL['subject']
          arguments = IL['argument']
          arg0 = IL['arg0']

          if action['mood'] == 'imperative':
              # здесь можно проверить, кто дал приказ
              self.run_assoc_func(arg0, subject, action, arguments, msg)
          elif action['mood'] == 'indicative':
              # яв-предложение должно подаваться в функцию обработки фактов. А эта строчка - временная.
              self.run_assoc_func(arg0, subject, action, arguments, msg)

      self.run_common_func(arg0, subject, action, arguments, msg)

class LogicShell:
    def __init__(self):
        self.LogicKernel = LogicKernel()

    def execIL(self, msg):
        ExecError = []

        for index_sentence, ILs in msg.ils.items():
            for IL in ILs:
                if IL['error_convert']['function']: continue
            if ILs: self.LogicKernel.LogicKernel(ILs, msg)

        return ExecError
