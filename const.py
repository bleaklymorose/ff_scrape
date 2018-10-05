DATABASE = 'database/count.db'
COMMON_DATABASE = 'database/common_count.db'

POS = ['qb', 'rb', 'wr', 'te', 'k']
URL_ADP = 'https://www.fantasypros.com/nfl/adp/'
URL_PRO = 'https://www.fantasypros.com/nfl/projections/'
URL_LEAD = 'https://www.fantasypros.com/nfl/reports/leaders/'

COMMON_ABRV = {'a.j.': 'aj', 'c.j.': 'cj', 'd.j.': 'dj', 'j.d.': 'jd', 'j.j.': 'jj', 't.j.': 'tj', 't.y.': 'ty'}
COMMON_NN = {'qb':
                    {'ben roethlisberger': ['big ben'],
                     'c.j. beathard': ['cj beathard', 'beathard'],
                     'jimmy garoppolo': ['jimmy g'],
                     'matt ryan': ['matty ice'],
                     'mitch trubisky': ['mitchell trubisky', 'trubs'],
                     'nick foles': ['big dick nick', 'bdn'],
                     'ryan fitzpatrick': ['fitzmagic', 'fitztragic'],
                     'tom brady': ['tb12']},
             'rb':
                    {'adrian peterson': ['ap', 'ad', 'all day'],
                     'alfred morris': ['alfmo'],
                     'christian mccaffrey': ['cmc'],
                     'c.j. anderson': ['cj anderson', 'cja'],
                     'c.j. prosise': ['cj prosise'],
                     'david johnson': ['dj'],
                     'ezekiel elliott': ['zeke'],
                     'giovani bernard': ['gio bernard', 'gio'],
                     'isaiah crowell': ['crow', 'cawcaw'],
                     'jamaal williams': ['j willy'],
                     'j.d. mckissic': ['jd mckissic'],
                     'kareem hunt': ['khunt'],
                     'legarrette blount': ['lgbt'],
                     'leonard fournette': ['lenny'],
                     'lesean mccoy': ['shady'],
                     'le\'veon bell': ['leveon bell', 'leveon'],
                     'ronald jones': ['rojo'],
                     'todd gurley': ['godd'],
                     't.j. logan': ['tj logan'],
                     't.j. yeldon': ['tj yeldon'],
                     'ty montgomery': ['ty monty', 'ty mont', 'tymo']},
             'wr':
                    {'a.j. green': ['aj green', 'ajg'],
                     'allen robinson': ['ar15', 'arob'],
                     'antonio brown': ['ab'],
                     'deandre hopkins': ['dhop', 'nuk'],
                     'desean jackson': ['djax'],
                     'emmanuel sanders': ['manny'],
                     'jarvis landry': ['juice'],
                     'j.j. jones': ['jj jones'],
                     'j.j. nelson': ['jj nelson'],
                     'j\'mon moore': ['jmon moore', 'jmon'],
                     'john brown': ['smokey'],
                     'josh gordon': ['flash'],
                     'larry fitzgerald': ['fitz'],
                     'marvin jones': ['mjj'],
                     'michael crabtree': ['crabby'],
                     'odell beckham jr.': ['obj', 'odell beckham', 'odb', 'odell beckham jr'],
                     't.y. hilton': ['ty hilton'],
                     'tyreek hill': ['freak', 'reek']},
             'te':
                    {'austin seferian-jenkins': ['asj'],
                     'c.j. uzomah': ['cj uzomah'],
                     'o.j. howard': ['oj howard', 'oj'],
                     'rob gronkowski': ['gronk']},
             'k':
                   {'greg zuerlein': ['gregleg', 'greg the leg', 'legatron']}
               }

NN_LOG = 'log/nicknames.log'
FILTER_LOG = 'log/filtered.log'
