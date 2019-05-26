######### Cyan #########
## Soundcloud Scraper ##

import os
import re
import sys
import urllib.request
from functools import lru_cache
from unicodedata import normalize

import pyperclip
import requests
from bs4 import BeautifulSoup


class ScrapeSC:

    MY_PATH = 'C:\\Users\\Dyan\\Desktop\\Musique\\'
    S_URL = 'https://soundcloud.com/'

    def __init__(self, link=None, artist=None):
        """ 
        Initialises instance of ScraperSC class.
        If Soundcloud link is not explicitly given, it will search for it in the system clipboard.
        An exception is raised if non-valid SC link is given (either case) and exits the program.
        When a valid SC link is given, 'requests' will fetch the html doc, which is then parsed to
            'BeautifulSoup'.
        """        
        self.link = link
        self.artist = artist
        self.soup = None    
        if self.link:
            self.url = self.link            
        else:
            self.url = pyperclip.paste()       
        if ScrapeSC.S_URL in self.url:
            r = requests.get(self.url)
            self.soup = BeautifulSoup(r.content, 'html.parser')
        else:
            print(f"Copy a valid SoundCloud link",
                  f"String given: {self.url}", sep='\n')
            sys.exit()
           
    
    @lru_cache(maxsize=2)
    def _get_title(self):
        """Obtains the title of the song from the Soundcloud page"""
        # Implement regex search here --> implemented [21/10/2018]; can be improved
        title = self.soup.find('meta', property='og:title').get('content')
        title = normalize('NFC', title)
        char_list = [':', '/', '|', '\\']
        if any(charc in char_list for charc in title):               # Remove any bad prefix or suffix
            re1 = r'(\w*\s*\w*\s*(:|/|\||\\)*\s*(:|/|\||\\)*\s*)'    # Prefix (if any)
            re2 = r'(?P<t>(.*)[^:*\s*/*\\*])'                        # Main + excluding suffix (if any)            
            pattern = re.compile(re1 + re2)                      
            re_title = re.search(pattern, title)
            return re_title.group('t')
        return title

        # Old code --> Crap
        """
        if ':' in title or '/' in title:
            for i, k in enumerate(title):
                if ':' in k:
                    return title[i+2:]
                elif '/' in k:
                    return title[i+3:]
        return title
        """
    
    @lru_cache(maxsize=2)
    def get_title(self):
        """Checks if artist's name is provided and prepend to existing title"""
        try:  # Manual input in case of error --> until better method is found
            if self.artist:
                return f"{self.artist} - {self._get_title()}"
            # elif #### 
            # TODO: implement direct command line overwrite   
            else:
                return self._get_title()
        except UnicodeEncodeError as err:
            print(f"Error in parsing title: {err}",
                  f"Key in manually.", sep='\n')
            title = input('> ')
            return title

    
    @lru_cache(maxsize=2)
    def get_full_filename(self):
        """Gets rid of bad characters in filenames"""
        filename = self.get_title()
        char_list = [':', '"', '*', '/', '|', '\\', '?', '<', '>']
        if any(char in char_list for char in filename):
            for char in char_list:
                filename = filename.replace(char, '_')
        full_filename = os.path.join(ScrapeSC.MY_PATH, filename)
        return full_filename


    def get_artwork(self):
        """Retrieves the artwork from the SC page and saves it to $MY_PATH$"""
        img_url = self.soup.find('meta', property='og:image').get('content')
        urllib.request.urlretrieve(img_url, f"{self.get_full_filename()}.jpg")
    
    
    def get_desc(self):
        """Retrieves the text description from the SC page and saves the content to
           a text file in $MY_PATH$"""
        desc = self.soup.find('meta', itemprop='description').get('content')
        with open(f"{self.get_full_filename()}.txt", 'w', encoding='utf-8') as f:
            f.write(desc)


    def __str__(self):
        return f"Title:\n{self.get_title()}"


# end of class
# --------------------------------------------------------------------------------------  

# In-script use only (without timekeeper.py):
def _timekeeper(func):
    def wrapper():
        start = _time()
        func()
        end = _time()
        timer = 1000 * (end-start) # in milliseconds
        print(f"{'-'*11} Execution time: {timer:.0f} ms {'-'*11}")
        print("Finished executing block".center(50), " -+- "*10, sep='\n', end='\n\n')
    return wrapper

@_timekeeper
def _main():
    sc = ScrapeSC()
    try:
        print(sc.get_title())
    except UnicodeEncodeError:
        print("Cannot Display")
    #sc.get_artwork()
    #sc.get_desc()
    print("File(s) downloaded")

if __name__ == '__main__':
    from time import perf_counter as _time
    _main()
