from pyechonest import song
import py7D
import json
import os
from pyechonest import config

config.ECHO_NEST_API_KEY="T3XI5Z9ADDMUM7372"
    
def getSongInfo(s,case):
    res7D = []
    resEN = []
    
    if case==1:
        # string contains name of the song
        resEN = song.search(title=s)
        #res7D = py7D.request('track', 'search', q=s, pageSize=1)
        
        # figure out the artist

    elif case==2:
        # string contains name of the artist
        resEN = song.search(artist=s)
        
        # figure out the song

    elif case==3:
        # string contains song and artist
        resEN = song.search(combined=s)
    
    if len(resEN)>0:
        for i in range(0,len(resEN)):
            title = resEN[i].title
            artist_name = resEN[i].artist_name
            print artist_name + ' - ' + title
        return resEN
    else:
        raise NameError('song not found')
    
if __name__ == "__main__":
    getSongInfo("so what",1)