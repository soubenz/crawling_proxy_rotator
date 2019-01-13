import json
from itertools import cycle
import requests
from requests.exceptions import ProxyError
import urllib3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class RandomProxy(object):

    def __init__(self):
        with open('proxy.json') as f:
            self.data = json.load(f)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_proxy(self):
        process = CrawlerProcess()
        process.crawl('proxy')
        return process.start()
    def load_proxy(self):
        proxies = set()
        for p in self.data:
            proxy_str = "{}://{}:{}".format(p['protocol'].lower(), p['proxy'], p['port'])
            proxies.add(proxy_str)
        return proxies


    def rotate_proxy(self):
        proxy_pool = cycle(self.load_proxy())
        url = 'https://httpbin.org/ip'
        working = 0
        while True:
            try:
                proxy = next(proxy_pool)
                response = requests.get(url,proxies={"http": proxy, "https": proxy},verify=False)
                return response.json()['origin']
                break
            except ProxyError:
                # print(proxy)
                pass
    # except:
    #     #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
    #     #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
    #     print("Skipping. Connnection error")





p = RandomProxy()
r = p.rotate_proxy()
print(r)
# p.get_proxy()