from ollama import chat
import html2text
import requests
version = 0.1
def search(query):
	webpages = []
	headers = {'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) RocketAIsearch/{version} Safari/537.36'}
	query = str(query)
	api_key = "" #api key here for google search engine api
	cx = '' #search engine id
	url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}'
	response = requests.get(url, headers=headers)
	results = response.json()
	for item in results.get('items', []):
		webpages.append(requests.get(item['link'], headers=headers))
#		print(f"Title: {item['title']}")
		print(f"Link: {item['link']}")
#		print(f"Snippet: {item['snippet']}\n")
	search_results = []
	for idx, webpage in enumerate(webpages, start=1):
		search_results.append(format(webpage.text))
		print(search_results[idx - 1])
	llm(search_results, query)
def format(html_content):
	text_maker = html2text.HTML2Text()
	text_maker.ignore_links = True  # Optional: Ignore links
	plain_text = text_maker.handle(html_content)
#	print(plain_text)
	return plain_text
def llm(input, prompt):
	tmp = ""
	for webpage in input:
		tmp = tmp + webpage + ", "
	response = chat(model='smollm2:1.7b', messages=[
		{'role': 'user', 'content': "The user searched for: " + str(prompt) + ". The system searched the internet and found the following:" + str(tmp)},
	])
	print("AI Responded: ")
	print(response['message']['content'])
query = input("Search query: ")
search(query)
