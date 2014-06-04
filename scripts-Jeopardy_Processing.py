
# In[1]:

#various imports, etc.
import re
import csv
from os import listdir
from os.path import isfile, join


# In[2]:

# dump all text into one bigass string for quick checking
with open('scripts-soccodes.csv','rU') as f:
    soctext = f.read()


# In[3]:

#Opens the soccodes csv file and processes the rows into a list
#Removes the last element of each row (not used for this project)
soccodes = []
with open('scripts-soccodes.csv','rU') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
    	soccodes.append(row[:-1]) # killing off the last element in rows


# In[4]:

# Defining helper functions

# pretty print a dictionary
def printdict(dict):
    for key, value in dict.iteritems():
        print key, value
        
# function to find unique occupations
# should update to require occ element position
def finduniqueoccs(dict):
    uniques= {}
    for key,value in dict.iteritems():
        if value[0] in uniques:
            uniques[value[0]] +=1
        else:
            uniques[value[0]] = 1
    return uniques

# Filters through player dict and returns a dictionary with only
# players with matching soccode results
def filterdict(dict):
    """returns only players with occupation matches"""
    clean = {}
    for key, value in dict.iteritems():
        if value[2] != False:
            clean[key] = value
    return clean

# function to process the tallied list of occupations and return
# a dictionary with occupations having num or more occurances
def findmorethan(dict,num):
    newdict = {}
    for key, value in dict.iteritems():
        if value >= num:
            newdict[key] = value
        else:
            continue
    return newdict

# function to process playerdict and prepare it for csv output
# format needs to be a list of dictionaries, key=header and value=value
# [{head:value, head:value}]
def prettyprintdict(dict,headers):
    list = []
    for key, value in dict.iteritems():
        tempdict = {}
        tempdict[headers[0]] = key
        tempdict[headers[1]] = value[0]
        tempdict[headers[2]] = value[1]
        if value[2] == False:
            tempdict[headers[3]] = False
        else:
            tempdict[headers[3]] = value[2][0]
            tempdict[headers[4]] = value[2][1]
            tempdict[headers[5]] = value[2][2]
        list.append(tempdict)
    return list

def countFalses(dict):
    falsesum = 0
    seen = 0
    for key,value in dict.iteritems():
        if value[2] == False:
            falsesum += 1
        seen += 1
    print "falses seen",falsesum,"out of",seen,"yielding",str(int((float(falsesum)/float(seen))*100))+"%", "failure"
    
def listfailures(dict):
    countdict= {}
    for key, value in dict.iteritems():
        if value[2] != False: 
            continue
        if value[0] in countdict:
            countdict[value[0]] +=1
        else:
            countdict[value[0]] = 1
    return countdict


# In[5]:

# Part 1: Construct player dictionary

# read through the files, find the phrases, add them to a dictionary

#find all the file names
mypath = 'players2/'
players = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and f[0] != '.' ]

#compile name and occ regex patterns
occupation = re.compile(r'<p class="player_occupation_and_origin">(?:an? *)?(.+?)(?:originally\s*)?from.+?</p>',re.IGNORECASE)
occupationfailed = re.compile(r'<p class="player_occupation_and_origin">(.+?)</p>',re.IGNORECASE)
name = re.compile(r'<p class="player_full_name">(.+?)</p>',re.IGNORECASE)

#create empty dictionary
playerdict = {}

#loop through the list of files
for each in players:
    #find the player number in the file name
    playernum = re.findall(r'[0-9]+',each)[0]
    #read through the file
    with open("players2/" + each,'rb') as player:
        player = player.readlines()
        # read through the lines
        for each in player:
            if 'player_occupation_and_origin' in each:
                # create empty player record in the dictionary
                playerdict[playernum] = []
                try:
                    try:
                        # if the elegant regex doesn't snag anything
                        playerdict[playernum].append(re.findall(occupation,each)[0].strip())
                    except:
                        # just snag all the things
                        playerdict[playernum].append(re.findall(occupationfailed,each)[0].strip())
                    # name just snags all the things
                    playerdict[playernum].append(re.findall(name,each)[0].strip())
                except:
                    # if either occupation occupationfailed fail, mark as failed
                    playerdict[playernum].append('FAILED')


# In[9]:

print len(soccodes)
print len(playerdict)
print len(playerdict['100'])

for row in soccodes:
    if row[0] == 'MiscTeacher':
        print soccodes.index(row)
        
soccodes[6593]


# Out[9]:

#     6597
#     9112
#     2
#     6596
# 

#     ['GradStu', 'Graduate student', 'Graduate student']

# In[10]:



# Part 2: Join Soccode information to the players

# processing the players and soccodes together
# will append the matching soc phrase to the player entry
# if not found, will append False

#looping through dictionary
count = 0
for key, value in playerdict.iteritems():
    if len(value) > 2:
        print "Remake the playerdict" #because this is using append, needs to not already have stuff
        break
    #boolean to see if a soccode has been found
    found = False
    #process through the soccode rows
    count = 0
    #if value[0] in soctext:
    for row in soccodes:
        # value[0] is the occ string for the human
        # row[2] is the specific occ string in the soccodes
        # lowercases both and checks for equality
        if value[0].lower() == row[2].lower():
            # if equal, add the soccode row to the player's record
            playerdict[key].append(row)
            # mark that is has been found
            found = True
            break
        elif 'graduate student' in value[0].lower():
            playerdict[key].append(soccodes[6593])
            found = True
            break
        elif 'teacher' in value[0].lower():
            playerdict[key].append(soccodes[6596])
            found = True
            break
    if found == False:
        # if finished looping through soccodes and not found, mark as false
        playerdict[key].append(False)
    print key, value
#from pprint import pprint       
#pprint(playerdict)

countFalses(playerdict)


# Out[10]:

#     5988 ['state fair coordinator', 'Peter Latouf', False]
#     5989 ['park ranger', 'Evelyn Chester', False]
#     5982 ['homemaker and volunteer', 'Sue Romberg', False]
#     5983 ['lawyer', 'Alex Hooper', ['23-1011', 'Lawyers', 'Lawyer']]
#     5980 ['law student', 'Anthony Resnick', False]
#     5981 ['software project manager', 'Stefanie Tomko', False]
#     5986 ['graduate student', 'Daniel Wilkinson', ['GradStu', 'Graduate student', 'Graduate student']]
#     5987 ['foreign service officer', 'Liz Murphy', False]
#     5984

# In[8]:






#fails =  listfailures(playerdict)

from pprint import pprint
#pprint(fails)

# print printdict(fails)
            


# Out[8]:

#     falses seen 7195 out of 9112 yielding 78% failure
# 

# In[9]:

# Code to produce a list of tallied occupations

#onlyoccs= filterdict(playerdict)
# print finduniqueoccs(onlyoccs)

# for key, value in findmorethan(finduniqueoccs(onlyoccs),3).iteritems():
#     print key, value


# In[11]:

# Part 3: prepare the dictionary for output
# Run playerdict through the output prep function

headers = ['PlayerID','Occupation','Name','MatchedSocCode','MatchedSocCore','MatchedSocTitle']
dictforprinting = prettyprintdict(playerdict,headers)
#print dictforprinting


# In[12]:

# Part 4: Write the processed playerdict to a csv
with open('playerout.csv','w') as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerows(dictforprinting)


# In[13]:

print "foo"


# Out[13]:

#     foo
# 

# In[ ]:



