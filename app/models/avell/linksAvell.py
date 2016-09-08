# coding: utf-8
import scrapy
import json
import re

f = open('invalid_links.json', 'wb')
class SpiderAvell(scrapy.Spider):

#http://avell.com.br/notebooks
# LOJAS AVELL -- VANESSA
  name = 'spider'
  start_urls = ['http://avell.com.br/notebooks/']
  download_delay = 1.5

  def parse(self, response):
    for vitrine in response.css('.col-md-4.col-sm-6'):
      link_data = {
        'link' : vitrine.css('a::attr("href")').extract_first(),
        'name' : vitrine.css('.informations h2 a::text').extract_first()
      }
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(bateria|suporte|break|carca|tampa|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
        f.write(json.dumps(link_data) + '\n')

      # ou então, libere para o output do scrapy
      else:
        yield link_data

    link_next = response.css('li.next a::attr("href")').extract_first()
    if link_next:
      yield scrapy.Request(link_next)     
        
    #http://www.taqi.com.br:80/browse/category.jsp?categoryId=cat40004&q_pageNum=2
    # PAGINADOR É UM SELECT.


    