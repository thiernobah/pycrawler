import requests
import urllib3
import re
import configparser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

class Spider():
	def __init__(self, start_url):
		self.http = urllib3.PoolManager(10)
		self.start_url = start_url
		parse_url = urlparse(self.start_url)
		self.host = parse_url.netloc
		pass

	def ini_parser(self, url):
		parse_url = urlparse(url)
		name = parse_url.netloc.split(".")[1]
		config = configparser.ConfigParser()
		config.read("queries/"+name+".ini")

		for k, s in config['DEFAULT'].items():
			print(k+"      "+s)

	def filter_url(self, url):
		parse_url = urlparse(url)
		name = parse_url.netloc.split(".")[1]
		f = open("urlfilter/"+name+".txt","r")
		for fil in f.readlines():
			print(fil)
			pass	

	def get_links(self, url, type="", part=""):
		try:
		   r = self.http.request('GET', url)
		   html = r.data
		   soup = BeautifulSoup(html)
		   if self.start_url != url and part != "":
		   	  utils = soup.find("div", {'class':part})
		   	  utils.find('div',{'class':'sort-by'}).decompose()
		   	  return utils.findAll("a");
		   else:	      
		      return soup.findAll("a")
		except:
		   pass

	def put_to_file(self, link):
		parse_url = urlparse(self.start_url)
		name = parse_url.netloc.split(".")[1]
		f = open("data/links/"+name+".txt", "a")
		f.write(link+"\n")
		f.close()	   

   
	def crawl(self,start_url):
		urls = []
		visited = []
		urls.append(start_url)
		#host = urlparse(start_url)

		while (len(urls) > 0):
			print(len(urls))
			link = urls.pop()
			self.put_to_file(link)
			try:
			   tags = self.get_links(link, "class", "category-products")
			   urlhost = urlparse(link)
			   for tag in tags:
				    l = urljoin(start_url,tag.get('href'))
				    if l not in visited and l.endswith("jpg") != True and l.endswith("pdf") != True and l.endswith("png") != True and urlhost.netloc == self.host and link.find("?dir=asc&order=position") == -1 :
					    print(l)
					    visited.append(l)
					    urls.append(l)
			except:
				pass
			pass
		f.close()	
		pass

#sort-by	
urls = "http://www.lafermedesanimaux.com/chiens.html"
c = Spider("http://www.lafermedesanimaux.com/")
#c.ini_parser("http://www.lafermedesanimaux.com/")

c.crawl(urls);
#http = urllib3.PoolManager()
#r = requests.get("http://www.cemsi.eu/");
#r = http.request('GET', 'http://www.cemsi.eu/')
#print(r.content);
