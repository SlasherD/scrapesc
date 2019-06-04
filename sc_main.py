############### Cyan ###############
## Main interface for SC scraping ##

import argparse
import asyncio

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
    parser.add_argument('-n', '--artistname',
                        help="""
                            Provide artist name, if missing from title.
                            Use quotation marks <""> if string contains whitespaces.
                            """)
    parser.add_argument('-o', '--overwrite',
                        help="""
                            Choose to manually overwrite filename (if current text is problematic).
                            Use quotation marks <""> if string contains whitespaces.
                            """) 
    args = parser.parse_args()
    sc = ScrapeSC(args.link, args.artistname, args.overwrite)
    try:
        print(sc)
    except UnicodeEncodeError:
        print("Cannot Display :(")
    if args.getart and args.getdesc:
        async def _main():
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, sc.get_artwork)
            await loop.run_in_executor(None, sc.get_desc)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_main())
    elif args.getart:
        sc.get_artwork()
    elif args.getdesc:
        sc.get_desc()
    print("File(s) downloaded")
    print(repr(sc))


if __name__ == '__main__':
    main()