############### Cyan ###############
## Main interface for SC scraping ##

import argparse

from scrapesc import ScrapeSC  # --> TODO: build a single package for this + main [use scrapesc]
from timekeeper import timekeeper


@timekeeper
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link',
                        help='Provide the link to Soundcloud page.')  
    parser.add_argument('-a', '--getart', action='store_true', 
                        help='Specify to retrieve artwork')
    parser.add_argument('-d', '--getdesc', action='store_true', 
                        help='Specify to retrieve description')
    parser.add_argument('-n', '--artist',
                        help="""
                            Provide artist name, if missing from title.
                            Use quotation marks <""> if string contains whitespaces.
                            """) 
    arg = parser.parse_args()
    args = [arg.link, arg.artist, arg.getart, arg.getdesc]
    # --> TODO: Optional argument for custom file save destination [must implement class method in main]
    sc = ScrapeSC(args[0], args[1])
    try:
        print(sc)
    except UnicodeEncodeError:
        print("Cannot Display :(")
    if args[2]:
        sc.get_artwork()
    if args[3]:
        sc.get_desc()
    print("File(s) downloaded")


if __name__ == '__main__':
    main()

# TODO: try implementing asyncio at some point