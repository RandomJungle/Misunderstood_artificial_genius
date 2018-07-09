import os
import nltk
import re
import random
from math import log
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.text import Text 
from nltk import ConditionalFreqDist, FreqDist
from nltk.collocations import *

class Misunderstood_genius:
	
	root = "C:/Users/juliette.bourquin/Desktop/writers/"
	
	def __init__(self, master) :
		'''	Constructor. master is a string that names a directory in the same repository that contains all the work from inspiration
		'''	
		self.master = master
		self.reader = PlaintextCorpusReader(self.root+master, r'.*', encoding='utf-8')
		self.text = self.reader.words()
		
	def generate_model(self, word, num=50):
		'''	write a text based on most probable word to appear after each word. Prone to looping
		'''
		bigrams = nltk.bigrams(self.text)
		cfdist = nltk.ConditionalFreqDist(bigrams)
		print(cfdist[word].pformat())
		for i in range(num):
			print(word, end=' ')
			word = cfdist[word].max()
			
	def count_foot(self, word):
		vowels = ['a', 'e', 'u', 'i', 'y', 'o']
		splitword = word.split(vowels)
		return(len(splitword))

	def text_generator(self, word, num=10):
		''' write a text based on a random choice of word that appear in collocation in master's work
		'''
		verse = ""
		bigrams = nltk.bigrams(self.text)
		cfdist = nltk.ConditionalFreqDist(bigrams)
		for i in range(num):
			verse += word + ' '
			word_collocates = []
			for w in cfdist[word] :
				word_collocates.append(w)
			word = random.choice(word_collocates)
		return verse
	
	def rhyme_generator(self, word, rhyme, foot=12):
		''' write a verse based on previous word used. For now it doesn't actually counts in foot, change that
		'''	
		verse = ""
		bigrams = nltk.bigrams(self.text)
		cfdist = nltk.ConditionalFreqDist(bigrams)
		for i in range(foot):
			verse += word + ' '
			word_collocates = []
			for w in cfdist[word] :
				word_collocates.append(w)
			if i < 12 :
				word = random.choice(word_collocates)
			else :
				rhyming_collocate = [word for word in word_collocates if word.endswith(rhyme)]
				word = random.choice(rhyming_collocates)
				verse += word 
		return verse
		
	def compose_standard_poem(self, length):
		'''	write a poem with each verse starting with most commons words in master's work
		'''	
		poem =''
		all_word_dist = nltk.FreqDist(w.lower() for w in self.text)
		mostcommon= all_word_dist.most_common(length)
		for word in [x[0] for x in mostcommon if re.search('[a-zA-Z]', x[0]) is not None]:
			verse = self.text_generator(word, title=title)
			poem += verse + '\n'
		return poem
			
	def compose_random_poem(self, length):
		'''	write a poem with each verse starting with random words from master's work
		'''
		poem = ''
		for word in random.sample([x for x in self.text if re.search('[a-zA-Z]', x) is not None], length):
			verse = self.text_generator(word, title=title)
			poem += verse + '\n'
		return poem
	
	def compose_prose_poem(self, length):
		'''	write a text that jumps to line after every n number of words, but is composed of one block only
		'''	
		final_work = ""
		first_word = random.choice([w.lower() for w in self.text if re.search('[a-zA-Z]', w) is not None])
		paragraph = self.text_generator(word=first_word, num=length)
		paragraphlist = paragraph.split(' ')
		for i in range(1,len(paragraphlist)) :
			final_work += paragraphlist[i] + ' '
			if i % 10 == 0 :
				final_work += '\n'
		return final_work
	
	def compose_rhyming_poem(self, length, foot):
		''' write a poem that rhymes
		'''	
		final_work = ""
		first_word = random.choice([w.lower() for w in self.text if re.search('[a-zA-Z]', w) is not None])
		first_verse = self.rhyme_generator(word=first_word, foot=12, rhyme='oi')
			
	
	def find_title(self):
		'''	find the best title to capture the essence of his work, through random search into words
		'''
		first_word = random.choice([w.lower() for w in self.text if re.search('[a-zA-Z]', w) is not None])
		length = random.choice([1,2,3,4,5,6,7,8,9])
		title = self.text_generator(word=first_word, num=length)
		return title
			
	def draft_manuscript(self, title, func, length):
		'''	write a piece of text to a file, send it to everyone in town and wait for the letters of rejection
		'''
		masterpiece = func(length)
		with open(self.root+title+'.txt', 'w', encoding='utf-8') as manuscript :
			manuscript.write(masterpiece)
			signature = re.sub("(^[a-zA-Z])(/)(.)*?", "\1", self.master.capitalize())
			manuscript.write('\n\n\t\t\t\t' + signature)
				
if __name__ == "__main__" : 
	
	spleener = Misunderstood_genius('collectif')
	print(spleener.count_foot('angels'))
	#work_title = spleener.find_title()
	#spleener.draft_manuscript(title=work_title, func=spleener.compose_structured_poem, length=100)