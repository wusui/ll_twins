import json
from pprint import pprint
from GetMatchData import CATEGORIES
from GetMatchData import JSON_FILENAME_FMT
from GetMatchData import gen_json

xswitch = {"lower": lambda x : x.lower(),
           "upper": lambda x : x.upper(),
           "capitalize": lambda x : x.title(),
           "nothing": lambda x : x}
blankval = {"space": " ", "underscore": "_"}

def convert(txt, ulval, bval):
    return blankval[bval].join(xswitch[ulval](txt).split('_'))

def convert_wrapper(txt, tfmt):
    parts = tfmt["format"].split(",")
    return convert(txt, parts[0], parts[1])

def generate_body_of_html(data, fmat):
    body = []
    body.append("<body>")
    hval = "h%s" % fmat["title"]["size"]
    for category in CATEGORIES:
        title = convert_wrapper(category, fmat["title"])
        body.append("<%s>%s</%s>" % (hval, title, hval))
        body.append("<table class=%s>" % fmat["table"]["css_format"])
        trow = ['<tr>']
        for field in fmat["table"]["columns"]:
            trow.append("<th>%s</th>" % convert_wrapper(field, fmat["header"]))
        trow.append('</tr>')
        body.append(''.join(trow))
        for entry in data[category]:
            trow = ['<tr>']
            for field in fmat["table"]["columns"]:
                trow.append("<td class=%s>" % fmat["cell"]["default_fmt"] )
                trow.append(entry[field])
                trow.append('</td>')
            trow.append('</tr>')
            body.append(''.join(trow))
        body.append("</table>")
    body.append("</body>")
    return '\n'.join(body)

def wrap_html(body, css_text):
    html = ['<html>']
    with open(css_text) as data_file:
        cdata = data_file.read()
    html.append(cdata)
    html.append(body)
    html.append('</html>')
    return '\n'.join(html)

def generate_day_report(jsond):
    with open(jsond) as data_file:
        data = json.load(data_file)
    pprint(data)
    our_fmt = {"title": {"format": "capitalize,space", "size": "2"},
     "header": {"format": "upper,space"},
     "cell": {"default_fmt": "center"},
     "table": {"css_format": "wfmt", "columns": ["rundle", "player_1", "player_2", "score"]}}
    body = generate_body_of_html(data, our_fmt)
    htmlpage = wrap_html(body, "css_text")
    return htmlpage
    
def generate_html_page(season, day):
    fname = JSON_FILENAME_FMT % day
    gen_json(season, fname, day)
    rpt = generate_day_report(fname)
    with open("ll%d_similarity_matchday_%d.html" % (season, day), 'w') as f:
        f.write(rpt)

if __name__ == "__main__":
    day = 17
    season = 75
    generate_html_page(season, day)
