from flask import Flask, render_template, request
from flask_cors import cross_origin
from db import db_operations
from fetch_url import fetch_urls
from logger import App_Logger


app = Flask(__name__)
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/channel',methods=['POST','GET'])
@cross_origin()
def index():
    try:
        logger = App_Logger()  # object initialization of App_Logger() class
        file = open("Scrapper_logs", 'a+')
        logger.log(file, "inside channel route")

        fetch = fetch_urls()  # object initialization of fetch_urls class
        all_links = fetch.get_video_links(2)  # give no of video for which links to fetch

        logger.log(file, "now entering into loop for links in all_links")

        for link in all_links:
            youtuber_name, video_link, likes, no_of_comments, title,s3_link, thumbnail, comment_list, commenter_names_list = fetch.fetch_details(
                link)
            print(youtuber_name, video_link, likes, no_of_comments, title, s3_link, thumbnail, comment_list,
                  commenter_names_list)
            logger.log(file, "all the details are fetch as: %s %s %s %s %s %s %s %s %s %s" %(youtuber_name, video_link, s3_link, likes, no_of_comments, title, s3_link, thumbnail, comment_list, commenter_names_list))

            db_op = db_operations()  # object initialization of db_operations class
            db_op.dump_sql(youtuber_name, video_link, title, s3_link, likes, no_of_comments)
            logger.log(file, "dump details into my_sql database successful")

            db_op.dump_mongo_db(comment_list, commenter_names_list, thumbnail)
            logger.log(file, "dump data into mongo_db successful")

            return "succesfully done"

    except Exception as e:
        print("exception message is :", e)
        return 'something is wrong'



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True, port = 5002)


# https://www.youtube.com/krishnaik06/videos
# https://www.youtube.com/Telusko/videos
# https://www.youtube.com/HiteshChoudharydotcom/videos
# https://www.youtube.com/saurabhexponent1/videos

