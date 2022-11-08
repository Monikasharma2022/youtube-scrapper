import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import request
from bs4 import BeautifulSoup
from pytube import YouTube
import base64
from logger import App_Logger
from comment import comment_scrapper
from s3_url import s3

class fetch_urls:
    def __init__(self):
        self.logger = App_Logger()
        self.driver_path = r'chromedriver.exe'
        self.file_object = open("Scrapper_logs", 'a+')

    def get_video_links(self, max_url_to_fetch):
        try:
            self.logger.log(self.file_object, "inside get_video_links method of fetch_url module")

            with webdriver.Chrome(executable_path= self.driver_path) as wd:
                wd.maximize_window()  # optional
                utube_channel_link = request.form['content']
                wd.get(utube_channel_link)
                time.sleep(2)
                url_count = 0
                all_links = []
                while url_count < max_url_to_fetch:
                    page = wd.find_element_by_tag_name("html")
                    page.send_keys(Keys.END)
                    all_video_list = wd.find_elements_by_css_selector(
                        "#dismissible.style-scope.ytd-grid-video-renderer ytd-thumbnail.style-scope.ytd-grid-video-renderer a#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail")
                    all_links = list(dict.fromkeys(map(lambda a: a.get_attribute('href'), all_video_list)))
                    url_count = len(all_links)

                    self.logger.log(self.file_object, "succefully found %s links" %max_url_to_fetch)

                    if url_count > max_url_to_fetch:
                        return all_links[0:max_url_to_fetch]
                return all_links

        except Exception as e:
            # print(e)
            self.logger.log(self.file_object, "Error while get_video_links: %s" %e)



    def fetch_details(self, url):
        try:
            self.logger.log(self.file_object, "enter inside fetch_details function")
            Y = YouTube(url)
            youtuber_name = Y.author
            video_link = url
            video = Y.streams.filter(file_extension='mp4')
            vid_file = video[0].download()
            self.logger.log(self.file_object, "video downloaded seccesfully")
            s3_link = s3.upload_s3(self, vid_file)

            self.logger.log(self.file_object, "successfully got s3_bucket presigned_url for video")

            option = webdriver.ChromeOptions()
            option.add_argument("--headless")
            with webdriver.Chrome(executable_path=self.driver_path, options=option) as wd:
                wd.get(url)
                time.sleep(5)
                soup = BeautifulSoup(wd.page_source, "html5lib")
            try:
                likes = soup.select_one("#top-level-buttons-computed a yt-formatted-string").text
                self.logger.log(self.file_object, "successfully got number of likes on video")

            except Exception as e:
                print('The Exception message is: ', e)
                likes = "NaN"

            title = Y.title
            thumbnail_url = Y.thumbnail_url
            thumbnail = base64.b64encode(requests.get(thumbnail_url).content)
            comment_list, commentor_names_list, no_of_comments = comment_scrapper.ScrapComment(self, url)

            self.logger.log(self.file_object, "successfully got all the details on video")

            return youtuber_name, video_link, likes, no_of_comments, title, s3_link, thumbnail, comment_list, commentor_names_list


        except Exception as e:
            self.logger.log(self.file_object, "Error while fetch_details: %s" %e)

