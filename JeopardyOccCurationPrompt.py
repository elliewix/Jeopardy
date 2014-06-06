# Program to read in the players, read in soccodes, and prompt a user to curate unmatched occs

import csv
from pprint import pprint
# read in the csv, assemble dictionary of players

# Helper functions

playerfile= 'playerout.csv'
socfile = 'scripts-soccodes.csv'

# return a fail report string
def failreport(dict):
    total = str(len(dict))
    fails = 0
    for key, value in dict.iteritems():
        if value[2] == 'False':
            fails += 1
    fails = str(fails)
    return fails + " fails out of " + total + " players, yielding " + str(int(100*(float(fails)/float(total)))) + "% failure."

# pretty print a list, prettier than pprint
def nicelistprint(list):
    result = ""
    for each in list[:-1]:
        result = result + each + " :: "
    result = result + list[-1]
    return result

def selectmatch(matches,matchindex,key,dict,curatorname):
    # presumes a dictionary with values of a list
    matchindex -= 1 # lowering by one to support sane user input (e.g. not zero for first element)
    # find player
    dict[key][2:] = matches[matchindex]
    dict[key] += [True,curatorname,False] #curated true, name, skipped false

# mark a player entity as skipped
def markskipped(key,dict,curatorname):
    dict[key]+= [True,curatorname,True] #curated true, name, skipped true

# prepare the dictionary for csv export
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

playerdict = {}
# Initial structure:
    # playerdict[key] = [scraped occ, name, sockey(false, or key, corename (empty or name), subname (empty or name)]
# after processing:
    # playerdict[key] = [scraped occ, name, sockey, corename, subname, curatedBool, curatedby, skippedBool]
with open(playerfile) as players:
    players = csv.reader(players)
    headers = next(players)
    for row in players:
        playerdict[row[0]] = row[1:-1]

# read in soccodes, assemble dictionary of soccodes
    # because this is going to be added to a ton of stuff, I'm going to include the keys in the values

socdict = {}
# socdict[key] = [key,corename,subname]

with open(socfile, 'rU') as soccodes:
    soccodes = csv.reader(soccodes)
    headers = next(soccodes)
    for row in soccodes:
        socdict[row[0]] = row[:-1] # again, killing the last element because unused

# read through the dictionary of players and look for players with unmatched occupations

print "\n\n"
print "Welcome to the curation program!"
print "The current progress is " + failreport(playerdict)
curatorname = "Elizabeth" #raw_input("What is your user name? ")
print "Welcome, " + curatorname + ", I am currently looking at: \nPlayer file: " + playerfile + "\nSOCCode file: " + socfile
# TODO: allow user to specify file names
print "Let's get started!\nThis program will search to see if the original occupation is contained inside\na soc code sub name.\n"


for playerkey, value in playerdict.iteritems():
    if value[2] == 'False':
        origocc = value[0].lower()
        name = value[1]
        # 1) Look for the original occ string in the soccode dictionary
        print "Looking at " + playerkey + ": " + name + "\nScraped occupation: " + origocc
        matches = []
        # loop through the soccodes and assemble matches
        for sockey, value in socdict.iteritems():
            if origocc in value[2].lower():
                matches.append(value)
        if len(matches) > 0:
            print "I found the following matches:"
            for index, value in enumerate(matches):
                print "Match " + str(index +1) + ": " + nicelistprint(value)
            matchchoice = raw_input("\nPlease select a match: ")
            # TODO: make this more robust against crap input
            if matchchoice.lower() == "skip":
                print "OK, skipped"
                markskipped(playerkey,playerdict,curatorname)
                print playerdict[playerkey]
                raw_input("Press enter to continue.")
                #TODO, do undo
            else:
                matchchoice = int(matchchoice)
                selectmatch(matches,matchchoice,playerkey,playerdict,curatorname)
                print "OK, I made that selection:"
                print playerdict[playerkey]
                raw_input("Press enter to continue.") #TODO: add an undo option
        else:
            print "I found no matches, moving on for now"
            # 2) report the results on the screen
            # 3) prompt the user to select one of the options or reject them
                # if selected, add to the player, return to main loop
                # if rejected, prompt for manual curation
                    # if yes:
                        # take input for a soccode entity ID, look it up, add to player
                        # return to main loop.  Make this a function?  Yes?
                    # else:
                        # return control to main loop
            # 4) Confirm what will be done and that it has been done
                # add in something to undo?
            # 5) prompt user to continue to next player or quit and export
                # Continue: next player
                # export: call export method
    else: 
        continue # continue back to playerdict loop

