# Program to read in the players, read in soccodes, and prompt a user to curate unmatched occs

# read in the csv, assemble dictionary of players
# read in soccodes, assemble dictionary of soccodes

# read through the dictionary of players and look for players with unmatched occupations

    # If matched: continue, maybe not do an else here because continue will skip everything else
    
    # Look for the original occ string in the soccode dictionary
        # 1) assemble a temporary array of all the matched soccodes
            # if array empty: report empty
            # else: report the array to the user
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

            