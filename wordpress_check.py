import re
import random
import requests
from bs4 import  BeautifulSoup, Comment

class wordPress():
    url = {}
    version = {}
    plugins = {}
    thema = {}
    agent = False

    def __init__(self, url, user_agent):
        self.url            = url
        self.agent          = user_agent
        self.clean_Url()
        self.random_Agent()
        self.check_if_Wordpress()
        self.wp_Themes()



    def  clean_Url(self):
        start_clean_Url = re.sub('(https:\/\/www.)|(http:\/\/www)|(www)|(https?:|)\/\/|(http)', '', self.url)
        start_clean_Url = re.sub('\/.*', '', start_clean_Url)
        cleaned_Url = "https://" + start_clean_Url + "/"
        return cleaned_Url

    def random_Agent(self):


        if self.agent != "random_agent":
            head =[
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
            ]
            headers = {'user-agent': random.choice(head)}
            return headers
        else:
            print("yo")
            pass
    def check_if_Wordpress(self, ):
        wp_checker = ''
        response =requests.get(self.clean_Url(), headers =self.random_Agent())
        if response.status_code == 200:
            if not "wp-" in response.text:
                wp_checker = "False"
            else:
                wp_checker ="True"
        return wp_checker

    def wp_Version(self):
        response = requests.get(self.clean_Url())
        soup = BeautifulSoup(response.text, "html.parser")
        b = str(soup.find_all("meta", attrs={'name': 'generator'}))
        b = re.search("(WordPress \d.\d.\d)", b, flags=0)
        return b.group()

    def wp_Themes(self):
        wp_theme_list = []
        wp_theme = wp_theme_list
        response = requests.get(self.clean_Url())
        soup = BeautifulSoup(response.text, "html.parser")
        find_link = soup.find("head")
        if find_link.find_all(text=lambda text: isinstance(text, Comment)) == True:
            for comments in find_link.find_all(text=lambda text: isinstance(text, Comment)):
                soup = BeautifulSoup(comments, "html.parser")
                if soup.find_all('link'):
                    for url in soup.find_all('link'):
                        search = re.search("themes\/.*\/", url['href'])
                        if search == None:
                            pass
                        else:
                            finish = re.sub('(themes.)|(\/.*)', '', search.group())
                            wp_theme_list.append(finish)
                elif soup.find_all('script'):
                    for url in soup.find_all('script'):
                        search = re.search("themes\/.*\/", url['src'])
                        if search == None:
                            pass
                        else:
                            finish = re.sub('(themes.)|(\/.*)', '', search.group())
                            wp_theme_list.append(finish)

                else:
                    pass
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            link = soup.find_all('link')
            for theme in link:
                search = re.search("themes\/.*\/", theme['href'])
                if search == None:
                    pass
                else:
                    finish = re.sub('(themes.)|(\/.*)', '', search.group())
                    wp_theme_list.append(finish)

        return ','.join(map(str, wp_theme))
    def wp_Plugin(self):
        pass




    def display_Information(self):
        if self.check_if_Wordpress() == "True":
            print("URL                   : %s" % self.clean_Url())
            print("WordPress version     : %s" % self.wp_Version())
            print("WordPress theme       : %s" % self.wp_Themes())


        else:
            print("URL     : %s" % self.clean_Url())
            print("Website type:  Is not Wordpress")

WordPress = wordPress("url", "agent")
WordPress.display_Information()
