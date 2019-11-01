# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.xpath('//div[@class="_2g1F-"/@href')
        for link in vacancy:
            response.follow(link, self.vacancy_parse)
        pass

    def vacancy_parse_sj(self, response:HtmlResponse):
        vacancy_link = response.css("head > link[rel = 'canonical']::attr(href)").extract_first()
        name = ''.join(response.css('h1._3mfro.rFbjy.s1nFK._2JVkc *::text').extract())
        min_salary = json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary'][
            'value']['minValue']
        max_salary = json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary'][
            'value']['maxValue']
        yield JobparserItem(name = name, vacancy_link = vacancy_link, min_salary = min_salary, max_salary = max_salary)
