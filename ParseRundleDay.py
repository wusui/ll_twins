from HTMLParser import HTMLParser
from HTMLParser import HTMLParseError
from Reader import reader
from ParseMatch import check_match_info

class RundleDayParse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.key = 0
        self.mdata = {}
    def handle_starttag(self, tag, attrs):
        try:
            self.key = 0
            if tag == u"a":
                for atp in attrs:
                    if atp[0] == 'href':
                        if atp[1].startswith('/match.php?id='):
                            partz = atp[1].split("=")
                            self.key = int(partz[1])
        except HTMLParseError:
            print 'parse error'
    def handle_data(self, data):
        if self.key != 0:
            if data.find("(") > 0:
                if self.key in self.mdata:
                    self.mdata[self.key].append(data)
                else:
                    self.mdata[self.key] = [data]
    def ret_value(self):
        retv = []
        for keyv in self.mdata.keys():
            if self.mdata[keyv][0] == self.mdata[keyv][1]:
                retv.append(keyv)
        return retv

def get_matches_for_rundle_day(season, rday, rundle):
    info = reader(u"https://learnedleague.com/match.php?%d&%d&%s" % (season, rday, rundle))
    parsev = RundleDayParse()
    parsev.feed(info)
    return parsev.ret_value()

def get_results_for_rundle_day(season, rday, rundle):
    matches = get_matches_for_rundle_day(season, rday, rundle)
    retv = []
    for match in  matches:
        res = check_match_info(match)
        if res:
            retv.append(res)
    return retv

if __name__ == "__main__":
    print get_results_for_rundle_day(75, 7, "B_Pacific")
    print get_results_for_rundle_day(75, 8, "B_Pacific")
