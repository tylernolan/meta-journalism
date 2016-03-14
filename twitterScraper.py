from urllib import urlopen
import datetime
class Tweet():
	def __init__(self, timeTweeted):
		self.time = datetime.datetime.fromtimestamp(timeTweeted)
		
class TwitterScraper():
	def __init__(self, searchTerms):
		baseUrl = "https://twitter.com/search?f=tweets&vertical=default&q={}"
		page = urlopen(baseUrl.format(self.formatSearchTerms(searchTerms))).read()
		self.tweets = []
		self.tweets.append(searchTerms)
		self.tweets += self.splitIntoTweets(page)
	def formatSearchTerms(self, searchterms):
		ret = ""
		for term in searchterms:
			ret += term + "+"
			
		return ret[:-1]
	def extractDate(self, tweet):
		tweet = tweet.split("<")
		for index, part in enumerate(tweet):
			if "data-time" in part:
				return float(part.split("\"")[3])
				
		f = open("error", 'w')
		f.write(str(tweet))
		f.close()
	def extractTweetText(self, tweet):
		tweet = tweet.split("class")
		print tweet[1]
		#TODO
	def splitIntoTweets(self, page):
		tweets = []
		page = page.split('<div class="js-tweet-text-container">')[1:-1]
		for tweet in page:
			date = self.extractDate(tweet)#datetime.date.fromtimestamp(self.extractDate(tweet))
			tweets.append(Tweet(date))
		return tweets
			
					
		
		
		
if __name__ == "__main__":
		ts = TwitterScraper(["Oculus","Rift"])
		for thing in ts.tweets[1:]:
			print thing.time
		