import scrapy
from urllib.parse import urljoin


class DivanLightingSpider(scrapy.Spider):
    name = 'divan_lighting'
    allowed_domains = ['divan.ru']
    start_urls = ['https://www.divan.ru/category/svet']

    def parse(self, response):
        # Собираем все карточки товаров на странице
        products = response.css('div._Ud0k')

        for product in products:
            yield {
                'name': product.css('span[itemprop="name"]::text').get().strip(),
                'price': product.css('meta[itemprop="price"]::attr(content)').get(),
                'url': urljoin('https://www.divan.ru', product.css('a::attr(href)').get()),
            }

        # Пагинация - переход на следующую страницу
        next_page = response.css('a[data-testid="pagination-next-button"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)