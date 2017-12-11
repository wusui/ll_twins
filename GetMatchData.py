from __future__ import print_function
import json
from ParseAllRundles import get_allrundles
from ParseRundleDay import get_results_for_rundle_day

CATEGORIES = ['perfect_defense', 'other_matches', 'forfeits']
def get_all_matches(season, verbose=False, mday=0):
    perfval = ['0(0)', '0(1)', '1(2)', '2(3)', '4(4)', '6(5)', '9(6)']
    ret_val = {}
    for cat in CATEGORIES:
        ret_val[cat] = []
    rdm = get_allrundles(season)
    if mday == 0:
        lrange = range(1,rdm['lastday'])
    else:
        lrange = range(mday, mday+1)
    for day in lrange:
        for rundle in rdm['rundles']:
            result = get_results_for_rundle_day(season, day, rundle)
            if verbose:
                print(season, day, rundle, result)
            for entry in result:
                print(season,  day, rundle, entry)
                mtch_data = entry.split(":")
                sides = mtch_data[0].split(" v. ")
                rval = {}
                rval['season'] = season
                rval['day'] = day
                rval['rundle'] = rundle
                rval['player_1'] = sides[0].strip()
                rval['player_2'] = sides[1].strip()
                rval['score'] = mtch_data[-1]+"-"+mtch_data[-1]
                if not mtch_data[-1] in perfval:
                    if mtch_data[-1].find("F") > 0:
                        ret_val['forfeits'].append(rval)
                    else:
                        ret_val['other_matches'].append(rval)
                else:
                    ret_val['perfect_defense'].append(rval)
    return ret_val

def gen_json(league, fname, day):
    rval = get_all_matches(league, mday=day)
    with open(fname, 'w') as f:
        json_string = json.dumps(rval)
        print(json_string, file=f)

from MakeHtmlTable import JSON_FILENAME_FMT       
if __name__ == "__main__":
    day = 7
    league = 75
    fname = JSON_FILENAME_FMT % day
    gen_json(league, fname, day)
