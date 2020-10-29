"""
Experimental draft code.
"""

import re

re_expressions_by_entity = {
    'email': [r'[a-z0-9]+', r'[a-z0-9]+@', r'[a-z0-9]+@[a-z0-9]+', r'[a-z0-9]+@[a-z0-9]+\.',
              r'[a-z0-9]+@[a-z0-9]+\.[a-z]+'],
    'url': [r'(?:https?)', r'(?:https?)://', r'(?:https?)://[a-z0-9]+'],
}

entities = ['maillogin@maildomain.ru', 'http://domain.com/path']

for entity in entities:
    for symbol_index in range(len(entity) + 1):
        part_entity = entity[:symbol_index]
        print(part_entity)

        for entity_name, re_expressions in re_expressions_by_entity.items():
            for re_index, re_expression in enumerate(re_expressions):
                weight_of_probability = (re_index + 1) * 100 / len(re_expressions)
                finded = re.findall(re_expression, part_entity)
                if finded and weight_of_probability > 70:
                    print('   ', finded, '{}%'.format(weight_of_probability), entity_name)



