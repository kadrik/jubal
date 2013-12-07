import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()
yt_service.ssl = True
yt_service.developer_key = 'AIzaSyA8bWsPMKLSihq9_mN9gekJS4KQv6IKT0c'
yt_service.client_id = '366061435643.apps.googleusercontent.com'
yt_client_secret = '9rwbAk3w2S8BAl0Zbqq0XTGT'

entry = yt_service.GetYouTubeVideoEntry(video_id='PXY2EmuMLDg')

def is_music(entry):
	for cat in entry.category:
		if (cat.term == "Music"):
			return True
	return False
		
def title(entry):
	return entry.title.text


print "Is Music? : ", is_music(entry)
print "Title     : ", title(entry)
print "Duration  : ", entry.media.duration.seconds