#Adaboost
#By Marielle Foster and Nick Petru
from numpy import *
import math
# import numpy

def read_in_data_titanic():
	fl = open("titanic.dat")

	data_points = []
	class_labels = []
	for line in fl:
		# class/crew, adult/child, male/female, survived/died
		line = line.split()
		for i in range(len(line)):
			line[i] = int(line[i])
		x = line[:3]
		y = line[3]
		if y == 0:
			y = -1
		data_points.append(x)
		class_labels.append(y)
	return data_points, class_labels

def classify(data_points, attr, threshhold, ineq):
	predictions = []
	num_items, num_attr = shape(data_points) #items in this case can be number of data_points
	for i in range(num_items):
		predictions.append(1)
	#predictions = matrix(predictions)
	for i in range(num_items):
		pass
		if ineq == 0: # less than
			if data_points[i][:,attr] < threshhold:
				predictions[i] = -1
		if ineq == 1:
			if data_points[i][:,attr] >= threshhold:
				predictions[i] = -1
	# print predictions
	return predictions

#takes in a weight vector D, 
def build_decision_stump(D, data_points, class_labels, error, class_estimate):
	# 	Set the min_error to +infinity
	#error = inf
	num_items, num_attr = shape(data_points)	

	best_stump = {}
	# 	For every feature in the dataset:
	for attr in range(num_attr):
 		# find the min and max for each column/attribute
 		attr_min = data_points[:,attr].min()
 		attr_max = data_points[:,attr].max()

 		attr_range = attr_max - attr_min

 		# 	For every step:
 		for threshhold in range(attr_range+1):
 			# 	For each inequality:			
 			for ineq in range(2):
 				predictions = []

 				# Build a decision stump and test it with the weighted dataset
 				predictions = classify(data_points, attr, threshhold, ineq)
 				errors = [1 for i in range(num_items)]

 				for i in range(num_items):
 					if predictions[i] == class_labels[i]:
 						errors[i] = 0

 				weighted_error = matrix(D).T*matrix(errors).T
				# 	If the error is less than the current minimum error: set this stump as the best stump 				
 				if weighted_error < error:
 					error = weighted_error
 					class_estimate = list(predictions)
 					best_stump["dimension"] = attr
 					best_stump["threshhold"] = threshhold
 					best_stump["inequality"] = ineq

				# 	If the error is less than minError: set this stump as the best stump
	#	 Return the best stump
	return best_stump, error, class_estimate

# http://www.cs.princeton.edu/~schapire/papers/explaining-adaboost.pdf Page 2 saved us
def calc_D(weak_stump, class_labels, class_estimate, D):
	neg_alpha = -1 * weak_stump["alpha"]
	D = matrix(D)

	# exponent = [neg_alpha for i in range(len(class_labels))]
	exponent = exp(multiply(neg_alpha* matrix(class_labels).T, matrix(class_estimate).T))
	new_D = multiply(D, exponent)
	return new_D

def train_decision_stumps(data_points, class_labels, num_iterations):
	num_items, num_attr = shape(data_points)
	best_stump_arr = []

	D = []
	for i in range(num_items):
		D.append([1/float(num_items)])

	total_estimate = [0 for i in range(num_items)]
	total_estimate = matrix(total_estimate)
	# print D_t
	# For each iteration:
	for i in range(num_iterations):
		error = inf
		class_estimate = []

		# 	Find the best stump using build_decision_stump()
		# assume the stump is a dictionary, containing the dimension value, 
		# the threshhold value and then finally add the alpha value
		weak_stump, error, class_estimate = build_decision_stump(D, data_points, class_labels, error, class_estimate)
		# 	Calculate alpha
		error = float(error)
		if error > 0.0:
			alpha = math.log((1-error)/error)/float(2)
		else:
			alpha = 0.0
		weak_stump["alpha"] = alpha

		# 	Add the best stump to the stump array
		best_stump_arr.append(weak_stump)	
		# 	Calculate the new weight vector D
		D = calc_D(weak_stump, class_labels, class_estimate, D)
		# 	Update the aggregate class estimate
		total_estimate = total_estimate + alpha*matrix(class_estimate)
		#*******************
		#total_errors = sum(total_estimate)/float(num_items)

		total_errors = 0
		total_estimate = total_estimate.T
		
		# Add up all the times the sign error (and therefore the likely prediction)
		# Is off, and then divide by the total number of datapoints.
		for k in range(len(class_labels)):
			if sign(class_labels[k]) != sign(total_estimate[k]):
				total_errors += 1
		total_estimate = total_estimate.T

		error_rate = total_errors/float(num_items)

		print "Round ", i + 1
		print "Error rate:", error_rate 

		# If we've reached a perfect predicting set of stumps, quit while you're ahead
		if error_rate == 0.0:
			break
	return best_stump_arr


def main():
	print "Adaboost on Titanic"
	data_points, class_labels = read_in_data_titanic()

	data_points = matrix(data_points)
	
	train_decision_stumps(data_points, class_labels, 10)
	
main()