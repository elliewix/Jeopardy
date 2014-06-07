
# In[1]:

import urllib2

for i in range(4367,9115):
    code = i
    url = "http://www.j-archive.com/showplayerstats.php?player_id=" + str(code)
    #filename = "DropBox/python/JArchiveScrape/Player" + str(code) + ".txt"
    filename = "player" + str(code) + ".txt"
    try:
        file( "players2/" +filename, "wb").write(urllib2.urlopen(url).read())
    except:
        print "player",i,"failed"


# In[5]:

print "foo"


# Out[5]:

#     foo
# 

# In[ ]:

|

