######### Cyan #########
## Soundcloud Scraper ##

import re
import sys
import urllib.request
from pathlib import Path
from unicodedata import normalize

import pyperclip
import requests
from bs4 import BeautifulSoup


class ScrapeSC:

    MY_PATH = Path.home() / 'Desktop/Musique'
    S_URL = 'https://soundcloud.com/'

    def __init__(self, link=None, artistname=None, overwrite=None):
        """ 
        Initialises instance of ScraperSC class.
        If Soundcloud link is not explicitly given, it will search for it in the system clipboard.
        An exception is raised if non-valid SC link is given (either case) and exits the program.
        When a valid SC link is given, 'requests' will fetch the html doc, which is then parsed to
            'BeautifulSoup'.
        """        
        self.url = link if link else pyperclip.paste()
        self.artist = artistname     
        if ScrapeSC.S_URL in self.url:
            r = requests.get(self.url)
            self.soup = BeautifulSoup(r.content, 'html.parser')
        else:
            print(f"Copy a valid SoundCloud link",
                  f"String given: {self.url}", sep='\n')
            sys.exit()
        self.title = overwrite if overwrite else self.get_title()
        self.filename = self.get_full_filename()

    
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

    
    def get_title(self):
        """Checks if artist's name is provided and prepend to existing title"""
        try:  # Manual input in case of error --> until better method is found
            if self.artist:
                return f"{self.artist} - {self._get_title()}"
            else:
                return self._get_title()
        except UnicodeEncodeError as err:
            print(f"Error in parsing title: {err}",
                  f"Key in manually.", sep='\n')
            title = input('> ')
            return title

    
    def get_full_filename(self):
        """Gets rid of bad characters in filenames"""
        char_list = [':', '"', '*', '/', '|', '\\', '?', '<', '>']
        if any(char in char_list for char in self.title):
            filename = self.title
            for char in char_list:
                filename = filename.replace(char, '_')
            return ScrapeSC.MY_PATH / filename
        else:
            return ScrapeSC.MY_PATH / self.title


    def get_artwork(self):
        """Retrieves the artwork from the SC page and saves it to $MY_PATH$"""
        img_url = self.soup.find('meta', property='og:image').get('content')
        urllib.request.urlretrieve(img_url, f"{self.filename}.jpg")
    
    
    def get_desc(self):
        """Retrieves the text description from the SC page and saves the content to
           a text file in $MY_PATH$"""
        desc = self.soup.find('meta', itemprop='description').get('content')
        with open(f"{self.filename}.txt", 'w', encoding='utf-8') as f:
            f.write(desc)


    def __str__(self):
        return f"Title:\n{self.title}"

    def __repr__(self):
        return f"File(s) saved as {self.filename}[.txt or .png]"
