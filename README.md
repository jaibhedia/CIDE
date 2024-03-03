<p align="center">

</a>
	<h2 align="center"> Crawler </h2>
	<h4 align="center"> Scrape and Store Dark Web Sites along with therir Latency | Crawler for Dark Web | Search Engine Oriented <h4>
</p>


## Functionalities
- It's implemented using BFS and in coming time it's implementation will be changed to A* Search (Preferential Crawler)

- [x] fetch onion links
- [x] recursive fetching
- [x] store scrapped data
- [x] user added url
- [x] url blacklisting

<br>

## Increasing the crawler reach
```txt
Increase Crawl Depth
Add More starter links
Create more spiders with special focus on Directories
```

<br>

## Spiders
- `DRL` Link Dir Onion
	- A big directory of urls
- `UADD` User Added
	- Added by user
	- presently links are appened in _user_added_urls.txt_ under spider_data
	- Crawled in exactly similar fashion as to DRL

	
<br>


## Instructions to run

#### Pre-requisites:
	-  Py3
	-  Tor

#### < directions to install > 
```bash
pip install -r requirements.txt
```

#### < directions to execute > (For commit of [Jul 10, 2020](https://github.com/1UC1F3R616/onion-crawler/commit/75b0cbdabc4b2591e6c75ccf08a9fc127e7a4967))
- This commit contains pipeline to generate data in csv/json file
- You can run this without much effort

```bash
# start tor on port 9150
pproxy -l http://:8181 -r socks5://127.0.0.1:9150 -vv
scrapy crawl name_of_spider # DRL
```

#### < directions to execute > (After commit Jul 10, 2020)
- This commit contains data pipeline to save data on MongoDB Server
- You need to setup MongoDB Server connection credentials and URI in settings.py/pipeline.py file

## Sample JSON
- [DRL](https://github.com/1UC1F3R616/onion-crawler/blob/master/dark_web_scraping/scraped_data_DRL_2020-07-02T00-58-53.json)
- [UADD](https://github.com/1UC1F3R616/onion-crawler/blob/master/dark_web_scraping/scraped_data_UADD_2020-07-02T08-06-50.json)
- [TF-IDF Type](https://github.com/1UC1F3R616/onion-crawler/blob/master/dark_web_scraping/scraped_data.json)


## Bigger Datasets
- [DarkNet Dataset](https://1uc1f3r616.github.io/Dark-Net-Websites-Dataset/)

## StoryBoarding
Idea hamster: --

Developer: I had prior experience with web scraping but hadn't worked with web crawlers before and scraping the deep-web was also something new to me as it required setting up tor proxy. This project developed my interest in the web-mining subject and therefore it encorged me to take this subject as a subject in college curriculum. 

