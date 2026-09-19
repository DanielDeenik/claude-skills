# Signal Sources — Data, URLs & Scraping Notes

## Tier 1: Leading Indicators (Pre-mainstream)

### Reddit
- **What to look for**: Complaint threads, "does anyone else have this problem", DIY
  workarounds, wish-list posts ("I wish there was a product that...")
- **Best subreddits by category**: r/BuyItForLife, r/malelivingspace, r/femalelivingspace,
  r/homeimprovement, r/Pets, r/xxfitness, r/productivity, r/WorkFromHome
- **Tool**: Reddit search with time filter "Past Month". Sort by "Top".
- **Scraping**: PRAW (Python Reddit API Wrapper) — free tier sufficient for monitoring.

### TikTok
- **What to look for**: "unboxing regret" videos, "#tiktokmademebuyit" adjacent content,
  comment sections on problem-complaint videos
- **Signal**: View velocity on problem-framing videos (not solution videos yet)
- **Tool**: Manual search + TikTok Creative Center (free, shows trending hashtags)

### Twitter / X
- **What to look for**: Casual complaints about product categories, emerging lifestyle
  vocabulary (new words = new needs)
- **Tool**: Advanced search, date-range filter. Look for volume of original posts (not RTs).

---

## Tier 2: Confirmation Indicators

### Google Trends
- **URL**: trends.google.com
- **What to look for**: 4–12 week upward slope. "Breakout" label on related queries.
- **Key technique**: Compare against a stable baseline term to calibrate relative growth.
- **Python**: `pytrends` library — unofficial Google Trends API wrapper.

### Amazon Best Sellers + Reviews
- **What to look for**: Products ranked #50–500 in a subcategory (not #1 — too saturated)
  with 3.2–3.8 star average and recent 1–2 star review clusters citing the *same* flaw.
- **Tool**: Manual review scraping or `amazon-review-scraper` on GitHub.
- **Signal**: If the top complaint is a *fixable* manufacturing flaw (not a fundamental
  design issue), that's the vulnerability.

---

## Tier 3: Saturation Indicators

### Facebook Ad Library
- **URL**: facebook.com/ads/library
- **What to look for**: Search the product keyword. Count number of active ads. Check
  ad start dates — if most ads started in the last 30 days, the rush is beginning.
  If ads have been running 90+ days with high spend, it's late-stage.
- **Interpretation**: 0–5 ads = pre-rush. 6–30 = entering. 30+ active = rush underway.
  100+ = saturated.

### AliExpress / CJDropshipping
- **What to look for**: Order volume on product listings. "Top Selling" badge.
  If a product shows 10,000+ orders in the last month, multiple suppliers exist = you
  can negotiate or switch easily.

---

## Scraping Stack (Python)

```python
# Minimal monitoring stack
pip install praw pytrends requests beautifulsoup4

# Reddit signal monitor
import praw
reddit = praw.Reddit(client_id='', client_secret='', user_agent='arbitrage-radar')
subreddit = reddit.subreddit('BuyItForLife+malelivingspace')
for post in subreddit.search('wish there was', time_filter='month', limit=50):
    print(post.title, post.score)

# Google Trends confirmation
from pytrends.request import TrendReq
pytrends = TrendReq()
pytrends.build_payload(['posture corrector'], timeframe='today 3-m')
df = pytrends.interest_over_time()
print(df.tail(4))  # Last 4 weeks — is slope positive?
```

---

## Asset Class-Specific Sources

### Stocks
- Glassdoor / LinkedIn hiring data (proxy for company growth direction)
- Supply chain forums (industry-specific Reddit equivalents)
- Earnings call transcript sentiment delta (compare last 3 quarters)

### Crypto
- GitHub commit frequency: github.com/[project-repo]/commits
- Discord member growth rate (manual or Statbot bot)
- Nansen / Dune Analytics: wallet concentration and on-chain activity

### Dropshipping
- CJDropshipping trending products (updated weekly)
- Ecomhunt / Minea (paid tools for validated product signals)
- Zik Analytics (eBay/Amazon cross-platform trend data)
