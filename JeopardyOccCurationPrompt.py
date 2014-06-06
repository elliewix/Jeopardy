# Program to read in the players, read in soccodes, and prompt a user to curate unmatched occs

import csv
from pprint import pprint
# read in the csv, assemble dictionary of players

# Helper functions

playerfile= 'playeroutfromprompt.csv'
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
        result = str(result) + str(each) + "\t"
    result = result + str(list[-1])
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
# function to process playerdict and prepare it for csv output
# format needs to be a list of dictionaries, key=header and value=value
# [{head:value, head:value}]

#headers = ["PlayerID","Occupation","Name","MatchedSocCode","MatchedSocCore","MatchedSocTitle","CuratedBool","Curator","SkippedBool"]
#outputfilename = 'playerout.csv'
def output(dict,headers,outputfilename):
    list = []
    for key, playervalue in dict.iteritems():
        tempdict = {}
        tempdict[headers[0]] = key
        playervalue.insert(0,key)
        for i, each in enumerate(headers):
            try:
                tempdict[headers[i]] = playervalue[i]
            except:
                tempdict[headers[i]] = ''
        list.append(tempdict)
    with open(outputfilename,'w') as f:
        f_csv = csv.DictWriter(f,headers)
        f_csv.writeheader()
        f_csv.writerows(list)

def lookingat(playerkey,name,origocc):
    print "Looking at " + playerkey + ": " + name + "\nScraped occupation: " + origocc + "\n"

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

headers = ["PlayerID","Occupation","Name","MatchedSocCode","MatchedSocCore","MatchedSocTitle","CuratedBool","Curator","SkippedBool"]
                        

# read through the dictionary of players and look for players with unmatched occupations

print "\n\n"
print "Welcome to the curation program!"
print "The current progress is " + failreport(playerdict)
curatorname = "Elizabeth" #raw_input("What is your user name? ")
print "Welcome, " + curatorname + ", I am currently looking at: \nPlayer file: " + playerfile + "\nSOCCode file: " + socfile
# TODO: allow user to specify file names
print "Let's get started!\nThis program will search to see if the original occupation is contained inside\na soc code sub name.\n"

flags = []

for playerkey, value in playerdict.iteritems():
    if value[2] == 'False' and value[6] != 'TRUE':
        origocc, name = value[0].lower(), value[1]
        # 1) Look for the original occ string in the soccode dictionary
 
        matches = []

        # loop through the soccodes and assemble matches
        for sockey, value in socdict.iteritems():
            if origocc in value[2].lower():
                matches.append(value)

        if len(matches) > 0:
            lookingat(playerkey,name,origocc)
            print "I found the following matches:"
            for index, value in enumerate(matches):
                print "\tMatch " + str(index +1) + ": " + nicelistprint(value)

            print "Type the number of the match to select it."
            print "Type 'skip' to skip a player.\nType 'done' to quit and save."
            print "Type 'none' to reject all matches and manually set the occupation."
            matchchoice = raw_input("\nMake your choice: ")
            # TODO: make this more robust against crap input
            print "\n\n"
            while True:
                if matchchoice.lower() == "skip":
                    print "OK, skipped"
                    markskipped(playerkey,playerdict,curatorname)
                    print playerdict[playerkey]
                    raw_input("Press enter to continue.")
                    #TODO, do undo
                    print "\n\n\n\n"
                    break

                elif matchchoice.lower() == 'done':
                    prompt = raw_input("do you want to save? ")
                    if prompt.lower() == 'yes':
                        outputfilename = 'playeroutfromprompt.csv'
                        output(playerdict,headers,outputfilename)
                    break

                elif matchchoice.lower() == 'none':
                    print "You have chosen to reject these.\nPlease review the coding sheet and enter a standard name."
                    print "Enter the code or say 'go back'"
                    prompt = raw_input("Your choice: ")
                    if prompt.lower() == 'go back':
                        break
                    else:
                        try:
                            print socdict[prompt]
                        except:
                            continue
                else:
                    matchchoice = int(matchchoice)
                    selectmatch(matches,matchchoice,playerkey,playerdict,curatorname)
                    print "OK, I made that selection.  The player information is now:"
                    print "\t" + nicelistprint(headers)
                    print "\t" + nicelistprint(playerdict[playerkey])
                    cont = raw_input("Do you want to continue? Type no to quit. ") #TODO: add an undo option
                    if cont.lower() == 'no':
                        prompt = raw_input("do you want to save? Type yes to save. ")
                        if prompt.lower() == 'yes':
                            outputfilename = 'playeroutfromprompt.csv'
                            output(playerdict,headers,outputfilename)
                    print "\n\n\n\n"
        else:
            continue #print "I found no matches, moving on for now"
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

