import requests
'''代理IP地址（高匿）'''
proxy = {
    'http': 'http://150.109.244.196:81',

}
'''head 信息'''
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
             'Connection': 'keep-alive'}
url = 'http://icanhazip.com'
p = requests.get('http://www.pornhub.com', headers=head, proxies=proxy)
print(p.text)