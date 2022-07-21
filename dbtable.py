import pandas as pd
import sqlalchemy as db
from images import get_images
import os

#just in case server goes down while someone is using our website
if os.path.exists('boards.db'):
    os.remove('boards.db')

def create_database():
    engine = db.create_engine("sqlite:///boards.db")
    return engine
    
all_boards = {}
board_num = 0

def create_table(engine):
    global board_num #access board_num on line 15
    board_num += 1 #increment board num (key)
    data = get_images() #get data (value)
    all_boards[board_num] = data #create k-v pair and add to all_boards dict
    df = pd.DataFrame(data) #create dataframe for board
    df.to_sql(str(board_num), con=engine, if_exists='fail', index=False) #transform dataframe into table

def previous_boards():
    all_boards_reversed = dict(reversed(list(all_boards.items()))) #reverse all_boards
    return all_boards_reversed

#whenever someone connects to our website, call this function
def delete_database(engine):
    engine.dispose()
    os.remove('boards.db')