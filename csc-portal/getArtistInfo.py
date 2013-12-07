#artist id produces html with picture and biography
from pyechonest import artist
from pyechonest import song
from pyechonest import config
config.ECHO_NEST_API_KEY="T3XI5Z9ADDMUM7372"

def mainFunction(s):
    #take a string as an input, and find out song, artist and artist informations
    songInfo = getSongInfo(s)
    aID = songInfo.artist_id
    genres = getGenre(songInfo)
    genres = [g.encode('utf-8') for g in genres]
    
    a = artist.Artist(aID)
    aName = a.name
    bio = getBiography(a)[1:1000]
    imgUrl = getPicture(a)
    s = '<div><h1>%s</h1></div><div><img src="%s"></div><div><p>%s</p></div><div>%s</div>' %(aName,imgUrl,bio,genres)
    return s

def getBiography(a):
    bio = a.get_biographies()[0] #get biographies and select the first one
    text = bio['text']
    return text
    
def getPicture(a):
    pic = a.get_images()[0]  #get images and select the first one
    url = pic['url'].encode('utf-8')
    return url
    
def getSongInfo(s):
    #take string as input and get corresponding song
    echo = song.search(combined=s)[0]
    return echo
	
def getGenre(echo):
    # take song structure as input and return the genres associated with the artist	
    the_artist = artist.Artist(id=echo.artist_id, bucket=['terms'])
    return map(lambda e: e['name'], the_artist.terms)