import os
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from models.product import Product
from models.scrapedproduct import ScrapedProduct

os.environ["WDM_PRINT_FIRST_LINE"] = "False"
os.environ["WDM_LOG_LEVEL"] = '0'

options = Options()
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])


class Website(ABC):
    """Abstract website class"""

    def __init__(self, price_filter: bool = True, availability_filter: bool = True):
        self.products: list[Product] = []
        self.scraped_products: list[ScrapedProduct] = []
        self.price_filter = price_filter
        self.availability_filter = availability_filter

    def run(self) -> None:
        """
        Use the products URLs to scrape data

        Returns `True` if all requests passed succesfully or
        `False` if one of them failed.
        `Note:` Only one request has to fail for this method to return `False`,
        some data may still have been scraped.
        """
        for product in self.products:
            scraped = self.scrape_product(product)

            self.scraped_products.extend(scraped)

    def request(self, url: str, delay: int = 0) -> str:
        """
        Make a request to the given url,
        delay is the amount of time to wait for dynamic content to load.
        """
        driver = Chrome(
            executable_path=ChromeDriverManager().install(), options=options)

        driver.get(url)

        driver.implicitly_wait(delay)

        return driver.page_source

    def soupify(self, page_source: str | bytes) -> BeautifulSoup:
        return BeautifulSoup(page_source, "html.parser")

    def price_check(self, threshold: int, price: float) -> bool:
        return int(price) < threshold

    def validate_data(self, product: Product, scraped_product: ScrapedProduct) -> bool:
        result: bool = True
        if self.price_filter:
            result = self.price_check(product.price_threshold,
                                      scraped_product.item_price)
        if self.availability_filter:
            result = scraped_product.availability
        return result

    def name(self, lower: bool = True) -> str:
        if lower:
            return self.__class__.__name__.lower()
        return self.__class__.__name__

    @abstractmethod
    def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        """
        Scrape a product, returns a `list[ScrapedProduct]`.
        If no items are found, returns an empty `list`.
        """

    @abstractmethod
    def create_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
        """
        Construct a ScrapedProduct object and return it.
        If any checks fail return `None`.
        """

    @abstractmethod
    def strip_price(self, price: str) -> float:
        pass

    @abstractmethod
    def check_availability(self, stock_desc: str) -> bool:
        pass
