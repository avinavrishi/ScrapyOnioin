import requests
import re
import pandas as pd


def extractLinkFromHtml(content):
	regexPattern = r"\b\w+\.onion\b"
	matches = re.findall(regexPattern, content)[4:25]
	return matches
	

def findSearchEngineLinks(urlList):
	urlListAndContent = {}
	Tor_Proxy = {'http' : 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}

	for i in range(len(urlList)):
		res = requests.get(urlList[i], proxies = Tor_Proxy)
		if res.status_code == 200:
			html = res.content.decode()
			urlListAndContent[urlList[i]] = html
		else:
			print(f'something went wrong {res.status_code}')


	topResultSet = set()
	for val in urlListAndContent.values():
		results = extractLinkFromHtml(val)


		for result in results:
			topResultSet.add(result)

	return list(topResultSet)


def main():

	urlKeyword = ['iphone', 'buy iphone']

	urlList =[]
	for key in urlKeyword:
		if " " in key:
			new_string= key.replace(" ", "+")
			urlList.append(f'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={new_string}')
		else:
			urlList.append(f'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={key}')

	topResult= findSearchEngineLinks(urlList)

	for result in topResult:
		print(result)

	resultFile = {'Keywords': [','.join(urlKeyword)], 'URLS': [','.join(urlList)], 'topResult': [','.join(topResult)]}

	df = pd.DataFrame(resultFile)
	df.to_csv('output.xlsx', index=False)
	print(df, "\nData saved in output.xlsx")
	

	


if __name__ == '__main__':
	main()