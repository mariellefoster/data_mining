import math
import sys
import time
import random

def standardize():
	fl = open("data.txt", "r")

	#sum values and put them in useful arrays
	sum_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	values = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
	letters = []

	for line in fl:
		arr = line.split(",")
		i = 0
		for val in arr:
			if i == 0:
				letters.append(val)
			else:
				values[i-1].append(int(val))
				sum_values[i-1] += int(val)
			i += 1

	#calculate averages for each column
	k = 0
	averages=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in sum_values:
		i = float(i)
		s = 20000
		averages[k] = float(i/s)
		k += 1

	#calculate standard deviations for each column
	std_devs =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	a = 0
	for arr in values:
		square_root_sum = 0
		for val in arr:
			square_root_sum += float(((float(val) - float(averages[a]))*(float(val) - float(averages[a]))))
		std_devs[a] += float(math.sqrt(square_root_sum/20000))
		a += 1

	#Standardize Columns
	a= 0 
	for arr in values:
		k = 0
		for i in arr:
			arr[k] = (i - averages[a])/std_devs[a]
			k+=1
		a += 1
	
	values.insert(0, letters)
	return values

#Find k nearest neighbors
def knn(i, distance, k, values):
	rogers = [] #it's a beautiful day in the neighborhood...
	i_tot = 0	
	for n in range(20000):
		#make sure not to compare same row
		if n != i:
			if distance == "manhattan":
				for l in range(1,17):
					i_tot += abs(values[l][i] - values[l][n])

			if distance == "euclidean":
				for l in range(1,17):
					i_tot += (values[l][i] - values[l][n])*(values[l][i] - values[l][n])
				i_tot = math.sqrt(i_tot)

			if len(rogers) == 0:
				rogers.append([i_tot, n])
			else:
				for m in range(len(rogers)):
					if (m == len(rogers)-1) and (rogers[m][0] >= i_tot):
						rogers.append([i_tot, n])
						break
					if rogers[m][0] <= i_tot:
						rogers.insert(m, [i_tot, n])
						break

			if len(rogers) > k:
				rogers = rogers[1:]
		i_tot = 0
	return rogers

#Have those k neighbors vote on the classification
def classify(neighbors, values):
	letters = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for n in neighbors:
		letters[ord(values[0][n[1]])-65] += 1
	highest = 0
	index = 0
	curr = 0
	tie_indexes = []
	for i in letters:
		if i > highest:
			index = curr
			highest = letters[i]
		curr += 1
	#print letters[index]
	
	#find and break ties
	tie_index=0
	for i in letters:
		if i == letters[index]:
			tie_indexes.append(tie_index)
		tie_index += 1

	if len(tie_indexes) > 1:
		num = random.randint(0, len(tie_indexes) - 1)
		index = tie_indexes[num]

	return index

#correct or nah?
def correct_or_nah(i, classification, values, classifications):
	actual = ord(values[0][i])-65
	classifications[actual][classification] += 1

#confusion matrix
def confusion_matrix(classifications):
	letter = 0

	confusion_arr = []
	outfile = open("confusion_matrix.txt", "w")
	correct = 0
	outfile.write("Predicted (Horizontal Axis) and Actual (Vertical Axis) \n")
	outfile.write("\tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ\tK\tL\tM\tN\tO\tP\tQ\tR\tS\tT\tU\tV\tW\tX\tY\tZ\n")
	for letter_arr in classifications:
		total = 0
		correct += letter_arr[letter]
		line = chr(letter+65)
		k = 0

		while k < 26:
			line += "\t" + str(letter_arr[k])
			k+=1
		line += "\n"
		outfile.write(line)
		letter += 1
	# print correct

	#accuracy
	#print str(float(correct)/200)

def main():
	time1 = time.time()
	args = sys.argv
	if len(args) != 3:
		print "Error: Wrong number of arguments."
		quit()
	values = standardize()
	classifications = []
	for i in range(26):
		classifications.append([])
	for i in classifications:
		for k in range(26):
			i.append(0)

	#command line arguments
	for i in range(20000):
		neighbors = knn(i, args[2], int(args[1]), values)
		classification = classify(neighbors, values)
		correct_or_nah(i, classification, values, classifications)
	confusion_matrix(classifications)
	
	time2 = time.time()
	print time2-time1
main()
