# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse_hh)

    def vacancy_parse_hh(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        vacancy_link = response.css('div > meta[itemprop="url"]::attr(content)').extract_first()
        min_salary = response.css('div.vacancy-header ~ div div.vacancy-title > span > span > meta::attr(content)').extract_first()
        max_salary = response.css('div.vacancy-title meta[itemprop="maxValue"]::attr(content)').extract_first()
        yield JobparserItem(name=name, salary=min_salary, max_salary = max_salary, vacancy_link = vacancy_link)
