from HTMLParser import HTMLParser
from HTMLParser import HTMLParseError
from Reader import reader

class MatchParse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = True
        self.prev_http = ''
        self.prev_points = ''
        self.getfscore = False
        self.count1 = 0
        self.count2 = 0
        self.foundyn = False
    def handle_starttag(self, tag, attrs):
        try:
            self.foundyn = False
            if tag == u"img":
                for itp in attrs:
                    if itp[0] == u"src":
                        if itp[1].startswith("/images/"):
                            if itp[1].endswith("lg.gif"):
                                self.getfscore = True
            if tag == u"td":
                for atp in attrs:
                    if atp[0] == u"class":
                        if atp[1] in ['ind-Yes2', 'ind-No2']:
                            if self.count1 % 2 == 0:
                                self.prev_http = atp[1]
                            else:
                                if atp[1] != self.prev_http:
                                    self.result = False
                            self.count1 += 1
                            self.foundyn = True
        except HTMLParseError:
            print 'parse error'
    def handle_data(self, data):
        if data.find(" v. ") > 0:
            self.result = data
        if self.getfscore:
            if '(' in data:
                self.result += ":" + data.strip()
        if self.foundyn:
            if self.count2 % 2 == 0:
                self.prev_points = data.strip()
            else:
                if data.strip() != self.prev_points:
                    self.result = False
            self.count2 += 1
            self.foundyn = False
    def handle_endtag(self, tag):
        if tag == u"td":
            self.getfscore = False
    def ret_value(self):
        return self.result

def check_match_info(game_no):
    """
    game_no: game number extracted from the LL site.
    
    returns False if this is not a twin game (most cases)
    returns a string consisting of player names separated by "v." and an LL score.
    """
    info = reader(u"http://learnedleague.com/match.php?id=%d" % (game_no))
    parsev = MatchParse()
    parsev.feed(info)
    return parsev.ret_value()

if __name__ == "__main__":
    print check_match_info(1407440)
    print check_match_info(1489209)
