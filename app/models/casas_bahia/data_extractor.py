# -*- coding: utf-8 -*-
import re
from lxml.cssselect import CSSSelector  
from helpers.http_client import HttpClient
from helpers.processors import Processors
from helpers.brands import Brands
from helpers.memory import Memory

class DataExtractor():

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.processors = Processors()
        self.brands = Brands()
        self.memory = Memory()


    #{ _id, available, brand, color, display_feature, display_size, graphics_processor_name, graphics_processor, name, operating_system, price, processor, ram_memory, sku, screen_resolution, storage, storage_type, url, img_url}

    # TODO: color, display_feature, display_size, graphics_processor_name, graphics_processor, operating_system, ram_memory, sku, screen_resolution, storage, storage_type, img_url 

    def parse(self):
        data = {}
        data['name'] = self.response.xpath('//b[@itemprop="name"]/text()')
        data['name'] = self.validate_field(data, 'name')
        data['url'] = self.url
        data['price'] = self.response.xpath('//i[@class="sale price"]/text()')
        data['price'] = self.normalize_price(data['price'])
        data['available'] = data['price'] != None or data['price'] != 0.0 
        data['processor'] = self.response.xpath('//*[@class="Processador"]/dd/text()')
        data['processor'] = self.normalize_processor(self.validate_field(data, 'processor'))
        data['brand'] = self.normalize_brand(data['name'])
        selector = CSSSelector('.Memoria-RAM dd')
        data['ram_memory'] = self.response)
        data['ram_memory'] = self.normalize_memory(self.validate_field(data, 'ram_memory'))


        return data

    def validate_field(self, data, field):
        return (data[field][0].strip() if (len(data[field]) > 0) else "")


    def normalize_memory(self, raw_data):
        print raw_data
        if (re.search('1', raw_data, re.IGNORECASE) != None):
            return self.memory.get_1GB()
        elif (re.search('2', raw_data, re.IGNORECASE) != None):
            return self.memory.get_2GB()
        elif (re.search('4', raw_data, re.IGNORECASE) != None):
            return self.memory.get_4GB()
        elif (re.search('6', raw_data, re.IGNORECASE) != None):
            return self.memory.get_6GB()
        elif (re.search('8', raw_data, re.IGNORECASE) != None):
            return self.memory.get_8GB()
        elif (re.search('10', raw_data, re.IGNORECASE) != None):
            return self.memory.get_10GB()
        elif (re.search('12', raw_data, re.IGNORECASE) != None):
            return self.memory.get_12GB()
        elif (re.search('14', raw_data, re.IGNORECASE) != None):
            return self.memory.get_14GB()
        elif (re.search('16', raw_data, re.IGNORECASE) != None):
            return self.memory.get_16GB()

    def normalize_price(self, raw_data):
        try:
            raw_data = raw_data[0].strip() if (len(raw_data) > 0) else 0.0
            raw_data = raw_data.replace('.', '').replace(',', '.')
            return float(raw_data)
        except ValueError:
            return 0.0


    def normalize_brand(self, raw_data):
        # ["Samsung", "Asus", "Acer", "Dell", "Apple", "Positivo", "LG", "Lenovo"]

        if (re.search('dell', raw_data, re.IGNORECASE) != None):
            return self.brands.get_dell()
        elif (re.search('asus', raw_data, re.IGNORECASE) != None):
            return self.brands.get_asus()
        elif (re.search('apple', raw_data, re.IGNORECASE) != None):
            return self.brands.get_apple()
        elif (re.search('acer', raw_data, re.IGNORECASE) != None):
            return self.brands.get_acer()
        elif (re.search('samsung', raw_data, re.IGNORECASE) != None):
            return self.brands.get_samsung()
        elif (re.search('positivo', raw_data, re.IGNORECASE) != None):
            return self.brands.get_positivo()
        elif (re.search('lenovo', raw_data, re.IGNORECASE) != None):
            return self.brands.get_lenovo()
        elif (re.search('lg', raw_data, re.IGNORECASE) != None):
            return self.brands.get_lg()


    def normalize_processor(self, raw_data):
        # ['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intem Pentium Quad Core', 'Intel Baytrail', 'AMD Dual Core', 'Item Atom', 'Intel Core M', 'Intel Celeron']

        # remove erros de enconding (ex: \u84d2)
        raw_data = re.sub('\\\u\w\w\w\w', '', raw_data)

        if (re.search("i3", raw_data, re.IGNORECASE) != None):
            return self.processors.get_i3()

        elif (re.search("i5", raw_data, re.IGNORECASE) != None):
            return self.processors.get_i5()

        elif (re.search("i7", raw_data, re.IGNORECASE) != None):
            return self.processors.get_i7()

        elif (re.search("Pentium", raw_data, re.IGNORECASE) != None):
            return self.processors.get_pentium_quad()

        elif (re.search("byt|baytrail", raw_data, re.IGNORECASE) != None):
            return self.processors.get_baytrail()

        elif (re.search("amd.+dual core", raw_data, re.IGNORECASE) != None):
            return self.processors.get_amd_dual()

        elif (re.search("atom", raw_data, re.IGNORECASE) != None):
            return self.processors.get_atom()

        elif (re.search("Intel.+Core.+M", raw_data, re.IGNORECASE) != None):
            return self.processors.get_core_m()

        elif (re.search("Celeron", raw_data, re.IGNORECASE) != None):
            return self.processors.get_celeron()

        elif (re.search("arm", raw_data, re.IGNORECASE) != None):
            return self.processors.get_arm_a9()

        elif (re.search("samsung", raw_data, re.IGNORECASE) != None):
            return self.processors.get_samsung()
          
        

