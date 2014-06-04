from bs4 import BeautifulSoup

for i in range(1,8688):
    filename = 'player'+str(i)+'.txt'
    with open(filename) as player:
        soup = BeautifulSoup(player)
        #print soup
    occupation = soup.find_all('p')[0].contents
    fullname = soup.find_all('p')[1].contents
    print str(i) + "@" + fullname[0].encode('utf-8') + "@" + occupation[0].encode('utf-8')