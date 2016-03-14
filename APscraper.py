from urllib import urlopen
import datetime
"http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT&query=donald+trump"
monthDict = {}
monthDict["Jan"] = "01"
monthDict["Feb"] = "02"
monthDict["Mar"] = "03"
monthDict["Apr"] = "04"
monthDict["May"] = "05"
monthDict["Jun"] = "06"
monthDict["Jul"] = "07"
monthDict["Aug"] = "08"
monthDict["Sep"] = "09"
monthDict["Oct"] = "10"
monthDict["Nov"] = "11"
monthDict["Dec"] = "12"
class APScraper():
	def __init__(self, searchterms):
		self.stories = []
		urlBase = "http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT&start_at={}&type=Story&language=English&selector=-----&output_format=headline&query={}"
		i = 0
		self.stories.append(searchterms)
		terms = self.formatSearchTerms(searchterms)
		url = urlBase.format(i, terms)
		page = urlopen(url).read()
		storyThing = self.getStories(page)
		storyHeader = storyThing[0].split("END GLOBAL CONTENT")[1]
		numStories = int(storyHeader.split("<")[14].split(";")[2].split("&")[0])
		while i < numStories:
			storyThing = self.getStories(page)
			storyText = storyThing[1:]
			self.stories += self.processIntoStories(storyText)
			i += 25
			url = urlBase.format(i, terms)
			page = urlopen(url).read()
			
		#self.dateFromString(storyText[1].split('>')[10])
	def formatSearchTerms(self, searchterms):
		ret = ""
		for term in searchterms:
			ret += term + "+"
			
		return ret[:-1]
		
	def getStories(self, page):
		data = page.split("<!-- END GLOBAL CONTENT -->")[1]
		stories = page.split("<!--right column-->")[0]
		splitStories = stories.split("storylink")
		return splitStories
	def dateFromString(self, dateString):
		monthChars = dateString[0:3]
		dayChars = dateString.split(";")[1].split(",")[0]
		timeChars = dateString.split(";")[2].split("&")[0].split(":")
		hour = timeChars[0]
		minutes = timeChars[1]
		morningOrNight = dateString.split(";")[3].split("&")[0]
		year = datetime.date.today().year
		if morningOrNight.startswith("P") and hour != "12":
			hour = int(hour) + 12
		month = monthDict[monthChars]
		dateObj = datetime.datetime(int(year), int(month), int(dayChars), int(hour), int(minutes))
		return dateObj

	def processIntoStories(self, storyList):
		stories = []
		for story in storyList:
			splitStory = story.split('>')
			title = splitStory[3][:-3]
			date = self.dateFromString(splitStory[10])
			stories.append(Story(title, date))
		return stories
			
class Story():
	def __init__(self, title, date):
		self.title = title
		self.date = date
		
if __name__ == "__main__":
	s = APScraper(["Donald", "Trump"])