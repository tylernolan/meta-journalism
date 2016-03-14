from trendsScraper import *
class TrendsProcessor():
	def __init__(self, searchTerms):
		trends = TrendsScraper(searchTerms).trends[1:]
		self.score = 0
		day = 1
		for loop, trend in enumerate(trends):
			self.score += trend.score / day
			if loop % 24 == 0 and loop != 0:
				day += 1
		
		
if __name__ == "__main__":
	tp = TrendsProcessor(["Hillary","Clinton"])
	print tp.score