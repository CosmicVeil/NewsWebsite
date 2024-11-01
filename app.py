# import libraries 
from flask import Flask, render_template, request 
from newsapi import NewsApiClient 

# init flask app 
app = Flask(__name__) 

# Init news api 
newsapi = NewsApiClient(api_key='1c4940703681426fa093f8aa12aa4da0') 

# helper function 
def get_sources_and_domains(): 
	all_sources = newsapi.get_sources()['sources'] 
	sources = [] 
	domains = [] 
	for e in all_sources: 
		id = e['id'] 
		domain = e['url'].replace("http://", "") 
		domain = domain.replace("https://", "") 
		domain = domain.replace("www.", "") 
		slash = domain.find('/') 
		if slash != -1: 
			domain = domain[:slash] 
		sources.append(id) 
		domains.append(domain) 
	sources = ", ".join(sources) 
	domains = ", ".join(domains) 
	return sources, domains 

@app.route("/", methods=['GET', 'POST']) 
def home(): 
	if request.method == "POST": 
		sources, domains = get_sources_and_domains() 
		keyword = request.form["keyword"] 
		related_news = newsapi.get_everything(q=keyword, 
									sources=sources, 
									domains=domains, 
									language='en', 
									sort_by='popularity') 
		no_of_articles = related_news['totalResults'] 
		if no_of_articles > 50: 
			no_of_articles = 50
		all_articles = newsapi.get_everything(q=keyword, 
									sources=sources, 
									domains=domains, 
									language='en', 
									sort_by='popularity', 
									page_size = no_of_articles)['articles'] 
		return render_template("home.html", all_articles = all_articles, 
							keyword=keyword) 
	else:
		sources, domains = get_sources_and_domains() 
		related_news = newsapi.get_everything(q="Climate Change", 
									sources=sources, 
									domains=domains, 
									language='en', 
									sort_by='popularity') 
		no_of_articles = related_news['totalResults'] 
		if no_of_articles > 50: 
			no_of_articles = 50
		all_articles = newsapi.get_everything(q="Climate Change", 
									sources=sources, 
									domains=domains, 
									language='en', 
									sort_by='popularity', 
									page_size = no_of_articles)['articles'] 
		return render_template("home.html", all_headlines = all_articles)
	return render_template("home.html") 

if __name__ == "__main__": 
	app.run(debug = True)
