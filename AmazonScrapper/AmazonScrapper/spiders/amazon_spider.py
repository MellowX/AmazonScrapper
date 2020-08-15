import scrapy
from ..items import AmazonscrapperItem
import json


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['amazon.com']

    search_term = input('Enter a term to search on Amazon: ')

    start_urls = [
        'https://www.amazon.in/s?k={0}'.format(search_term)
    ]

    def parse(self, response):
        items = AmazonscrapperItem()

        product_name = response.css('.a-size-base-plus.a-text-normal').css('::text').extract()
        product_brand = response.css('.s-line-clamp-1 .a-color-base').css('::text').extract()
        product_price = response.css('.a-price:nth-child(1) .a-offscreen').css('::text').extract()
        product_image = response.css('.s-image::attr(src)').extract()
        product_rating = response.css('.a-icon-star-small .a-icon-alt').css('::text').extract()

        items['product_name'] = product_name
        items['product_brand'] = product_brand
        items['product_price'] = product_price
        items['product_image'] = product_image
        items['product_rating'] = product_rating

        # create json 
        finalJSON = getProductJSON(items)
        print("Final JSON = " + str(finalJSON))

    

# returns product list json object
def getProductJSON(items):
    product_name_list = items['product_name']
    product_brand_list = items['product_brand']
    product_price_list = items['product_price']
    product_image_list = items['product_image']
    product_rating_list = items['product_rating']
    # print(product_rating_list)
    product_list = []

    for i in range(len(product_name_list)):
        single_product_dict = {}
        try:
            single_product_dict['product_name'] = product_name_list[i]
            single_product_dict['product_image'] = product_image_list[i]
            single_product_dict['product_price'] = product_price_list[i]
            single_product_dict['product_brand'] = product_brand_list[i]
            single_product_dict['product_rating'] = product_rating_list[i]
        except:
            continue
        # print(single_product_dict)
        product_list.append(single_product_dict)

    #  create a empty dictionary
    product_list_dict = {}
    # Add product list array to dict
    product_list_dict['product_list'] = product_list

    # convert to json
    product_json_dump = json.dumps(product_list_dict)
    products_json_obj = json.loads(product_json_dump)
    # print(products_json_obj)

    # return in json format
    return products_json_obj