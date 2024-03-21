import sqlite3
from datetime import datetime

def get_sensor_data(number_of_rows):

    query ="""SELECT * FROM sensor ORDER BY datetime DESC;"""
    datetimes= []
    error = []
    ppm1 = []
    ppm2 = []
    ppm3 = []
    latitude = []
    longtitude = []
    id = []



    try:
        conn = sqlite3.connect("/var/www/html/flask/database/ppm_database.db")
        cur=conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in reversed(rows):
            ppm1.append(row[0])
            ppm2.append(row[1])
            ppm3.append(row[2])
            latitude.append(row[3])
            longtitude.append(row[4])            
            datetimes.append(row[7])
            error.append(row[5])
            id.append(row[-1])
            
        return ppm1, ppm2, ppm3, latitude, longtitude, error, datetimes, id
        
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"error occured {e}")
    finally:
        conn.close()


get_sensor_data(100)