# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
from collections import defaultdict

class ScrapeWithScrapyPipeline:
    def open_spider(self, spider):
        self.grouped_data = defaultdict(list)

    def process_item(self, item, spider):
        category = item['category_type']
        product_data = {
            "code": item.get('code', ''),
            "title": item.get('title', ''),
            "brand": item.get('brand', 'Unknown'),
            "price": item.get('price', ''),
            "review_count": item.get('review_count', '0 reviews'),
            "image_link": item.get('image_link', ''),
            "category_type": category,
        }
        self.grouped_data[category].append(product_data)
        return item

    def close_spider(self, spider):
        output = []
        for category, product in self.grouped_data.items():
            output.append({category: product})
        with open('category_product.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
