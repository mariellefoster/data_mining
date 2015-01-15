#Locality Sensitive Hashing
import re

def set_maker(enron_file, num_docs):
	i = 0
	sets = []
	doc_nums = []
	for line in enron_file:
		line = re.sub('\n', '', line)
		if len(line.split()) != 3:
			pass
		else:
			if i < num_docs:
				
				info = line.split(" ")
				#while still in document i
				#print int(line[0]),(i + 1)
				if int(info[0]) == (i + 1):
					doc_nums.append(int(info[1]))
				#when you've reached document i+1
				else:
					print "h"
					#make the set, start the next one
					doc = set(doc_nums)
					sets.append(doc)
					i += 1
			else:
				#represent each document as a set of words
				return sets

#Jaccard similarity 
def jaccard(doc1, doc2):
	pass

def sig_matrix(num_rows, doc1, doc2):
	pass

def main():
	
	#import enron data set, store in a \tmp file for grader happiness
	#Specify exceedingly clearly in comments where the string is 
	#that contains the location and name of the data file.
	
	enron_file = open("docword.enron.txt", 'r')

	
	#Prompt the user to enter in the number of documents for your program to read in from the file.
	
	num_docs = raw_input("Enter the number of documents you desire: ")
	sets = set_maker(enron_file, int(num_docs))
	
	print len(sets)
	print sets[0]
	# #Prompt the user to enter in two document id numbers. 
	# #Note that the document ids are indexed so they start at the number 1. 
	# #You may wish to subtract 1 from all document ids
	# doc1 = raw_input("Enter the first document id number you desire: ")
	# doc2 = raw_input("Enter the second document id number you desire: ")

	# #Print out the exact Jaccard similarity of these two documents.
	# jaccard(None, None)

	# #Prompt the user to enter in a number of rows to use for the signature matrix.
	# num_rows = raw_input("Enter the number of rows you desire: ")
	# sig_matrix(0, None, None)

	# #Print out an estimate of the Jaccard similarity for these same two documents 
	# #based on the signature matrix.

main()