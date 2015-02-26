# kmeans.py
# Marielle Foster and Nick Petru

import math
import random
from itertools import izip
import copy

# format the data store only the user attributes
def read_in_data():
	fl = open("wp_namespace.txt", "r")
	data = []
	for line in fl:
		line = line.split()
		line = line[len(line)-4:]
		for i in range(4):
			line[i] = int(line[i])
		data.append(line)
	return data

# log all data and store the max and min for each of the four categories
def log_transform(data, attr_range):
	for user in data:
		i =0
		for attribute in range(len(user)):
			# log transform
			user[attribute] = float(math.log(user[attribute]+1, 2))
			if (user[attribute] < attr_range[i][0]):
				attr_range[i][0] = user[attribute]
			if (user[attribute] > attr_range[i][1]):
				attr_range[i][1] = user[attribute]
			i += 1
	return data

# TODO: return data to original scale
def log_reverse(data_point):
	for i in range(len(data_point)):
		#print 2**data_point[i]
		data_point[i] = (2**data_point[i])-1
	return data_point
	

# randomly set k centers
def simple_center(k, centers, attr_range):
	#random.seed(1)
	for center in centers:
		for i in range(4):
			cent = random.random()
			cent = cent*(attr_range[i][1] - attr_range[i][0]) + attr_range[i][0]
			center[0].append(cent)

# fancily set k centers
def complex_center(centers, data,k):
	#random.seed(11)
	# pick one random point
	num = random.randint(0, len(data)-1)
	centers.append([data[num], [],0])
	
	# iteratively pick other k-1 points that are furthest from those
	while k > 1:
		furthest_point = [0,0,0,0]
		furthest_point_dst = 0
		for point in data:
			pt_dists = []
			for center in centers:
				pt_dists.append(euclidean_squared(point, center[0]))
			
			# determine farthest point from existing centers	
			min_pt_dists = min(pt_dists)
			if min_pt_dists > furthest_point_dst:
				furthest_point = point
				furthest_point_dst = min_pt_dists
		
		centers.append([furthest_point, [], 0])
		k -= 1
	return

# cluster the data (populate the k center[1]s)
def cluster(centers, data,k):
	furthest_points = []
	for user in data:
		user_error = []
		for i in range(k):
			user_error.append(euclidean_squared(user, centers[i][0]))
		MIN = min(user_error)
		c = user_error.index(MIN)
		
		# calculate the error and determine cluster and set center
		centers[c][2] += MIN
		centers[c][1].append(user)
		furthest_points.append([MIN, user])
	furthest_points = sorted(furthest_points)
	
	# return furthest points to easily reset the center's coordinates
	# in case the cluster is empty
	furthest_points = furthest_points[len(furthest_points)-k:]
	return furthest_points[::-1]

# eucliden squared metric
def euclidean_squared(X, Y):
	dist = 0
	for i in range(len(X)):
		dist += (X[i] - Y[i])**2
	return dist

# find the average distance between the center and the cluster and shift
# the center accordingly
def reset_centers(centers):
	for center in centers:
		average = [0,0,0,0]
		for point in center[1]:
			average = map(sum, izip(point, average))
		for x in range(len(average)):
			average[x] = average[x]/float(len(center[1]))

		# reset the center
		center[0] = average
		center[1] = []
		center[2] = 0

# if any centers have an empty cluster use furthest_points to reset center
def empty_clusters(centers, furthest_points, data, k):
	has_empty = True
	while has_empty:
		has_empty = False
		i = 0
		for center in centers:
			if not center[1]:
				has_empty = True
				center[0] = furthest_points[i][1]
				i += 1
		furthest_points = cluster(centers, data, k)

#unlog the data and subsequent error
def unlogged_error(centers):
	for center in centers:
		error = 0
		center_reversed = log_reverse(center[0])
		for i in range(len(center[1])):			
			error += euclidean_squared(log_reverse(center[1][i]), center_reversed)
			#print prev_point, prev_center
		center[2] = error

def main():

	#read in data
	data = read_in_data()

	#log transform the data with log_2(1+x)
	


	# You'll need to initialize the cluster centers. 
	# Do something appropriate. Implement choosing k random 
	# points, and something fancier. Allow the user to 
	# choose which technique to use when starting the program.

	k = int(raw_input("How many clusters do you want? "))
	center_type = raw_input("Do you want simple or complex center initialization (type s or c)? ")
	
	#for k in range(20):
	attr_range = [[1000,0] for i in range(4)] 
	log_transform(data, attr_range)

	# each center stores list of coordinates (i.e. attr) and list of points in its cluster
	# k centers, each with a list of 4 coordinates, a list of points in its cluster and it's SSE
	
	if center_type == "s":	

		centers = [[[],[], 0] for i in range(k)]
		simple_center(k, centers, attr_range)
	elif center_type == "c":
		centers = []
		complex_center(centers, data,k)
	else:
		print "Not the right letter to enter..."
		exit()

	#cluster the data
	furthest_points = cluster(centers, data,k)

	SSE_prev = 1
	SSE = 0
	# run until the error converges
	while SSE_prev != SSE:

		SSE_prev = SSE
		empty_clusters(centers, furthest_points, data, k)
		SSE = 0
		for center in centers:
			SSE += center[2]
		print "SSE before reset: ", SSE
		
		reset_centers(centers)
		cluster(centers, data, k)
		SSE = 0
		for center in centers:
			SSE += center[2]
		print "SSE after reset: ", SSE

		
		# SSE = 0
	unlogged_error(centers)
	SSE = 0
	for center in centers:
		SSE += center[2]
	
		# print k+1, "Centers"
	# for center in centers:
	# 		print center[0]
	# 		SSE += center[2]
	print "For k = ", k, " we have a Final Unlogged SSE = ", SSE
		#print SSE

main()