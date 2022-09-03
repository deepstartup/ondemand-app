#!/usr/bin/python
import psycopg2
from config import config
#########################################################
class connect:
    def __init__(self,params):
        #conn = None
        self.params = params
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
    def do_select(self,postgres_select_query):
        self.cur.execute(postgres_select_query)
        db_version = self.cur.fetchone()
        print(db_version)
        self.cur.close()
    def do_insert(self,postgres_insert_query,record_to_insert):
        self.postgres_insert_query=postgres_insert_query
        self.record_to_insert=record_to_insert
        self.cur.execute(self.postgres_insert_query, self.record_to_insert)
        self.conn.commit()
        self.count = self.cur.rowcount
        print(self.count, "Record inserted successfully into mobile table")
        self.cur.close()
#########################################################
#if __name__ == '__main__':
    #params_all=config()
    #main_conn=connect(params_all)
    #main_conn.do_select('select * from subscriber_master')
    #main_conn.do_insert(postgres_insert_query,record_to_insert)