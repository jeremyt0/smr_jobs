import sqlite3



class Database(object):

    instance = None

    @staticmethod
    def getInstance():
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance

    def __init__(self):
        super().__init__()

        self.database_path = 'db/database.sql'
        self.connection = sqlite3.connect(self.database_path)

        company_table_query = ''' CREATE TABLE IF NOT EXISTS COMPANY(
                                    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    company_name TEXT NOT NULL); 
                                '''

        jobs_table_query = ''' CREATE TABLE IF NOT EXISTS JOB(
                                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                job_title TEXT NOT NULL,
                                FOREIGN KEY(company_id) REFERENCES COMPANY(company_id));
                            '''

        self.create_table(company_table_query)
        self.create_table(jobs_table_query)


    def save_and_quit(self):
        try:
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            # utils.print_to_log(e)
            return False
        # utils.print_to_log("Database saved and closed.")
        print("Database saved and closed.")
        return True

    def create_table(self, query):
        try:
            c = self.connection.cursor()
            c.execute(query)
        except Exception as e:
            # utils.print_to_log(e)
            return False
        return True