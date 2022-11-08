import mysql.connector as conn
import pymongo
from logger import App_Logger
from my_cred import monngo_connection_string

class db_operations:
    def __init__(self):
        self.logger = App_Logger()
        self.file_object = open("Scrapper_logs", 'a+')

    def dump_sql(self, youtuber_name, video_link, title, s3_link, likes, no_of_comments):
        try:
            self.logger.log(self.file_object, "enter into dump_sql method")

            mydb = conn.connect(host="localhost", user="root", passwd="Monika$9")
            print(mydb)
            cursor = mydb.cursor()
            cursor.execute("create database if not exists python_challenge_project")
            s = "create table if not exists python_challenge_project.youtubers_table(youtuber_name varchar(50), video_link varchar(100),title varchar(500), s3_link varchar(1500), likes varchar(50), no_of_comments varchar(50))"
            cursor.execute(s)
            s = ("insert into python_challenge_project.youtubers_table"
                 "(youtuber_name, video_link, title, s3_link, likes, no_of_comments)"
                 "values (%s, %s, %s, %s, %s, %s)")
            data = (youtuber_name, video_link, title, s3_link, likes, no_of_comments)
            cursor.execute(s, data)
            mydb.commit()

        except Exception as e:
            self.logger.log(self.file_object, "error while dump_sql : %s" %e)


    def dump_mongo_db(self, comment_list, commentor_names_list, thumbnail):
        try:
            self.logger.log(self.file_object, "enter into dump_mongo_db method")
            cluster = pymongo.MongoClient(monngo_connection_string)
            db = cluster.test
            print(db)
            database = cluster['python_project_challenge']
            collection = database['youtubers_collection']
            data = {"comment_list": comment_list,
                    "commentor_names": commentor_names_list,
                    "thumbnail_base_64": thumbnail
                    }
            collection.insert_one(data)
        except Exception as e:
            self.logger.log(self.file_object, "error while dump_mondo_db : %s" %e)


