from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db').connect()

query = '''
    SELECT * FROM tb_first_app;
'''

df = pd.read_sql_query(text(query), engine)

### E se quisermos criar/deletar tabelas no banco?

query2 = text('''
    insert into tb_artist (
        select
            t1."date",
            t1."rank",
            t1.artist,
            t1.song
        from public."Billboard" as t1
        where t1.artist = 'Nirvana'
        order by t1.artist, t1."date");

''')

engine.execute(query2)