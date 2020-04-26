from typing import Union

import requests
from bs4 import BeautifulSoup, NavigableString


class CountryStats:
    def __init__(self, country_name: str, total_cases: str, new_cases: str, total_deaths: str, new_deaths: str,
                 total_recovered: str, active_cases: str, critical_cases: str, cases_per_1m_pop: str,
                 deaths_per_1m_pop: str, total_tests: str, tests_per_1m_pop: str) -> str:
        self.country_name: str = country_name
        self.total_cases: str = total_cases
        self.new_cases: str = new_cases
        self.total_deaths: str = total_deaths
        self.new_deaths: str = new_deaths
        self.total_recovered: str = total_recovered
        self.active_cases: str = active_cases
        self.critical_cases: str = critical_cases
        self.cases_per_1m_pop: str = cases_per_1m_pop
        self.deaths_per_1m_pop: str = deaths_per_1m_pop
        self.total_tests: str = total_tests
        self.tests_per_1m_pop: str = tests_per_1m_pop


def __extract_country_stats(country_table: Union[BeautifulSoup, NavigableString], country_name: str) -> list:
    stats: list = list()
    for row in country_table.find_all('tr'):
        if country_name in row.text:
            stats = row.text.splitlines()

    return stats


def __parse_country_stats(stats: list) -> CountryStats:
    country_stats: CountryStats = CountryStats(stats[1], stats[2], stats[3], stats[4], stats[5], stats[6], stats[7],
                                               stats[8], stats[9], stats[10], stats[11], stats[12])
    return country_stats


def __display_stats(country_stats: CountryStats) -> str:
    stats: str = (' Country:{}\n Total Cases:{} \n New Cases:{}\n Total Deaths:{}\n New Deaths:{}\n'
                  ' Total Recovered:{}\n Active Cases:{}\n Critical Cases:{}\n Tot Cases/1M pop:{}\n'
                  ' Deaths/1M pop:{}\n Total Tests:{}\n Tests/1M pop:{}'.
                  format(country_stats.country_name, country_stats.total_cases, country_stats.new_cases,
                         country_stats.total_deaths,
                         country_stats.new_deaths, country_stats.total_recovered, country_stats.active_cases,
                         country_stats.critical_cases,
                         country_stats.cases_per_1m_pop, country_stats.deaths_per_1m_pop, country_stats.total_tests,
                         country_stats.tests_per_1m_pop))
    return stats


def scrape(url: str, tag_type: str, tag_class: str, country_name: str) -> str:
    results: requests.Response = requests.get(url)
    beautifier: BeautifulSoup = BeautifulSoup(results.content, 'html.parser')
    country_table: Union[BeautifulSoup, NavigableString] = beautifier.find(tag_type, class_=tag_class)
    stats: list = __extract_country_stats(country_table, country_name)
    country_stats: CountryStats = __parse_country_stats(stats)
    return __display_stats(country_stats)
