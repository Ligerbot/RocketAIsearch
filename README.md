# RocketAIsearch
RocketAIsearch is an LLM search engine.
# How it works
* RocketAIsearch uses the Google search API to gather 10 of the most relevant sources.
* This info is then fed into the LLM, which can be chosen by modifying the Python file.

__This project uses Ollama so the Ollama server must be running__
# Setup
* First, run a webserver in the root directory of the project. I used python's simple http server and it worked well.
* Second, set your API key and search engine ID in the python file. Search up "google search api" for help. Also be sure to change the model in use. tinyllama is very bad but I am forced to use it because my laptop is bad.
* Run `python3 rocketAIsearch.py`
# Info
### Currently I am no longer working on this project. I may update it occasionally.
