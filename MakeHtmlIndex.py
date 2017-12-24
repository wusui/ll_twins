import json
from GetMatchData import CATEGORIES
from GetMatchData import JSON_FILENAME_FMT
from MakeHtmlTable import convert_wrapper

def get_table_counts():
    count = {}
    for day in range(1,26):
        fname = JSON_FILENAME_FMT % day
        try:
            with open(fname) as data_file:
                data = json.load(data_file)
                this_day = {}
                for field in CATEGORIES:
                    this_day[field] = len(data[field])
                count[day] = this_day
        except EnvironmentError:
            break
    return count

def wrap_html(index_lines, index_text, season):
    html = []
    with open(index_text) as data_file:
        idata = data_file.read()
    html.append(idata % (season, season))
    html.append(index_lines)
    html.append('</body>')
    html.append('</html>')
    return '\n'.join(html)

def gen_index_html_in(season):
    data = get_table_counts()
    total = {}
    for lbl in CATEGORIES:
        total[lbl] = 0
    all_txt = []
    for day in range(1,26):
        if not day in data.keys():
            break
        nline = ['<a href="./ll%d_similarity_matchday_%d.html">' % (season, day)]
        nline.append("Day %d: (" % day)
        inparens = []
        for clause in CATEGORIES:
            txt = convert_wrapper(clause, {"format": "capitalize,space"})
            numb = data[day][clause]
            total[clause] += numb
            comb_txt = "%s %d" % (txt, numb)
            inparens.append(comb_txt)
        nline.append(', '.join(inparens))
        nline.append(')</a><br>')
        ftxt = ''.join(nline)
        all_txt.append(ftxt)
    all_txt.append("<h2>TOTALS</h2>")
    for clause in CATEGORIES:
        txt1 = convert_wrapper(clause, {"format": "capitalize,space"})
        otxt = "%s: %d<br>" % (txt1,  total[clause])
        all_txt.append(otxt)
    return '\n'.join(all_txt)

def gen_index_html(season):
    filename = "ll_index_%d.html" % season
    output = wrap_html(gen_index_html_in(season),"index_text", season)
    with open(filename, 'w') as f:
        f.write(output)
        
if __name__ == "__main__":
    season = 74
    gen_index_html(season)
