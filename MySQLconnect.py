import mariadb
from MySQLdbconfig import read_db_config
 
 
def connect(filename, section):
    """ Connect to MariaDB SQL database """
 
    db_config = read_db_config(filename, section)
    
    try:
        conn = mariadb.connect(**db_config)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    
    conn.autocommit = False
    return conn
 
 
if __name__ == '__main__':
    connect('config.ini', 'mydb')