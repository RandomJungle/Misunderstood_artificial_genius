import os
import nltk
import re
import random
from math import log
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.text import Text 
from nltk import ConditionalFreqDist, FreqDist
from nltk.collocations import *

class Misunderstood_artificial_poet:
	
	def __init__(self, master) :
		'''	Constructor. master is a string that names a directory in the same repository that contains all the work from inspiration
		'''	
		self.master = 'masters/' + master
		self.reader = PlaintextCorpusReader(self.master, r'.*', encoding='utf-8')
		self.text = self.reader.words()
		
	def generate_model(self, word, num=50):
		'''	Writes a text based on most probable word to appear after each word. Prone to looping
		'''
		bigrams = nltk.bigrams(self.text)
		cfdist = nltk.ConditionalFreqDist(bigrams)
		print(cfdist[word].pformat())
		for i in range(num):
			print(word, end=' ')
			word = cfdist[word].max()
			
	def count_foot(self, word):
		''' Counts number of foot in word (doesn't account for jonctions for now)
		'''	
		startsWithVowel = False
		if re.match('[aeiouyàéèùôûâêîïöüäëÿ]', word):
			startsWithVowel = True
		splitword = re.split(pattern='[aeiouyàéèùôûâêîïöüäëÿ]', string=word, flags=re.IGNORECASE)
		cleansplit = [el for el in splitword if el is not '']
		if startsWithVowel :
			cleansplit.append('vowel')
		return(len(cleansplit))
		
	def check_rhyme(self, language, string, substring):
		''' Checks if the end of a string rhymes with a substring (could this be implemented via machine learning ?)
		'''
		pattern = re.sub('(.*?)([aeiouyàéèùôûâêîïöüäëÿ][zrtpmlkjhgfdsqwxcvbn]*?$)', '\2', string)
		if language == 'french':
			pattern = re.sub('', '', pattern)
		elif language == 'english':
			pass

	def text_generator(self, word, num=10):
		''' Writes a text based on a random choice of word that appear in collocation in master's work
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
	
	def rhyme_generator(self, inputWord, rhyme=None, foot=12):
		''' Writes a verse based on previous word used
		'''	
		verse = ""
		counted_foot = 0
		bigrams = nltk.bigrams(self.text)
		cfdist = nltk.ConditionalFreqDist(bigrams)
		continueWriting = True
		if rhyme is None :
			rhyme = random.choice([word for word in self.text if (len(word) > 3 and re.match('[a-zA-Z]', word))])[-3:]
		while continueWriting:
			word_collocates = []
			for w in cfdist[inputWord] :
				word_collocates.append(w)
			if counted_foot < foot-2 :
				word = random.choice(word_collocates)
				verse += word + ' '
			else :
				rhyming_collocates = [word for word in word_collocates if (word.endswith(rhyme) and self.count_foot(word) == 2 and word != inputWord)]
				if not rhyming_collocates:
					rhyming_collocates = [word for word in self.text if (word.endswith(rhyme) and self.count_foot(word) == 2 and word != inputWord)]
				word = random.choice(rhyming_collocates)
				verse += word + ' '
				continueWriting= False
			counted_foot += self.count_foot(word)
		verse = re.sub(' $', '', verse)
		return verse
		
	def compose_standard_poem(self, length):
		'''	Writes a poem with each verse starting with most commons words in master's work
		'''	
		poem =''
		all_word_dist = nltk.FreqDist(w.lower() for w in self.text)
		mostcommon= all_word_dist.most_common(length)
		for word in [x[0] for x in mostcommon if re.search('[a-zA-Z]', x[0]) is not None]:
			verse = self.text_generator(word, title=title)
			poem += verse + '\n'
		return poem
			
	def compose_random_poem(self, length):
		'''	Writes a poem with each verse starting with random words from master's work
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
		''' write a poem that rhymes. For now we use a simple rhyming techniques : AABBCCDD (it's boring but it's simple)
			Also the phonetics aren't fully implemented yet, so for now rhymes are based on the 3 last letters from previous verse
			EXTRA tricky for french with all usual mute letters that we love so much
		'''	
		final_work = []
		first_word = random.choice([w.lower() for w in self.text if re.search('[a-zA-Z]', w) is not None])
		verse = self.rhyme_generator(inputWord=first_word, foot=12, rhyme=None)
		final_work.append(verse)
		first_word = verse.split(' ')[-1]
		previous_rhyme = verse[-3:]
		for i in range(2,length):
			if i%2 != 0:
				verse = self.rhyme_generator(inputWord=first_word, rhyme=None)
				previous_rhyme = verse[-3:]
				final_work.append(verse)
			else:
				verse = self.rhyme_generator(inputWord=first_word, rhyme=previous_rhyme)
				final_work.append(verse)
		final_work = "\n".join(final_work)
		return final_work
			
	def find_title(self):
		'''	find the best title to capture the essence of his work, through random search into words
		'''
		first_word = random.choice([w.lower() for w in self.text if re.search('[a-zA-Z]', w) is not None])
		length = random.choice([1,2,3,4,5,6,7,8,9])
		title = self.text_generator(word=first_word, num=length)
		return title
			
	def draft_manuscript(self, title, func, **kwargs):
		'''	write a piece of text to a file, send it to everyone in town and wait for the letters of rejection
		'''
		masterpiece = func(**kwargs)
		with open('failed_attempts/'+title+'.txt', 'w', encoding='utf-8') as manuscript :
			manuscript.write(masterpiece)
			signature = re.sub("(^[a-zA-Z])(/)([a-zA-Z])(/)(.)*?", "\3", self.master.capitalize())
			manuscript.write('\n\n\t\t\t\t' + signature)
				
if __name__ == "__main__" : 
	
	spleener = Misunderstood_artificial_poet('hugo')
	work_title = spleener.find_title()
	spleener.draft_manuscript(title=work_title, func=spleener.compose_rhyming_poem, length=10, foot=12)