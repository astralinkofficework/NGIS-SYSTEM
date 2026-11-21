import sqlite3
con = sqlite3.connect('.data/security.sqlite3')
cur = con.cursor()
cur.execute('DELETE FROM ip_restrictions')
con.commit()
print("ip_restrictions cleared!")
con.close()
