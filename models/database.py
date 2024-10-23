from sqlalchemy import create_engine, Column, String, Integer, Table, MetaData

engine = create_engine('sqlite:///rules.db')
metadata = MetaData()

rules_table = Table('rules', metadata,
    Column('id', Integer, primary_key=True),
    Column('rule', String, nullable=False)
)

metadata.create_all(engine)
