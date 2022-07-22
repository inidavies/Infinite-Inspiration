import pandas as pd
import sqlalchemy as db
from images import get_images
import os


def create_database():
    """Creates database"""
    engine = db.create_engine("sqlite:///boards.db")
    return engine


all_boards = []
board_num = 0


def create_table(engine, theme):
    """Creates table with board information"""
    global board_num
    board_num += 1
    data = get_images(theme)
    if type(data) is list:
        all_boards.append(data)
        df = pd.DataFrame(data)
        df.to_sql(str(board_num), con=engine, if_exists='replace', index=False)
    else:
        return -1
    return data


def previous_boards():
    """Reverses all_boards"""
    all_boards_reversed = list(reversed(all_boards))
    return all_boards_reversed


def delete_database(engine):
    """Deletes database"""
    engine.dispose()
    os.remove('boards.db')
