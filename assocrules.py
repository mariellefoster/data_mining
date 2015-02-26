#Marielle Foster and Nick Petru
#Data Mining 324

import heapq
import itertools

#read in movie data
## GRADER NOTE: Place the movies and rating data in the same folder as this program
def read_in_mov():

	fl = open("movies.dat", 'r')
	arr = [None for i in range(3953)]
	arr.append(0)
	for line in fl:
		l = line.split("::")
		if len(l) > 1:
			arr[int(l[0])] = (l[1])
	return arr

#function to read in mid size data
## GRADER NOTE: Place the movies and rating data in the same folder as this program
def read_in_mid():
	fl = open("ratings.dat", 'r')
	arr = [[] for i in range(6041)]
	for line in fl:
		l = line.split("::")
		if len(l) > 1:
			arr[int(l[0])].append(int(l[1]))
	for user in arr:
		user = set(user)
	return arr

# find frequent item_sets of size one
def find_item_sets(support, data, candidate_list):
	movie_arr = [[0, i] for i in range(3953)]

	for user in data:
		for movie in user:
			movie_arr[movie][0] += 1

	#sorts movies based on how many reviews they got
	movie_arr = heapq.nlargest(3953, movie_arr)

	i = 3952
	#finds the movies above the threshhold
	while movie_arr[i][0] < support:
		i -= 1
	
	movie_arr = movie_arr[:i]
	item_set = []
	candidates_dict = {}
	#makes an item_set with just the movie numbers
	for movie in movie_arr:
		ID = [movie[1]]
		ID = set(ID)
		item_set.append(ID)
		candidates_dict[movie[1]] = movie[0]
	candidate_list.append(candidates_dict)
	return item_set



#makes printing prettier
def list_string(lst):
	string = ''
	i = 0
	for item in lst:
		if item != None:
			string += str(item) + ", "
		i += 1
	#takes off last ', '
	string = string[:len(string)-2]

	return string

def apriori(item_sets, transactions, support, candidate_list):
	k = 1
	item_sets = heapq.nsmallest(len(item_sets), item_sets)
	#while F_k is not empty
	last_item_list = list()
	while item_sets:
		#find all frequent item_sets at that confidence threshhold
		k += 1		
		# Generate candidate item_sets
		candidate_list.append(generate_candidates(item_sets, k, support, candidate_list[k-2]))

		for t in transactions:
			# identify all candidates that belong to t
			candidate_list[k-1] = subset(candidate_list[k-1], sorted(t))	
	
		item_sets = extraction(candidate_list[k-1], support, [], [])
		for item_set in item_sets:
			last_item_list.append(item_set)
	return last_item_list

def extraction(candidates, support, item_sets, key_set):
	for key, value in candidates.iteritems():
		if isinstance(value, dict):	
			key_set.append(key)
			item_sets = extraction(value, support, item_sets, key_set)
			key_set.pop()
		else:
			if value >= support:
				key_set.append(key)
				temp = set(key_set)
				item_sets.append(temp)
				key_set.pop()
	return item_sets

# create candidate subset belonging to t
def subset(candidates, t):
	if not t:
		return candidates
	ID = t[0]
	if ID in candidates:
		if isinstance(candidates[ID], int):
			candidates[ID] += 1
			return subset(candidates, t[1:])
		else:
			candidates[ID] = subset(candidates[ID], t[1:])
	return subset(candidates, t[1:])

# populate the hash tree such that keys are ids 
# and values are dictionaries until the leaves (which are counts)
def generate_candidates(item_sets, k, support, prev_cands):
	candidates = []
	i = 1
	for item_set in item_sets:
		item_set = set(item_set)
	for item_set in item_sets:
		for m in range(i, len(item_sets)):
			u = item_set.union(item_sets[m])	
			if len(u) == k:

				#prune candidates
				if len(item_set) > 1:
					if u not in candidates:
						if prune(u, prev_cands, item_sets[m], item_set, support):						
							candidates.append(u)
				else:
					if u not in candidates:
						candidates.append(u)
		i += 1

	final_candidates = {}
	#You should print out the number of candidate item_sets you have of each size right before you go
	#back to the data to actually count.
	print "Number of Candidates: ", len(candidates)
	if candidates:
		print "Currently searching for frequent subsets of size: ", len(candidates[0])
		for cand in candidates:
			rec_build_tree(sorted(cand), final_candidates)
	return final_candidates

#prunes infrequent candidate
def prune(cand, prev_cands, s, t, support): #s and t are sets
	combos = set(itertools.combinations(cand, len(s)))
	for combo in combos:
		if combo != s and combo != t:
			sup = support_func(prev_cands, sorted(list(combo)))
			if support > sup:
				return False
	return True

# build the candidate hash tree recursively
def rec_build_tree(cand, hash_tree):
	#base case
	if not cand:
		return hash_tree

	#go deeper
	if cand[0] not in hash_tree:
		if len(cand) > 1:
			item = cand[0]
			hash_tree[item] = {}
			cand.remove(item)
			return rec_build_tree(cand, hash_tree[item])
		else:

			hash_tree[cand[0]] = 0
	else:
		item = cand[0]
		cand.remove(item)
		return rec_build_tree(cand, hash_tree[item])
	
#create tuples of association rules
def genrules(candidate_list, final_item_sets, confidence):
	rules = []
	for item_set in final_item_sets:
		subsets = set(itertools.combinations(item_set, len(item_set)-1))
		for subset in subsets:
			consequent = item_set-set(subset)
			antecedent = set(subset)

			#solve for a rule's confidence
			conf_denom = support_func(candidate_list[0], list(consequent))
			conf_num = support_func(candidate_list[len(item_set)-2], list(antecedent))
			conf = conf_num/float(conf_denom)
			
			if conf >= confidence:
				rules.append((antecedent, consequent))
	return rules

#finds the support of a candidate located in hash tree
def support_func(cand_tree, candidate):
	if not candidate:
		return 0
	while isinstance(cand_tree, dict):
		item = candidate[0]
		candidate.remove(item)
		if item in cand_tree:
			cand_tree = cand_tree[item]
		else:
			return 0
	return cand_tree
	

def get_movie_names(movie_names, item_sets):
	name_sets = []
	for item in item_sets:
		name_sets.append(movie_names[item])
	return name_sets

def main():
	## GRADER NOTE: Place the movies and rating data in the same folder as this program
	transactions = read_in_mid()
	support = raw_input("What do you want the threshhold to be? ")
	support = int(support)
	confidence = raw_input("What do you want the confidence to be? ")
	confidence = float(confidence)

	movie_names = read_in_mov()
	#find all frequent 1-item_sets
	candidate_list = []
	item_sets = find_item_sets(support, transactions, candidate_list)
	
	final_item_sets = apriori(item_sets, transactions, support, candidate_list)

	print "Final Item Sets: "
	for item in final_item_sets:
		print list_string(get_movie_names(movie_names, item))
	print "Rules: "
	rules = genrules(candidate_list, final_item_sets, confidence)
	for rule in rules:
		print list_string(get_movie_names(movie_names, rule[0])), " -> ", list_string(get_movie_names(movie_names, rule[1]))


main()