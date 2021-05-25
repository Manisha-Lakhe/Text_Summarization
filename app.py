import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
import heapq
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def home():
	return render_template('Home.html')

@app.route('/summarize',methods=['POST'])
def summarize():
	if request.method == 'POST':
		my_file = request.form['myfile']
		if my_file:
			with open(my_file, "r",encoding="utf8") as f:
				article_text = f.read()
		else:
			article_text = request.form['text']

		article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
		article_text = re.sub(r'\s+', ' ', article_text)

		formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
		formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

		sentence_list = nltk.sent_tokenize(article_text)

		stopwords = nltk.corpus.stopwords.words('english')

		word_frequencies = {}
		for word in nltk.word_tokenize(formatted_article_text):
			if word not in stopwords:
				if word not in word_frequencies.keys():
					word_frequencies[word] = 1
				else:
					word_frequencies[word] += 1

		maximum_frequncy = max(word_frequencies.values())
		for word in word_frequencies.keys():
			word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
		maximum_frequncy = max(word_frequencies.values())

		sentence_scores = {}
		for sent in sentence_list:
			for word in nltk.word_tokenize(sent.lower()):
				if word in word_frequencies.keys():
					if len(sent.split(' ')) < 30:
						if sent not in sentence_scores.keys():
							sentence_scores[sent] = word_frequencies[word]
						else:
							sentence_scores[sent] += word_frequencies[word]
	
		summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
		summary = ' '.join(summary_sentences)

	return render_template('Result.html', summary=summary)

if __name__ == '__main__':
	app.run(debug=True)
