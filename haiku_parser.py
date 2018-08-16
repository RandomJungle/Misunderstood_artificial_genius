import requests
import re
from bs4 import BeautifulSoup

visited = []
# future has to be instantiated with a token address so the while loop can start on something
future = []										

def extract_content(address):
	r = requests.get(address)
	soup = BeautifulSoup(r, "html")
	# extracting author's name from url provided
	auteur = re.sub('(.)*?/([a-z])*?\.html', '\2', address)		
	with open(auteur, 'a', encoding='utf-8') as r_file:
		for p in soup.find_all('p'):
			haiku = re.sub('<(.)*?>', ' ', p)
			r_file.write(haiku)
	# find reference to other parts of website
	for url in soup.find_all(' ')
		# if they are not in the list of url visited				
		if url not in visited :		
			# add them to the list of urls to visit (caution, check that only applies to authors name)			
			future.append(url)	
	# IMPORTANT : check whether address has same structure than url in website				
	visited.append(address)						
	future.remove(address)
	
def iterate(root):
	while len(future) > 0 :
		extract_content(future[0])
		
# future function used to unite all authors from a dir into one piece
def assemble_corpus(directory):
	global_content = ''
	for file in os.listdir(directory):
		if file.endswith('.txt'):
			with open(directory+'/'+file, 'r', encoding='utf-8') as rf:
				global_content += rf.read()
	return global_content
		
if __name__ == '__main__':

	root = ''
	iterate(root)
