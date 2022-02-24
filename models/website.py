import os
from abc import ABC, abstractmethod

import stockchecker
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
        self.driver = Chrome(
            executable_path=ChromeDriverManager().install(), options=options)

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

        stockchecker.save_products(self.scraped_products)

    def request(self, url: str, delay: int = 0) -> str:
        self.driver.get(url)

        self.driver.implicitly_wait(delay)

        return self.driver.page_source

    def get_soup(self, url: str, delay: int = 0) -> BeautifulSoup:
        """
        Make a request to the given url,
        The `delay` param is the amount of time to wait for dynamic content to load.
        (For SSR webapps)
        """
        return BeautifulSoup(self.request(url, delay), "html.parser")

    def price_check(self, threshold: int, price: float) -> bool:
        return int(price) < threshold

    def validate_data(self, scraped_product: ScrapedProduct, product: Product) -> bool:
        """
        Returns `True` if the scraped_product passes all the enabled filters.
        Products are automatically validated when using the `construct_product()` method
        """
        if self.price_filter:
            return self.price_check(product.price_threshold,
                                    float(scraped_product.item_price))
        if self.availability_filter:
            return scraped_product.availability
        return True

    def name(self, lower: bool = True) -> str:
        if lower:
            return self.__class__.__name__.lower()
        return self.__class__.__name__

    def validate_scraped(self, scraped_product: ScrapedProduct | None, product: Product) -> bool:
        """Returns `True` if the passed `ScrapedProduct` is valid."""
        if scraped_product is None:
            return False
        if not self.validate_data(scraped_product, product):
            return False
        return True

    def log(self, message):
        print(f"{self.name().upper()} LOG: {message}")

    @abstractmethod
    def scrape_product(self, product: Product) -> list[ScrapedProduct]:
        """
        Scrape a product, returns a `list[ScrapedProduct]`.
        If no items are found, returns an empty `list`.
        """

    @abstractmethod
    def find_product(self, product: Product, item: Tag) -> ScrapedProduct | None:
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

    def __repr__(self) -> str:
        return f"{self.name()}\n Products: {self.products}"
