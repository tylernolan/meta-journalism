import datetime
import time
from twitterScraper import *
from APscraper import *
from trendsProcessor import *
import traceback
import sys
#processing data stories[story,story,story] story{string title, date date}
def timedif(current, then):
		deltat=current-then
		return deltat
		
def updatescore(deltat):
	score=(1/deltat)*100
	return score

def processAP(stories):
	now=time.time()		#time since 01/01/1970
	search=stories[0] 	#list of search terms
	score=0
	for index, story in enumerate(stories[2:]):
		a=time.mktime(story.date.timetuple())
		b=time.mktime(stories[index+1].date.timetuple())
		if story.date<datetime.datetime.today()-datetime.timedelta(days=7):
			deltat=timedif(b,a) #time since last post
			if deltat>0:
				score+=updatescore(deltat)
				title=story.title
				for word in search:
					if word in title:
						score+=updatescore(deltat)
	print score
	return score

def processTwitter(tweets):
	elapsedtimes=0 
	for index, tweet in enumerate(tweets[2:]):
		a=time.mktime(tweets[index+1].time.timetuple())
		b=time.mktime(tweet.time.timetuple())
		elapsedtimes+=timedif(a,b)
	score=elapsedtimes/(len(tweets)-2)
	print 1/score
	return 1/score
class MainProcessor():
	def __init__(self, searchQuery):
		self.apScore = 0
		self.twitterScore = 0
		self.trendsScore = 0
		self.powerScore = 0
		search = searchQuery.split(" ")
		search = [x.strip() for x in search]
		try:
			self.apScore = processAP(APScraper(search).stories)
		except BaseException, e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
			print "Unable to get AP Score for {}".format(search)
		try:
			self.twitterScore = processTwitter(TwitterScraper(search).tweets)
		except BaseException, e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
			print "Unable to get Twitter Score for {}".format(search)
		try:
			self.trendsScore = float(TrendsProcessor(search).score) / 1000
			print "trends score: {}".format(self.trendsScore)
		except BaseException, e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
			print "Unable to get Trends Score for {}".format(search)
		try:
			sdDiff = self.trendsScore - self.apScore
			self.powerScore = abs(sdDiff) + (self.twitterScore * sdDiff)
		except:
			print "unable to get power score for {}".format(search)
			
if __name__ == "__main__":
	f = open("searches.txt").readlines()
	out = open("output.csv", 'w')
	for line in f:
		mp = MainProcessor(line)
		out.write("{},{},{},{}\n".format(mp.apScore, mp.twitterScore, mp.trendsScore, mp.powerScore))
	#stories = APScraper(["Trump"]).stories
	#print "AP Score..."
	#processAP(stories)
	
	#tweets=TwitterScraper(["Trump"]).tweets
	#print "Twitter Score..."
	#processTwitter(tweets)
	
	#p = TrendsProcessor(["Trump"])
	#print "Google Trends Score..."
	#print p.score