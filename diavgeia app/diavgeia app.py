# mathesis.cup.gr course with title "Introduction to Python"
# Final Project: Data retrieval from diavgeia.gov.gr

import re
import urllib.request
import urllib.error

authorities = {}

def rss_feed(url): 
    '''
    Opening of rss feed,
    :param url: the address of rss feed.
    This function creates a file with the
    contents of the rss_feed having as name
    the rss_feed's address. It calls the
    function process_feed which chooses and
    prints content.
    '''
    url += r"/rss"
    req = urllib.request.Request(url)

    filename = url.replace('/', '_').replace('.', '_') + '.rss'
    filename = filename[8:]

    try:
        with urllib.request.urlopen(req) as response:
            char_set = response.headers.get_content_charset()
            html = response.read().decode(char_set)
        with open(filename, "w", encoding = char_set) as p:
            p.write(html)
    except urllib.error.HTTPError as e:
        #print('Σφάλμα HTTP:', e.code)
        print('HTTP Error:', e.code)
    except urllib.error.URLError as e:
        #print('Αποτυχία σύνδεσης στον server')
        #print('Αιτία: ', e.reason)
        print('Fail to connect to server')
        print('Reason: ', e.reason)
    else:
        process_feed(filename)

def process_date(date):
    '''
    The function formats the greek date of rss_feed:
    In rss file the date has the form: Wed, 14 Jun 2017 17:21:16 GMT
    and it should be formatted in a greek date, i.e. Τετ, 14 Ιουν 2017
    :param date:
    :return: the greek date
    '''
    daysEngToGr = {'Mon': 'Δευ', 'Tue': 'Τρι', 'Wed': 'Τετ', 'Thu': 'Πεμ', 'Fri': 'Παρ', 'Sat': 'Σαβ', 'Sun': 'Κυρ'}
    monthsEngToGr = {'Jan': 'Ιαν', 'Feb': 'Φεβ', 'Mar': 'Μαρ', 'Apr': 'Απρ', 'May': 'Μαι', 'Jun': 'Ιουν', 'Jul': 'Ιουλ', 'Aug': 'Αυγ', 'Sep': 'Σεπ', 'Oct': 'Οκτ', 'Nov': 'Νοε', 'Dec': 'Δεκ'}
    dayMonth = re.findall(r'(\b[\w]{3}\b)', date)
    date = re.sub(dayMonth[0], daysEngToGr[dayMonth[0]], date)
    date = re.sub(dayMonth[1], monthsEngToGr[dayMonth[1]], date)
    return date[:17]

def process_feed(filename):
    '''
    A function that opens a file with the rss feed and
    it prints the date and the titles of postings that contain.
    '''
    date_tag = 'lastBuildDate'
    title_tag = 'title'
    text = ''
    with open(filename, "r", encoding = 'utf-8') as f:
        text = f.read()
    date = re.findall(r'<' + date_tag + r'\b[^>]*>(.*?)</' + date_tag + r'>', text, re.I)
    print(process_date(date[0]))
    titles = re.findall(r'<' + title_tag + r'\b[^>]*>(.*?)</' + title_tag + r'>', text, re.I)
    i = 1
    print('*** {} ***'.format(titles[0].strip()))
    for j in range(1, len(titles)):
        print (i, titles[j])
        i = i + 1
    print('\n')

def search_authorities(authority):
    '''
    searching of authority name which fits to the user's criteria
    '''
    tonoi = ('αά', 'εέ', 'ηή', 'ιί', 'οό', 'ύυ', 'ωώ')
    n_phrase = ''
    for c in authority:
        char = c
        for t in tonoi:
            if c in t:
                char = '[' + t + ']'
        n_phrase += char
    pattern = '.*' + n_phrase + '.*'
    result = []
    for k, v in authorities.items():
        w = re.findall(pattern, k, re.I)
        for r in w:
            result.append(r)
    return result

def load_authorities():
    '''
    It loads the authorities to the dictionaty authorities{}
    '''
    try:
        with open("500_authorities.csv", "r", encoding = "utf-8") as f:
            for line in f:
                line = line.strip()
                authority = line.split(';')
                authorities[authority[0]] = authority[1]
    except IOError as e:
        print(e)
            
    
######### main ###############
'''
the main program manages the interraction with the user
'''
load_authorities()
while True :
    #authority = input(50 * "^" + "\nΟΝΟΜΑ ΑΡΧΗΣ:(τουλάχιστον 3 χαρακτήρες), ? για λίστα: ")
    authority = input(50 * "^" + "\nAUTHORITY NAME:(at least 3 characters), ? for list: ")
    if authority == '':
        break
    elif authority == "?": # it presents the authorities names
        for k,v in authorities.items():
            print (k,v)
    elif len(authority) >= 3 :
        # it searches an authority name that fits to user's criteria
        result = search_authorities(authority) 
        for r in result:
            print (result.index(r)+1, r, authorities[r])
        while result:
            #choice = input("ΕΠΙΛΟΓΗ....")
            choice = input("CHOICE....")
            if choice == "": break
            elif choice.isdigit() and 0 < int(choice) < len(result) + 1:
                choice = int(choice)
                url = authorities[result[choice - 1]]
                print(url)
                # it calls the function that loads the file rss:
                rss_feed(url)
            else: continue
    else :
        continue
