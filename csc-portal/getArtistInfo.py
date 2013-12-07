# YOUTUBE STUFF

import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()
yt_service.ssl = True
yt_service.developer_key = 'AIzaSyA8bWsPMKLSihq9_mN9gekJS4KQv6IKT0c'
yt_service.client_id = '366061435643.apps.googleusercontent.com'
yt_client_secret = '9rwbAk3w2S8BAl0Zbqq0XTGT'
	
def is_music(entry):
	for cat in entry.category:
		if (cat.term == "Music"):
			return True
	return False

# END YOUTUBE STUFF

# ECHO NEST STUFF

from pyechonest import artist
from pyechonest import song
from pyechonest import config
config.ECHO_NEST_API_KEY="T3XI5Z9ADDMUM7372"

# END ECHO NEST STUFF

class Track:

	def __init__(self,youtube_id):
		self.youtube_id=youtube_id
		self.youtube_entry = yt_service.GetYouTubeVideoEntry(video_id=self.youtube_id)
		self.youtube_title = self.youtube_entry.title.text
		self.song = getSongInfo(self.youtube_title)   #echo nest song class
		self.genres = getGenre(self.song.artist_id)   #genres associated to the artist of the song
		self.artistBio = getBiography(artist.Artist(self.song.artist_id)) #biography of the artist of the song
		self.artistName = self.song.artist_name.encode('utf-8')
		self.artistPic = getPicture(artist.Artist(self.song.artist_id)) #picture of the artist of the song
		self.lyrics = getLyrics(self.song) #lyrics of the song
	
	def get_html(self):
	    return '<div><h1>%s</h1></div><div><img src="%s"></div><div><p>%s</p></div><div>%s</div>' %(self.artistName,self.artistPic,self.artistBio,self.genres)


def getBiography(a):
    bio = a.get_biographies() #get biographies and select the first one
    if len(bio)>=1:
        bio = bio[0]
        text = bio['text'].encode('utf-8')
        return text
    else:
        return
    
def getPicture(a):
    pic = a.get_images()  #get images and select the first one
    if len(pic)>=1:
        pic = pic[0]
        pic = pic['url'].encode('utf-8')
        return pic
    else:
        return
    
def getSongInfo(s):
    #take string as input and get corresponding song
    echo = song.search(combined=s)[0]
    return echo
	
def getGenre(artist_id):
    # take song structure as input and return the genres associated with the artist	
    the_artist = artist.Artist(id=artist_id, bucket=['terms'])
    return map(lambda e: e['name'].encode('utf-8'), the_artist.terms)

def getLyrics(song):
    lfid = song.get_foreign_id('lyricfind-US')
    if not lfid:
        return
    else:
        lfid = lfid.replace('lyricfind-US:song:', '')
        url = 'http://test.lyricfind.com/api_service/lyric.do' +  \
            '?apikey=2233d1d669999ce64ee0eb073d6da191' + \
            '&reqtype=default&output=json&trackid=elid:' + lfid
    print url