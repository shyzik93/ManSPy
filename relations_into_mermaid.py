from manspy.utils.settings import Settings, InitSettings

with InitSettings(), open('res.md', 'w', encoding='utf-8') as f:
    cu = Settings().database.cu

    rels = {}
    for row in cu.execute('SELECT * FROM descr_relation WHERE 1;').fetchall():
        rels[row['id_relation']] = row

    f.write('flowchart TD\n')
    for row in cu.execute('SELECT * FROM words WHERE 1;').fetchall():
        node1 = row['id_word']
        word = row['word']
        f.write(f'    N{node1}[{word}];\n')

    f.write('\n')
    for row in cu.execute('SELECT * FROM relations WHERE 1;').fetchall():
        node1 = row['id_word']
        node2 = row['id_group']
        descr_rel = rels[row['id_type']]
        type_link = descr_rel['name1']

        is_node1_word = 'N'# if row['isword'] else 'G'
        is_node2_word = 'N' if descr_rel['type_parent'] == 'word' else 'G'
        f.write(f'    {is_node1_word}{node1} -->|{type_link}| {is_node2_word}{node2}\n')
