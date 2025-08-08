import scrapy

from ..items import ProductItem

class ProductspiderSpider(scrapy.Spider):
    name = "productspider"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/"]

    def parse(self, response):
        categories = response.css('#nav-one > li')
        for category in categories:
            category_name = category.css('a::text').get()
            link = category.css('a::attr(href)').get()
            if link :
                yield response.follow(
                    link,
                    callback=self.parse_category,
                    meta={'category_type': category_name.strip() if category_name else "Unknown"})


    def parse_category(self, response):
        category_type = response.meta['category_type']
        products_links = response.css('div.product-block-inner > div.image > a::attr(href)').getall()

        for link in products_links :
            if link :
                yield scrapy.Request(
                    link,
                    callback=self.parse_product,
                    meta={'category_type':category_type}
                )

        next_page = response.css('ul.pagination li a:contains(">")::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_category,
                meta={'category_type': category_type}
            )

    def parse_product(self, response):
        item = ProductItem()
        item['code'] = response.xpath('//ul[@class="list-unstyled"]/li[span[contains(text(), "Product Code:")]]/text()').get(default='').strip()
        item['title'] = response.css('h3.product-title::text').get(default='').strip()
        item['brand'] = response.xpath('//ul[@class="list-unstyled"]/li[span[contains(text(), "Brand:")]]/a/text()').get(default='Unknown').strip()
        item['price'] = response.xpath('//ul[@class="list-unstyled price"]/li/h3/text()').get(default='').strip()
        item['review_count'] = response.css('div.rating-wrapper > a.review-count::text').get(default='0 reviews').strip()
        item['image_link'] = response.css('div.product-info > div > div.image > a::attr(href)').get(default='').strip()
        item['category_type'] = response.meta['category_type']

        yield item