import time
from bs4 import BeautifulSoup
from selenium import webdriver
from logger import App_Logger


class comment_scrapper:
    def __init__(self):
        self.logger = App_Logger()
        self.driver_path = r'chromedriver.exe'
        self.file_object = open("Scrapper_logs", 'a+')

    def ScrapComment(self, url):
        try:

            self.logger.log(self.file_object, "enter inside scrape_comment function")
            option = webdriver.ChromeOptions()
            option.add_argument("--headless")
            driver = webdriver.Chrome(executable_path=self.driver_path, options=option)
            driver.get(url)
            prev_h = 0
            while True:
                height = driver.execute_script("""
                        function getActualHeight() {
                            return Math.max(
                                Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                                Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                                Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                            );
                        }
                        return getActualHeight();
                    """)
                driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
                # fix the time sleep value according to your network connection
                time.sleep(2)
                prev_h += 200
                if prev_h >= height:
                    break
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            comment_div = soup.select("#content #content-text")
            comment_list = [x.text for x in comment_div]
            commentor_name = soup.select("#author-text span")
            commentor_names_list = [x.text.replace("\n", "").replace("  ", "") for x in commentor_name]
            no_of_comments = len(comment_list)

            self.logger.log(self.file_object, "successful end of scrape_comment function")
            return comment_list, commentor_names_list, no_of_comments

        except Exception as e:
            self.logger.log(self.file_object, "Error while fetch_details: %s" % e)

