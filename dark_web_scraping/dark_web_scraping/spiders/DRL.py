from ..items import DarkWebScrapingItem

from collections import Counter
import lxml.html.clean
from string import punctuation
import logging

import scrapy
import nltk
from scrapy.utils.log import configure_logging
from nltk.corpus import stopwords

from nltk import PorterStemmer
from bs4 import BeautifulSoup


stemmer = PorterStemmer()


# GLOBALS
STOPS = set(stopwords.words("english"))

def cleanme(content):
    """
    input: A String
    return: A Word Count Dictionary 
    - Remove Tags
    - Special Character Free (\n, \r, \t, extra_space)
    - Remove Punctuations
    - Create Word List
    - Remove Stop words (English)
    - Use Steaming
    - Word Count | TF-IDF
    """
    # Remove Tags
    cleaner = lxml.html.clean.Cleaner(
        allow_tags=[''],
        remove_unknown_tags=False,
        style=True,
    )
    html = lxml.html.document_fromstring(content)
    html_clean = cleaner.clean_html(html)
    text = html_clean.text_content().strip()

    # Special Character Free
    text.lower()
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')

    # Remove Punctuations
    text = text.translate(str.maketrans('', '', punctuation))

    # Create Word List
    word_list = text.split(' ')

    # Remove Stop words (English)
    filtered_words = [word for word in word_list if word not in STOPS]

    # Steaming
    # tokens = [stemmer.stem(t) for t in filtered_words] # no stemming 06-09-2020 | will consider lemmatization

    # Word Count
    # return dict(Counter(tokens)) # no stemming
    return dict(Counter(filtered_words))

    # TF-IDF
    # word_counter = Counter(tokens)
    # total_words = sum(word_counter.values())
    # for key in word_counter:
    #     word_counter[key] = word_counter[key]/total_words
    # return word_counter


class DrlSpider(scrapy.Spider):

    name = 'DRL'
    allowed_domains = ['onion', 'i2p']

    start_urls =    ['http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion{}'.format(page) for page in range(1, 3)]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='DRL_LOGS.log',
        format='%(levelname)s %(asctime)s: %(message)s',
        level=logging.ERROR
    ) 


    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        links =set()
        content = soup.get_text()  # Get text content from the page


        # Keywords to search for
        keywords = ['drug', 'weapons', 'illegal', 'darkweb']

        # Search for keywords in the content
        for keyword in keywords:
            if keyword in content:
                # Keyword found, do something with the information (e.g., print URL)
                self.logger.info(f"Keyword '{keyword}' found on page: {response.url}")
                break  # Exit loop after first keyword found

        # Check if the page is from an i2p domain
        if '.i2p' in response.url:
            # Do something specific for i2p domains
            self.logger.info(f"This page is from an i2p domain: {response.url}")

        # Check if the page is from an onion domain
        elif '.onion' in response.url:
            # Do something specific for onion domains
            self.logger.info(f"This page is from an onion domain: {response.url}")

        # Continue crawling recursively
        # (You can add more conditions here for other types of domains or pages)
        for link in soup.find_all('a'):
            next_page = link.get('href')
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )

        # Title
        title = soup.title.text
        title_keywords = cleanme(title)

        # Meta Keywords & Description
        meta_tags = soup.find_all('meta')

        for meta_tag in meta_tags:
            if meta_tag.get('name') in ['keywords', 'Keywords']:
                keywords =  cleanme(meta_tag.get('content'))
                break
            else:
                keywords = ''

        for meta_tag in meta_tags:
            if meta_tag.get('name') in ['description', 'Description']:
                # description =  cleanme(meta_tag.get('content')) # not cleaning description as it's not a part of search param | 06-09-2020
                description =  str(meta_tag.get('content'))
                break
            else:
                description = ''

        word_frequency = cleanme(response.text)
        # print(dir(response))

        ## Older yield
        # yield {
        #     'url': response.url,
        #     'title': title,
        #     'title_keywords': title_keywords,
        #     'keywords': keywords,
        #     'description': description,
        #     'meta': response.meta,
        #     'links': links,
        #     'word_frequency': word_frequency
        # }

        ## New yield for API v1: 06-09-2020 | In v1 revision 2, we will be providing back the content also on a new endpoint
        ## Removing proxy key from Meta Data
        meta_data = {key:val for key, val in response.meta.items() if key not in ['proxy', 'download_timeout']}
        # item = DarkWebScrapingItem()
        # item['url'] = response.url
        # item['title'] = title
        # item['title_keywords'] = title_keywords
        # item['keywords'] = keywords
        # item['description'] = description
        # item['meta'] = meta_data
        # item['links'] = links

        # yield item

        yield {
            'url': response.url,
            'title': title,
            'title_keywords': title_keywords,
            'keywords': keywords,
            'description': description,
            'meta': meta_data,
        }

        # Recursion |  Change Depth Settings in Settings.py
        next_pages = links

        for next_page in next_pages:
            if next_page:
                yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)