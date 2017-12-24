import os
from MakeHtmlIndex import gen_index_html
from MakeHtmlTable import generate_html_page

if __name__ == "__main__":
    season = int(os.getcwd().split(os.sep)[-1][2:])
    for day in range(1,26):
        generate_html_page(season, day)
    gen_index_html(season)
