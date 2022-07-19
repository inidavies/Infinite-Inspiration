import pandas as pd
import sqlalchemy as db
from images import get_images

def board_database():
    data = get_images()
    df = pd.DataFrame(data)
    engine = db.create_engine("sqlite:///test.db")
    df.to_sql('board', con=engine, if_exists='fail', index=False)
    return engine

engine = board_database()
test_table = pd.read_sql_table(table_name='board', con=engine)
print(test_table)