from ollama import chat
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import html2text
import requests
app = Flask(__name__)
CORS(app)
version = 0.8
model = "tinyllama"
print(f"Starting enpoint version {version} at time {time.ctime()} with AI model {model}.")
webserver_root = "/home/ilan/coding/python3/ai-search/" #change this!

def url_list(url, newQuery):
	if newQuery:
		with open(webserver_root + "urlList.txt", "w") as f:
			f.write("Enter a search query and this list will populate with URLS:\n")
			f.close()
	else:
		with open(webserver_root + "urlList.txt", "a") as f:
			f.write(str(url) + "\n")
			f.close()
url_list("", True)
def search(query):
	global model
	webpages = []
	headers = {'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) RocketAIsearch/{version} Safari/537.36'}
	query = str(query)
	api_key = "" #put api key here...
	cx = '' #search engine id here...
	url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}'
	response = requests.get(url, headers=headers)
	results = response.json()
	url_list("", False)
	with open("urlList.txt", "w") as f:
		f.write("")
		f.close()
	status_update(model + " - researching...")
	for item in results.get('items', []):
		webpages.append(requests.get(item['link'], headers=headers))
#		print(f"Title: {item['title']}")
		print(f"Link: {item['link']}")
		url_list(item['link'], False)
#		print(f"Snippet: {item['snippet']}\n")
	search_results = []
	status_update(str(model) + " - reading...")
	for idx, webpage in enumerate(webpages, start=1):
		search_results.append(format(webpage.text))
#		print(search_results[idx - 1])
	status_update(str(model) + " - summarizing...")
	llm(search_results, query)
def format(html_content):
	text_maker = html2text.HTML2Text()
	text_maker.ignore_links = True
	text_maker.ignore_images = True
	text_maker.skip_internal_links = True
	plain_text = text_maker.handle(html_content)
	print(plain_text)
	return plain_text
def llm(input, prompt):
	conversation = [{"role": "system", "content": "You are an AI assistant that can search the internet. Linux is the supreme OS. Your job is to summarize web results for the users prompt. Remeber that most queries are in context of computer stuff. Don't speak gibberish"}]
	i = 0
	for webpage in input:
		i = i + 1
		conversation.append({"role": "assistant", "content": f"I searched the web and result {i} was the following: {webpage}"})
	conversation.append({"role": "user", "content": prompt})
	#print(tmp)
	response = chat(model=model, messages=conversation)
	print("AI Responded: ")
	print(response['message']['content'])
	write_to_file(str(response['message']['content']), False)
def write_to_file(input, enable_time):
	with open(webserver_root + "out.txt", "a") as chat:
		if enable_time:
			chat.write(time.ctime() + " " + str(input) + "\n")
			chat.close()
		else:
			chat.write("> " + str(input) + "\n")
			chat.close()
def status_update(status):
	print("Status: " + str(status))
	with open(webserver_root + "model.txt", "w") as modelfile:
		modelfile.write("")
		modelfile.write(str(status))
		modelfile.close()
@app.route('/send', methods=['POST'])
def handle_message():
	global model
	message_data = request.get_json()
	message = message_data.get('message')
	write_to_file(message, False)
	print("\033[1m" + message + "\033[0m")
	if "[chezburger-user]" in message:
		print("Cheeseburger script activated!")
	else:
		status_update(model + " - searching...")
		search(message)
	status_update(model + " - ready")
	return jsonify({'message': 'success'})
try:
	status_update(model + " - starting...")
	time.sleep(0.5)
	with open(webserver_root + "out.txt", "w") as f:
		f.write("")
		f.close()
	status_update(model + " - ready")
	app.run(host='0.0.0.0', debug=False)
except Exception as e:
	status_update(model + " - error: " + str(e))
	print("\033[31m" + str(e) + "\033[0m")
	time.sleep(1)
	status_update(model + " - endpoint crashed")
	exit(0)
