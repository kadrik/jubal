import cgi
import urllib


from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from random import choice

import facebook
api_key = '462952027154922'
secret_key = '1a0b17d7e34b330d96ff38f65c28d2b4'
facebookapi = facebook.Facebook(api_key, secret_key)


# YOUTUBE STUFF

import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()
yt_service.ssl = True
yt_service.developer_key = 'AIzaSyA8bWsPMKLSihq9_mN9gekJS4KQv6IKT0c'
yt_service.client_id = '366061435643.apps.googleusercontent.com'
yt_client_secret = '9rwbAk3w2S8BAl0Zbqq0XTGT'

def get_entry(key):
	return yt_service.GetYouTubeVideoEntry(video_id=key)
	
def is_music(entry):
	for cat in entry.category:
		if (cat.term == "Music"):
			return True
	return False
		
def get_title(entry):
	return entry.title.text

# END YOUTUBE STUFF

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>

    <hr>

    <form>Guestbook name:
      <input value="%s" name="guestbook_name">
      <input type="submit" value="switch">
    </form>

    <a href="%s">%s</a>
"""

BANNER = """\
<div style='font-family: courrier, sans-serif;top: 0px;
	left:0px;width: 100%;height: 27px;position: absolute;
	background-color: rgb(45, 45, 45);line-height: 27px;'>
	<span style='padding-left:10px;color: #fff;
		background-color: transparent;font-weight: bold;
		text-decoration: none;'>
			Jubal.io
</span></div>
"""

FOOTER = """\
<div style='font-family: courrier, sans-serif;
		font-size:8pt;text-align:center;margin:auto;margin-top:10pt;'>
	<span style='color: lightgray;
		background-color: transparent;
		text-decoration: none;'>
			&copy;2013 CS Corporation - contact@csc.io - +447810845591 - 566 Cable Street, Unit 137, LONDON, EW1 3HB.
</span></div>
"""

YOUTUBE_PLAYER = """\
<div style='margin-top:50px;text-align:center'>
<div id="player" style='margin-bottom:10px;'></div>
    <script>
	youtube_id = "%s";
    function next(){
          document.src = "/";
          location.reload(true);
    }

      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '320',
          width: '480',
          videoId: youtube_id,
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError': onPlayerError
          }
        });
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
        event.target.playVideo();
      }

      // 5. The API calls this function when the player's state changes.
      //    The function indicates that when playing a video (state=1),
      //    the player should play for six seconds and then stop.
      function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.ENDED){
            next();
        }
       }

      function stopVideo() {
        player.stopVideo();
      }

      function onPlayerError(event){
       next();
      }
</script>
"""

GOOGLE_AD_CM = """\
<br/>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- csc -->
<ins class="adsbygoogle"
     style="display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-0213861397630160"
     data-ad-slot="9920854469"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>
"""

GOOGLE_AD_CSC = """\
<br/>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- csc 468 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:468px;height:60px"
     data-ad-client="ca-pub-0213861397630160"
     data-ad-slot="5987153667"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""


FACEBOOK_SDK = """\
<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=462952027154922";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
"""
DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Facebook_user(ndb.Model):
	"""Models an individual Facebook user."""
	name = ndb.StringProperty(indexed=False)
	facebook_id = ndb.StringProperty(indexed=False)
	registration_date = ndb.DateTimeProperty(auto_now_add=True)
	
class Youtube_video(ndb.Model):
	"""Models a Youtube video."""
	youtube_id = ndb.StringProperty(indexed=False)
	registration_date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        ids = ["PXY2EmuMLDg","3G-VUsBEcJ0","Vhj-XDdFunA","zAhFzB2JDDA","8qw_9Z_fzww","Uf62SR1jP5I","-j9uiC06ZuM","QIP7nG6s3WM","oNxMzTdrjvE","Y_df95Wcp3Y","va4OyeQHbr8","OAUx74-Ni50","IGyj9sMwd38","pFgRkPXemG8","dvY-y-H6TDg","_3EXHdT8DKM","vjncyiuwwXQ","lqV_ExWj-bw","OdxJhzyNPbo","A4N_zbegHro","7-G6Lrqr_iM","6GPm5_X3Ykg","ZBbXmEOy7-o","8qdQfs3Ib6s","7ppmdvXsMBE","WMKmQmkJ9gg","FGBhQbmPwH8","V1bFr2SWP1I","DhXkeBykF1o","TM7ICFXvpYw","E4kc0Aby2vA","OlVbEclPj4c","w9TGj2jrJk8","sdctCI-3nLY","e9EQsLf9wf4","Be-loLSUWT0","Jj6yXxVc21Y","AAkFBQ6sIcc","VNAt33KxfNc","cfOa1a8hYP8","QrzGpVOPcTI","oqaiH8iBZ5g","p-zeiYvAOLE","ENBX_v1Po1Y","2a4gyJsY0mc","P8a4iiOnzsc","sVh3WQtx_pw","4ee9Mqr0bdE","rYEDA3JcQqw","AhcttcXcRYY","cPRt2r3Qemw","i4rsAWJtWQI","7KhsLve4d0E","SmVAWKfJ4Go","0eDMHyfezxM","5ZT_nrrpe8c","zCkNu9OxThc","tId5I7WYZpQ","zanYf6c-DpA","bjjc59FgUpg","a07LlJrDQJA","cgqOSCgc8xc","DhCR9pOXdqc","N090STPx-2M","d-diB65scQU","9B-h1EEsKDA","_MM-I9LAQZE","8BhHTA6Gzn0","lE2B8PfsvGk","LLLY0j-lU8s","JT5zmEgIQn4","RYypmgIYOVQ","yb-beamG91Y","df2K91QSqJE","LanCLS_hIo4","zQE36wRM7HY","jEgX64n3T7g","K1lD5cE6Bwc","0sODneKnkU8","n-OByxoRlp4","3Io4wWwsmXg","1lyu1KKwC74","dr_wSwKFQQk","Zi8vJ_lMxQI","rWWt9C0_rSo","iuFHsIBMcsg","yM6hPuui-l8","etmWPV9ULo0","4mUmdR69nbM","dNg9SQxip5A","A_uMGuktiqo","Mj7o45lmZWI","zRcBvRC8j6g","TMETa77dUrg","z5rCaR4pJwc","EtlzW5F7V0s","6jmZTtFxcUg","A5_GqVMDLnQ","QIP7nG6s3WM","NwNgKytPOg4","e3WMPJQIDNo","EdBym7kv2IM","6FJSfLjQM4I","ZGDYa0abSXk","jrExrzacqAU","AueGN0b_dGo","po8e8nftgqI","nKvLB9P1ZoA","lcfCNVkcsjk","sFrNsSnk8GM","G5_rEGhQpIo","us4hWUEKkyM","Yu0bluEpy30","WrwhfhncPfM","JhjA2nvVD7U","XLpxxtWfuHU","kEH7cphEODk","bXfeGaiwNNc","Rfxf8PQi5B4","K4vOkuT4Ero","Dv7WllrZOcI","e4cjXXQCnLI","IGx46gMHaxE","16LFKCCDooc","7uE2-cc4f_k","VYloQVIaCps","v4tsoU3KlBg","jY0LDHgbh3o","3QAqJAfBjN8","uWhkbDMISl8","tEFp1Nv_xx4","7Z-DC66THOU","5MvsyNSk20Q","yiSjYv0QRPY","WfAqI3kwb_Y","UB_GbMQftkA","9Clwhfyqed8","wK7tq7L0N8E","Vqf44c1o8Bc","1pV8-Ybi2aY","hCdlTilrp5k","omGnzAd28YM","_XnTGkCUYoA","1s0-tbR-nzs","F0BDMTLRxgg","oS6wfWu0JvA","GFIvXVMbII0","GX89u0tzk9I","zC2ZbogNXvE","6UknDjQZr5E","Ps76ppc9_kM","dXhiu1ZbOyo","wS5qQ_qlRE0","vkPMyI8yb_g","dg3pPv_aIhw","JSUIQgEVDM4","UkHCncMbFEc","_L6Hfqxkgtc","OQ0IizC3j1g","-IWZXTo5Rgk","k9xb3BR6KuY","fSaUBzdNV04","iF8kJvgp0_Q","pau8Zf7srlU","2uRrdeUiqCA","snxpjEpQo9c","6dmrXhohwCw","MhKWwoAuuC8","tokCv2bjh3k","4uOxOgm5jQ4","b6I28pPgffA","NPQD7KxutcM","q5Ba-wAbIic","npAjisjvx8U","aQVT61U54kI","VHaeyBuD3mA","uE51B_G8Zk0","f0ulSeGpuZI","YHMNnPzZCGA","aqwEwpEgwB8","_ZXFe1ifETo","Hdc2zNgJIpY","wePM0aITzYc","KotlCEGNbh8","9AEoUa0Hlso","NrLkTZrPZA4","QY60VAViupk","Um3C9Gmpm4Y","THBeaPQqF54","MKk1u5RMTn4","tYQbZhWXRwM","OqeNROknctQ","4hOBgZa3hOA","UYIAfiVGluk","sF8eMK6dUXA","gs3nnPKMiZE","Rd37esAtkD4","GfISngTyaR0","pVadl4ocX0M","tZHG1HlP6WE","SVq2yMuAMVQ","eqqWfsIxbPo","vwv8yLjrR0w","a2j-QYaid0k","pqaUZkf52fs","9Aqj6u_7kFM","1iXUY9kwxo4","Qmny4LSjDgU","8rEgNKBZggg","1tEnAgKDF34","gjTomL2RAbM","AsyQzLauhqI","LXpbrGBIGxw","TUHFfR8hWcA","U3GIM7Dys1w","YeYJDu8TIck","USlE-5T1TY8","1IJzBvOCXpc","r4dOACe2QiE","UR1Jamb65YM","oFmjCyaGXwE","hoiZMxZ07wQ","ERF45KiPOwI","81ZlLsa1zaA","f08VwWQY0T8","iZ5s_V7PO84","6y7whyfiEJE","BwI6uJ2J-DM","qWkaMQ2O0NY","g0MTQpDgSFc","qe80msx6LnA","OmHockF_KTo","E33I5neA6pQ","zJsYgqQ0zEk","3Jtuf1TIl3E","z9lrVZdaluk","zAhFzB2JDDA","lQmKdS2y7bY","9U4XY-W6MmQ","0gtHR6gLAck","kBNKbG7rr4Y","0bb3DCGae-A","ATxSvH2yzH0","UmPM1KvLp24","enUx3VTFkSA","x4wuE12C4nc","EOEZz8G6P7s","HOu5iWhexE0","N9_tcQQ4o9w","Di-etRm4cN8","IXuuY4WEnHY","7Q8svnBoohU","7Qi4r7fIqQQ","nk-oa7YzHyk","WPncumXZExo","OnEQTFkakvU","nbgqdyN4-I4","vO5XB8BEORs","1EAOG97UZbg","SRYb0pc-BC4","4pNtuwPVzhM","ULXdGjFkKBc","cK8YSsjIaDs","JdeMvR--ICk","FoMvBFemNsc","tcRiSNviyok","E2NiP0azUvY","cWDxU813wd0","prGSIc7HcMU","rzy2wZSg5ZM","qLUIGVDgIOA","Y2jxjv0HkwM","MV_3Dpw-BRY","WDzpD_p1A8w","-DSVDcw6iW8","WA8EJQOqbdo","iMtz1d0ruAk","1G4isv_Fylg","kYZjsVO1YFk","dwt3kr0_l6I","Yu6Hr9kd-U0","InUm0v-fN8w","cCQpqSqeoMI","SOfG-DMR_gI","xKNh_Tva2X0","IeDMnyQzS88","0BSHAXpNey0","kQY5bcZdHBk","z3wXqyRQZnA","TPKbG1CCLx8","wmrHo1P6ph8","kN8LiaZAh-I","Vj_vjYPULT4","rIHrdLwa_y8","4axSpwbKuis","l4rXxEn6gnU","-WY9QwM_olw","6MAQxOBiD6A","xYuE21BncfI","M5LJrQVvYYg","Lp3kcHchD1Y","hHrvuQ4DwJ8","3GXtkAJOZ1s"]
        youtube_id = choice(ids)
		
        self.response.write('<html><body>')
        self.response.write(FACEBOOK_SDK)
        self.response.write(BANNER)

        self.response.write(YOUTUBE_PLAYER % youtube_id)        
        youtube_entry = get_entry(youtube_id)
        youtube_title = get_title(youtube_entry)
        self.response.out.write("<br/>%s<br/>" % youtube_title)

        self.response.out.write('<br/><form><span style="vertical-align:middle;" class="fb-login-button" data-width="200" scope="read_stream"></span>')
		#<br/>
        self.response.out.write('<button style="margin-left:5pt;width:4em;height:2em;vertical-align:middle;" type=submit value="Next">Next</button></form>')

        self.response.write(GOOGLE_AD_CSC)

        self.response.out.write('<br/><div style="margin-top:20pt;text-align:center;margin:auto;"><div style="width:466px;margin:auto;padding-top:5pt;padding-bottom:5pt;background:gray;border:1px solid black;"><span style="font-size:20pt;font-variant:small-caps;"><a style="color:white;text-decoration:none" href="">Would you like to know more?</a></span></div></div>')

        # Checks to make sure that the user is logged into Facebook.
        if facebookapi.check_session(self.request):
            pass
        else:
		    # If not redirect them to your application add page.
		    url = facebookapi.get_add_url()
			#'<fb:redirect url="' + url + '" />')
        #user = facebookapi.users.getInfo([facebookapi.uid], ['uid', 'name', 'birthday', 'relationship_status'])[0]		
        #self.response.write(user)
        self.response.write(FOOTER)
        self.response.write(GOOGLE_AD_CM)
        self.response.write("</body></html>")

class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)



