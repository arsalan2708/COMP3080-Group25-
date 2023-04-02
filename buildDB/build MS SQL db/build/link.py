''' Creates and populates two tables one for linking projects
 to the actors and the other to link the crew with the project'''

def createActorsTable(c):
    c.execute('''CREATE TABLE actors(
        tconst varchar(30) not null,
        nconst varchar(30) not null,
        characters varchar(150),
        FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (nconst) REFERENCES people(nconst) ON DELETE CASCADE ON UPDATE CASCADE
        );''')
    c.commit()

def createCrewTable(c):
    c.execute('''CREATE TABLE crew(
        tconst varchar(30) not null,
        nconst varchar(30) not null,
        category varchar(45),
        job varchar(175),
        FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (nconst) REFERENCES people(nconst) ON DELETE CASCADE ON UPDATE CASCADE
        );''')
    c.commit()

def build (conn,path):
    cursor = conn.cursor()
    createActorsTable(cursor)
    createCrewTable(cursor)
    
    print("Building people to project relations")
    with open(path+"rData.tsv") as f:
        f.readline()
        for data in f:
            d = data.strip('\r\n').split('\t')
            d[4] = None if d[4]=='' else d[4]
            d[5] = None if d[5]=='' else d[5].strip('[]')
            if d[3]=='actor':
                cursor.execute(''' INSERT INTO actors 
                VALUES(?,?,?)''',(d[0],d[2],d[5]))
            else:
                cursor.execute(''' INSERT INTO crew 
                VALUES(?,?,?,?)''',(d[0],d[2],d[3],d[4]))
        
        cursor.commit()
    cursor.close()
