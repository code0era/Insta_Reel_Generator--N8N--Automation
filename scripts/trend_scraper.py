"""
trend_scraper.py
Fetch today's top trending topic using pytrends.
Returns the topic as a plain string.
"""
from pytrends.request import TrendReq
import json, sys

def get_trending_topic() -> str:
    pytrends = TrendReq(hl="en-US", tz=330)
    df = pytrends.trending_searches(pn="united_states")
    return str(df.iloc[0, 0])

if __name__ == "__main__":
    topic = get_trending_topic()
    print(json.dumps({"topic": topic}))
