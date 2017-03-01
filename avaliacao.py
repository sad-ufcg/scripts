"""
Script to process LIME tables.
"""
from pprint import pprint

import codecs
import locale
import sys

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

import MySQLdb


def describe_tables(cursor, tables):
    for row in cur.execute("SHOW TABLES;").fetchall():
        table = row[0]
        print '=========', table
        cursor.execute("DESCRIBE " + table + ";")
        for row in cursor.fetchall():
            print '\t'.join([str(x) for x in row])
        cursor.execute("SELECT * FROM " + table + ";")
        for row in cursor.fetchall():
            print '\t'.join([str(x) for x in row])


flatten = lambda l: [item for sublist in l for item in sublist]


def f(value):
    if not value:
        return
    return filter(lambda x: x, value)


def stats(value):
    copy = f(value)
    copy.sort()
    result = {}
    result['median'] = copy[len(copy) / 2]
    result['size'] = len(copy)
    result['q1'] = copy[len(copy) / 4]
    result['q3'] = copy[3 * len(copy) / 4]
    result['avg'] = sum(copy) / float(len(copy))
    return result


def agreg(scores):
    if not scores:
        return  {'size': 0, 'avg': 0, 'median': 0, 'q1': 0, 'q3': 0, 'avg': 0}
    final = [x['avg'] for x in scores]
    result = stats(final)
    result['size'] = min([x['size'] for x in scores])
    return result


def calculate(scores):
    if not scores:
        return
    final = map(list, zip(*scores))
    res = []
    for value in final:
        res.append(stats(value))
    return res


def suma(scores):
    final = [0, 0, 0, 0, 0]
    for score in scores:
        for score_i in range(len(score)):
            if score[score_i] == u'Y':
                final[score_i] += 1
    return final


def check(string):
    return string.lower().strip() not in ['nenhum', 'nada', 'n/a', '-']


TRANSLATE = {'A1':5, 'A2': 4, 'A3': 3, 'A4': 2, 'A5': 1}  # Translate scores to a value
result = {}
surveys = {}

db = MySQLdb.connect(host="localhost", user="root", passwd="enter", db="lime", charset='utf8', use_unicode=True)
cur = db.cursor()
# describe_tables(cursor, tables)
cur.execute("SELECT surveyls_survey_id, surveyls_title FROM lime_surveys_languagesettings;")

for row in cur.fetchall():
    surveys[row[0]] = row[1]

for survey, descr in surveys.items():
    try:
        cur.execute("SELECT * FROM lime_survey_" + str(survey) + ";")
    except:
        continue
    scores = []
    comments = []
    other_comments = []
    other = []
    for row in cur.fetchall():
        if len(row) == 40:  # tables with IP
            start = 6
        elif len(row) == 39:  # tables without IP
            start = 5
        else:
            continue
        scores_c = [TRANSLATE.get(x, None) for x in row[start:start+28:2]]
        if scores_c[0]:
            scores.append(scores_c)
            comments.append(f(row[start+1:start+29:2]))
            other_comments.append(row[start+28:start+33])
            other.append(f(row[start+33]))
    result[survey] = (descr, agreg(calculate(scores)), f(comments), f(other), suma(other_comments))

proc = result.values()
proc.sort(key=lambda x: (x[1]['median'], x[1]['size']))
proc.sort(key=lambda x: (x[0]))

total = [0, 0, 0, 0, 0]
for disciplina in proc:
    if '2016' not in disciplina[0]:
        continue
    print disciplina[0]
    #print disciplina[0] + '#' + str(disciplina[1]['size']) + '#' + str(disciplina[1]['median'])
    print " * Tamanho/Med/1Q/3Q: " + str(disciplina[1]['size']) + " " + str(disciplina[1]['median']) + " " + str(disciplina[1]['q1']) + " " + str(disciplina[1]['q3'])
    if disciplina[4]:
        total[0] += disciplina[4][0]
        total[1] += disciplina[4][1]
        total[2] += disciplina[4][2]
        total[3] += disciplina[4][3]
        total[4] += disciplina[4][4]
        print disciplina[4]
    continue
    if disciplina[2]:
        for l_comment in disciplina[2]:
            for comment in l_comment:
                if check(comment):
                    print "  - " + comment
    if disciplina[3]:
        for other in disciplina[3]:
            if check(other):
                print "  - " + other

# lime_surveys_languagesettings
# - surveyls_survey_id      int(11) NO      PRI     None
# - surveyls_title  varchar(200)    NO              None

# lime_survey_IDIDID
#0 id      int(11) NO      PRI     None    auto_increment
#1 token   varchar(36)     YES     MUL     None
#2 submitdate      datetime        YES             None
#3 lastpage        int(11) YES             None
#4 startlanguage   varchar(20)     NO              None
#5 ipaddr  text    YES             None
#6 111479X2207X14706       varchar(5)      YES             None
#7 111479X2207X14706comment        text    YES             None
#... 14 perguntas total
#... 5 abertas
#... 1 texto

print total
db.close()
