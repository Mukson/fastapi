import databases
import sqlalchemy
import pandas as pd


DATABASE_URL = "postgresql://root:root@db:5432/bostongene"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
df = pd.read_csv("./signatures.tsv", delimiter='\t').rename({'Unnamed: 0': 'nsclc_name'}, axis=1)
df.columns = map(str.lower, df.columns)
df.to_sql("patients", con=engine, if_exists='replace', index=True)
engine.execute('alter table patients add primary key(index)')
metadata.reflect(bind=engine)
table = metadata.tables['patients']


