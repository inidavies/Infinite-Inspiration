import pandas as pd
import sqlalchemy as db
from images import get_images
import os


def create_database():
    engine = db.create_engine("sqlite:///boards.db")
    return engine
    
all_boards = []
board_num = 0

def create_table(engine, theme):
    global board_num #access board_num on line 15
    board_num += 1 #increment board num (key)
    data = get_images(theme) #get data (value)
    all_boards.append(data) #create k-v pair and add to all_boards dict
    df = pd.DataFrame(data) #create dataframe for board
    df.to_sql(str(board_num), con=engine, if_exists='replace', index=False) #transform dataframe into table
    return data

def previous_boards():
    all_boards_reversed = list(reversed(all_boards)) #reverse all_boards
    return all_boards_reversed

#whenever someone connects to our website, call this function
def delete_database(engine):
    engine.dispose()
    os.remove('boards.db')