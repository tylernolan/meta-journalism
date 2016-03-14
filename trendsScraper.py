from pytrends.pyGTrends import pyGTrends
import datetime
class Trend():
	def __init__(self, date, score):
		self.date = date
		self.score = score
class TrendsScraper():
	def __init__(self, searchterms):
		self.trends = []
		self.trends.append(searchterms)
		con = pyGTrends("trendsscraper123", "googleTrends")
		con.request_report(self.formatSearchTerms(searchterms), date = "today 7-d")
		data = con.get_data()
		self.trends += self.processScore(data)
		
	def processScore(self, data):
		trends = []
		splitData = data.split("Interest over time")[1].split("\n\n")[0]
		for line in splitData.split("\n")[2:]:
			s = line.split(",")
			date = datetime.datetime.strptime(s[0], "%Y-%m-%d-%H:%M %Z")
			score = int(s[1])
			trends.append(Trend(date, score))
		return trends
	def formatSearchTerms(self, searchterms):
		ret = ""
		for term in searchterms:
			ret += term + " "
		return ret[:-1]
if __name__ == "__main__":
	ts = TrendsScraper(["Donald","Trump"])
	print ts.trends