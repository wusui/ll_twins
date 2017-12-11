from HTMLParser import HTMLParser
from HTMLParser import HTMLParseError
from Reader import reader

class AllRundleParse(HTMLParser):
    def __init__(self, season):
        HTMLParser.__init__(self)
        self.llendtxt = "LL%d Leagues" % season
        self.standhead = "/standings.php?%d&" % season
        self.okay = True
        self.lastday = 0
        self.rundles = []
    def handle_starttag(self, tag, attrs):
        try:
            if self.okay:
                if tag == u"a":
                    for apt in attrs:
                        if apt[0] == 'href':
                            if apt[1].startswith(self.standhead):
                                parts = apt[1].split("&")
                                self.rundles.append(parts[-1])
        except HTMLParseError:
            print 'parse error'
    def handle_data(self, data):
        sdata = data.strip()
        if sdata.startswith("As of Match Day"):
            self.lastday = int(sdata.split()[-1])
        if sdata == self.llendtxt:
            self.okay = False
    def ret_value(self):
        retv = {}
        retv['lastday'] = self.lastday
        retv['rundles'] = self.rundles
        return retv

def get_allrundles(season):
    info = reader(u"https://learnedleague.com/allrundles.php?%d" % (season))
    if info.startswith("Season not yet underway."):
        return {}
    parsev = AllRundleParse(season)
    parsev.feed(info)
    return parsev.ret_value()

if __name__ == "__main__":
    rdm = get_allrundles(75)
    print rdm
