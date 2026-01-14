import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.is_cloud_run = os.environ.get("K_SERVICE") is not None

        if self.is_cloud_run:
            self.unix_socket = "/cloudsql/portfolio-website-484305:us-central1:resume-db"
        else:
            self.host = "127.0.0.1"
            self.port = 3306

        self.database       = 'db'
        self.user           = 'master'
    
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills']
        
    # create connection to database
    def query(self, query = "SELECT * FROM users", parameters = None):

        if self.is_cloud_run:
            cnx = mysql.connector.connect(
            user=self.user,
            password=self.password,
            unix_socket=self.unix_socket,
            database=self.database,
            charset='latin1'
            )
        else:
            cnx = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
                charset='latin1'
            )

        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
            
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        # if purge true drop tables (reverse order due to foreign key relations (don't break referential integrity))
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # execute sql queries for each table to create them
        for table in self.tables:
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data from each coresponding csv file
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()   
                # pars rows into parameters list         
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # first row is column names, rest is data
                cols = params[0]
                params = params[1:] 

                # inset data into newly created table
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        # check if we are inserting many rows or one
        has_multiple_rows = any(isinstance(el, list) for el in parameters)

        # creates list of placeholders
        keys, values = ','.join(columns), ','.join(['%s' for x in columns])
        
        # creates insert query for data
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """

        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        # execute query and return ID of last inserted row
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id


    def getResumeData(self):
        """
        Retrieves all resume data from database.
        Returns nested dictionary structure of institutions -> positions -> experiences -> skills
        Used for dynamically rendering resume page.
        """
        # get all insitutions
        institutions = self.query("""
            SELECT * FROM institutions
            ORDER BY inst_id
        """)        
        resume_data = {}
        
        # build nested dictionary structure
        for inst in institutions:
            inst_id = inst['inst_id']

            # add institution data
            resume_data[inst_id] = {
                'address': inst['address'],
                'city': inst['city'],
                'state': inst['state'],
                'type': inst['type'],
                'zip': inst['zip'],
                'department': inst['department'],
                'name': inst['name'],
                'positions': {}
            }
            
            # get positions for this institution
            positions = self.query("""
                SELECT * FROM positions 
                WHERE inst_id = %s 
                ORDER BY position_id
            """, (inst_id,))
            
            # add position data
            for pos in positions:
                pos_id = pos['position_id']
                resume_data[inst_id]['positions'][pos_id] = {
                    'end_date': pos['end_date'],
                    'responsibilities': pos['responsibilities'],
                    'start_date': pos['start_date'],
                    'title': pos['title'],
                    'experiences': {}
                }
                
                # get experiences for this position
                experiences = self.query("""
                    SELECT * FROM experiences 
                    WHERE position_id = %s 
                    ORDER BY experience_id
                """, (pos_id,))
                
                # add experience data
                for exp in experiences:
                    exp_id = exp['experience_id']
                    resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                        'description': exp['description'],
                        'hyperlink': exp['hyperlink'],
                        'name': exp['name'],
                        'skills': {}
                    }
                    
                    # get skills for this experience
                    skills = self.query("""
                        SELECT * FROM skills 
                        WHERE experience_id = %s 
                        ORDER BY skill_id
                    """, (exp_id,))
                    
                    # add skill data
                    for skill in skills:
                        skill_id = skill['skill_id']
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                            'name': skill['name'],
                            'skill_level': skill['skill_level']
                        }
        
        return resume_data

