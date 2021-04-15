import scrapy

from scrapy.loader import ItemLoader

from ..items import AlwafabankItem
from itemloaders.processors import TakeFirst


class AlwafabankSpider(scrapy.Spider):
	name = 'alwafabank'
	start_urls = ['https://alwafabank.com/category/%d8%a3%d8%ae%d8%a8%d8%a7%d8%b1/']

	def parse(self, response):
		post_links = response.xpath('//p[@class="uk-margin-medium"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@property="headline"]/text()').get()
		description = response.xpath('//div[@class="uk-margin-medium-top"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=AlwafabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
