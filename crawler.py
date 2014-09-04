import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import urllib3

class Spider():

	def __init__(self, start_url):
		self.http = urllib3.PoolManager(10)
		self.start_url = start_url
		pass

	def get_links(self, url, type="", part=""):
		try:
		   r = self.http.request('GET', url)
		   html = r.data
		   soup = BeautifulSoup(html)
		   if self.start_url != url and part != "":
		   	  utils = soup.find("div", {'class':part})
		   	  return utils.findAll("a");
		   else:	      
		      return soup.findAll("a")
		except:
		   pass


	def crawl(self,start_url):
		urls = []
		visited = []
		urls.append(start_url)
		host = urlparse(start_url)

		while (len(urls) > 0):
			print(len(urls))
			link = urls.pop()
            
			try:
			   tags = self.get_links(link, "class", "category-products")
			   urlhost = urlparse(link)
			   for tag in tags:
				    l = urljoin(start_url,tag.get('href'))
				    if l not in visited and l.endswith("jpg") != True and l.endswith("pdf") != True and l.endswith("png") != True and urlhost.netloc == host.netloc:
					    print(l)
					    visited.append(l)
					    urls.append(l)
			except:
				pass
			
			
			pass
		pass
	

c = Spider("http://www.lafermedesanimaux.com/")
c.crawl("http://www.lafermedesanimaux.com/");
#http = urllib3.PoolManager()
#r = requests.get("http://www.cemsi.eu/");
#r = http.request('GET', 'http://www.cemsi.eu/')
#print(r.content);
