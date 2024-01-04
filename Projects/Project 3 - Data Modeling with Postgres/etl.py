import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    ETL process of the song and
    artist files. Load them to
    each data table.

    Arguments:
    cur - cursor variable for dbase
    filepath - file path for song and artist files

    Return:
    song data in table
    artist data in table
    """    
    # open song file
    df = pd.read_json(filepath, lines=True, orient='columns')

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)

def drop_dupe_records():
    """
        Drop dupe records from table   
    """
    
    tables = [song_table, artist_table, user_table, time_table, songplay_table]
    key = ['song_id', 'artist_id', 'user_id', 'timestamp', 'songplay_id']
    
    for key, table in zip(keys, tables):
        table.drop_duplicates(subset=[key], inplace=True, ignore_index=True)
        
def process_log_file(cur, filepath):
    """
    ETL processing for the log data.
    To create time, users and song
    data tables.

    Arguments:
    cur - cursor variable for dbase
    filepath - file path for log file

    Return:
    time data in time table
    user data in users table
    songplay data in songplay table
    """    
    # open log file
    df = pd.read_json(filepath, lines=True, orient='columns')

    # filter by NextSong action
    df = df.query("page == 'NextSong'")

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit = 'ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']].copy()
    user_df.columns = ['user_id', 'first_name', 'last_name', 'gender', 'level']
    
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        start_time = pd.to_datetime(row.ts, unit='ms').strftime('%Y-%m-%d %I:%M:%S')
        songplay_data = (start_time, row.userId, row.level, str(songid), str(artistid), row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Data into Directory Structure

    Arguments:
    cur - cursor variable for dbase
    conn -  connection to dbase with (parameters) filepath - file path for processing of data(song_data) / data(log_data)
    func - function for process song data / process log data        

    Return:
    print out of files processed
    """   
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    """
    Connection to dbase, process data for data/song_data and data/log_data

    Arguments: Empty

    Return: Complete dataset being processing into dbase tables
    """          
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()