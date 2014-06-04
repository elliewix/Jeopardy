# Jeopardy Processing

Processing information about Jeopardy players

This is a personal project to scrape information about Jeopardy players, prepare data for analysis, and eventually run those tests.

# Steps

1. Gather player info
2. Gather game info
3. Connect them
4. Answer all the questions

# Source

The player information is from http://www.j-archive.com/.  Player pages were saved as text files to avoid hitting their page too much.

SOC Codes were collected from http://www.bls.gov/soc/.

# Things of interest

1.  What are the occupations of Jeopardy players?
  * Normalize these to soccodes.
  * Some manual curation will need to be done
2.  Are certain occuptions more likely to produce long running champions?
3.  Where are players from?
  * Are certain locations hot spots for champions?
  * How have player locations changed over time?
4.  Are players who defeat long running champions more likely to become long running champions?

# Files

* scripts-Jeopardy Processing.ipynb
    * Processing script, will output the player info as csv
* scripts-Jeopardy_Scraping.ipynb
    * Code to gather the player text files
* scripts-soccodes.csv
    * csv file with SOC codes info
* scripts-playerout.csv
    * example output
* players/
    * player text files
* OldScripts/
    * this has been a long term and learning project, so I've archived older code here.