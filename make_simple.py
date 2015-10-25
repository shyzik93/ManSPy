# -*- coding: utf-8 -*-
import repper, simpletools
import os, shutil, re

list_words = simpletools.fopen('words.txt', 'r').split('\n')
list_words = [w for w in list_words if w and w[0] != '#']



def edit_files(rec=0, _path=None, names=None):
  if not rec:
    os.path.walk(main_path+'_simple', edit_files, 1)
    return
  for name in names:
    path = os.path.join(_path, name)  
    if os.path.isfile(path) and path[-3:] == '.py':
      text = simpletools.fopen(path, 'r')

      #if 'list_FASIF' not in text:
      #  text = re.sub(r"'''.*?'''", '', text, flags=re.DOTALL)
      #  text = re.sub(r'""".*?"""', '', text, flags=re.DOTALL)
      #text = re.sub(r"\s*#.*", '', text)
      for w in list_words:
        text = text.replace("'%s'" % w, str(list_words.index(w)))
        text = text.replace('"%s"' % w, str(list_words.index(w)))

      simpletools.fopen(path, 'w', u'# -*- coding: utf-8 -*-\n')
      simpletools.fopen(path, 'a', text)

def make_user_version(main_path):
  simple_path = main_path+'_simple'
  orig_path = main_path
  # копируем
  if os.path.exists(simple_path):
    shutil.rmtree(simple_path)
  shutil.copytree(orig_path, simple_path)
  # редактируем файлы (обфускация)
  edit_files()

if __name__ == '__main__':
  main_path = os.path.abspath('')
  make_user_version(main_path)
