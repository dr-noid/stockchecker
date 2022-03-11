from abc import ABC, abstractmethod

import pyppeteer
import stockchecker
from bs4 import BeautifulSoup
from bs4.element import Tag
from fake_useragent import FakeUserAgent

from models.product import Product
from models.scrapedproduct import ScrapedProduct


class Website(ABC):
    """Abstract website class"""
    compatible_stocks: list[str]

    def __init__(self, price_filter: bool = True, availability_filter: bool = True):
        self.products: list[Product] = []
        self.scraped_products: list[ScrapedProduct] = []
        self.price_filter = price_filter
        self.availability_filter = availability_filter
        self.ua = FakeUserAgent()

    async def run(self) -> None:
        """
        Use the products URLs to scrape data

        Returns `True` if all requests passed succesfully or
        `False` if one of them failed.
        `Note:` Only one request has to fail for this method to return `False`,
        some data may still have been scraped.
        """
        self.driver = await pyppeteer.launch(defaultViewport={"width": 1920, "height": 1080})

        self.log("Running")

        for product in self.products:
            scraped = await self.scrape_product(product)
            self.scraped_products.extend(scraped)

        await self.driver.close()

        stockchecker.save_products(self.scraped_products)

    async def request(self, url: str) -> str:
        page = await self.driver.newPage()
        await page.setUserAgent(self.ua.random)
        await page.goto(url, waitUntil='networkidle2')
        return await page.content()

    async def get_soup(self, url: str) -> BeautifulSoup:
        """
        Make a request to the given url,
        The `delay` param is the amount of time to wait for dynamic content to load.
        (For SSR webapps)
        """
        return BeautifulSoup(await self.request(url), "html.parser")

    def validate_scraped(self, scraped_product: ScrapedProduct | None, product: Product) -> bool:
        """Returns `True` if the passed `ScrapedProduct` is valid."""
        if scraped_product is None:
            return False
        if self.price_filter:
            if scraped_product.item_price > product.price_threshold:
                return False
        if self.availability_filter:
            if not scraped_product.availability:
                return False
        return True

    def check_availability(self, stock_desc: str) -> bool:
        for x in self.compatible_stocks:
            if stock_desc.find(x) != -1:
                return True
        return False

    def name(self, lower: bool = True) -> str:
        if lower:
            return self.__class__.__name__.lower()
        return self.__class__.__name__

    def log(self, message):
        print(f"{self.name().upper()} LOG: {message}")

    @abstractmethod
    async def scrape_product(self, product: Product) -> list[ScrapedProduct]:
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
        """
        Parses a `float` price from a string,
        every `Website` subclass has it's own implementation for this method.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.name()}\n Products: {self.products}"
