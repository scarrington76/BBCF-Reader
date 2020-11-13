from os import listdir
from os.path import  isfile, join
import pandas as p
import xlrd
from xlrd.timemachine import xrange
import re

path = "/Users/scottcarrington/Desktop/BBCF/WWCF/GameLogs"
filelist = [f for f in listdir(path) if isfile(join(path, f)) and "txt" in f]
teams_xls = p.read_excel('/Users/scottcarrington/Desktop/BBCF/BBCF Gamereader Python/gamereader/wwcf_dict.xlsx')
team_dict = teams_xls.to_dict()
teams_list = p.read_excel('/Users/scottcarrington/Desktop/BBCF/BBCF Gamereader Python/gamereader/wwcf_teams.xlsx')
teams_list = teams_list['Teams'].astype(str).values.tolist()
# print (teams_list)
# print(readfiles)
# print(team_dict)
has_key = lambda a, d: any(k in a for k in d)
teamone = "1"
teamtwo = "2"
validplay = 0
cols = ["Offense", "Defense", "Quarter", "Down&Dist", "To Go", "FieldPos", "Formation", "Time", "Score"]
statdf = p.DataFrame(columns=cols)
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
entry = []

def get_team(s, l, one, two):
    finalteam_l = 0
    finalteam = " "
    for team in l:
        if team in s and team != one:
            tempteam = team
            tempteam_l = len(team)
            if tempteam_l > finalteam_l:
                finalteam = tempteam
    return finalteam

def set_posession(line, one, two):
    oneball = one+" ball"
    twoball = two+" ball"
    if oneball in line:
        return one, two
    elif twoball in line:
        return two, one
    else:
        return "None", "None"

def lineone(line, one, two):
    if line.startswith(one):
        line = line[len(one) + 7:]
    extract = re.split(r'\W+', line)
    qtr = extract[0]
    down = extract[1]
    distance = extract[2]
    fieldpos = extract[3]
    timehr = extract[4]
    timemin = extract[5]
    scorediff = int(extract[6]) - int(extract[7])
    return qtr,down,distance,fieldpos,timehr,timemin,scorediff

for file in filelist:  ##File is the current file in the list of files to process
    with open(join(path, file)) as f:
        lines = f.readlines()  ##Data_line is current line of file
        for i in xrange(len(lines)):
            # print(lines[i] + "   **processing")
            if teamtwo is "2" and teamone is not "1":
                teamtwo = get_team(lines[i], teams_list, teamone, teamtwo)
                # print("***********" + teamtwo + " is assigned to Team Two")
            if teamone is "1":
                teamone = get_team(lines[i], teams_list, teamone, teamtwo)
                # print("***********" + teamone + " is assigned to Team One")
            if (lines[i].startswith(teamone) or lines[i].startswith(teamtwo)) and lines[i+1].startswith('Offense: '):  ## Determines if a line is valid
                offense, defense = set_posession(lines[i], teamone, teamtwo)
                validplay += 1
                # print(lines[i])
                # print("offense >>> " + offense + " defense >>>> " + defense)
                qtr,down,distance,fieldpos,timehr,timemin,scorediff = lineone(lines[i], offense, defense)
                statdf = statdf.append({'Offense': offense, 'Defense': defense, 'Quarter': qtr, 'FieldPos': fieldpos, 'Score': scorediff},ignore_index=True)

print(statdf)