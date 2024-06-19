import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import bs4
import humanfriendly
from rich import print

USER_BLOCK_CLASS = "hidden md:block"
USERNAME_CLASS = "ml-3 font-semibold text-dark-100"
MESSAGE_DATA_CLASS = "text-dark-300 hidden lg:flex items-center justify-center"
EXP_DATA_CLASS = "hidden lg:flex items-center justify-center text-dark-300"


class Scraper:
    def __init__(self, url: str, driver: str, verbose: bool = False):
        self.verbose = verbose
        self.url = url
        if self.verbose:
            print("[green]INFO:[/] Logging in verbose mode")
            print(f"[green]INFO:[/] Scraping target URL: {self.url}")

        driver = driver.lower().strip()
        if self.verbose:
            print(f"[green]INFO:[/] Matching for driver: {driver}")
        match driver:
            case "edge":
                self.driver = webdriver.Edge()
            case "firefox":
                self.driver = webdriver.Firefox()
            case "chrome":
                self.driver = webdriver.Chrome()
            case _:
                print(f"[red]ERROR[/]: Driver {driver} not implemented.")
                exit(1)

        if verbose:
            print(f"[green]INFO:[/] Driver selected: {driver}")

        self.get_page()
        self.close_driver()
        self.scrape_page()
        self.dump_to_json()

        if self.verbose:
            print("[green]INFO:[/] Scraper finished :)")

    def get_page(self):
        if self.verbose:
            print("[green]INFO:[/] Getting page for URL")

        self.driver.get(self.url)
        self.scroll_down()
        self.page = self.driver.page_source

        if self.verbose:
            print("[green]INFO:[/] Done getting page")

    def close_driver(self):
        if self.verbose:
            print("[green]INFO:[/] Closing driver")

        self.driver.close()

        if self.verbose:
            print("[green]INFO:[/] Done closing driver")

    def scroll_down(self):
        if self.verbose:
            print("[green]INFO:[/] Scrolling down page (may pause, be patient)")

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script(
                        "return document.body.scrollHeight"
                    )
                    > last_height
                )
            except Exception:
                break

            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

        if self.verbose:
            print("[green]INFO:[/] Done scrolling")

    def scrape_page(self):
        if self.verbose:
            print("[green]INFO:[/] Scraping page")

        self.soup = BeautifulSoup(self.page, "html.parser")
        self.user_elements: list[bs4.element.Tag] = self.soup.find_all(
            "div", class_=USER_BLOCK_CLASS
        )

        if self.verbose:
            print(f"[green]INFO:[/] User elements found: {len(self.user_elements)}")
            print("[green]INFO:[/] Done scraping page")

    def dump_to_json(self):
        if self.verbose:
            print("[green]INFO:[/] Dumping leveling data to json")

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M")
        self.file_path = f"./output/{formatted_datetime}.json"

        if self.verbose:
            print(f"[green]INFO:[/] Output file path: {self.file_path}")

        with open(self.file_path, "w") as f:
            self.lvl_data = []

            self.users = 0
            for user in self.user_elements:
                username = user.find(class_=USERNAME_CLASS).text
                messages = humanfriendly.parse_size(
                    user.find(class_=MESSAGE_DATA_CLASS).text
                )
                exp = humanfriendly.parse_size(user.find(class_=EXP_DATA_CLASS).text)

                data = {"username": username, "messages": messages, "exp": exp}

                self.lvl_data.append(data)
                self.users += 1

            # print(self.lvl_data)
            json.dump(self.lvl_data, f, indent=4)

        if self.verbose:
            print("[green]INFO:[/] Done dumping data")
