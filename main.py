import argparse
from src.scrape import Scraper

parser = argparse.ArgumentParser(
    prog="Mee6-Levels-Please", description="Scrape level data from a m**6 leaderboard."
)
parser.add_argument("url", type=str, help="The URL of the m**6 leaderboard")
parser.add_argument("driver", type=str, help="The WebDriver that you have installed")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode for logging")
args = parser.parse_args()

scraper = Scraper(args.url, args.driver, args.verbose)
