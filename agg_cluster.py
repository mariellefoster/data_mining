import math
import heapq


def read_in_data():
	fl = open("portfoliodata.txt", "r")
	data = []
	for line in fl:
		line = line.split()	
		adjust_data(line)
		for i in range(len(line)):
			if line[i] != 'inf':
				line[i] = float(line[i])
		data.append(line)
	return data

def adjust_data(line):
	for i in range(3,7):
		if line[i] != 'inf':
			line[i] = float(line[i])
		if i == 3:
			if not(line[3] == 9999.99 or line[3] < 1):
				line.insert(3, 'inf')
			if line[3] > 9000:
				line[3] = 'inf'
		if i == 4:
			if not (line[i] <= 800 and line[i] >= 200):
				line.insert(4, 'inf')
				line.insert(5, 'inf')
		if i == 6:
			if not (line[i] <= 36 and line[i] >= 15):
				line.insert(6, 'inf')

#To measure the distance between two clusters, use the Euclidean-squared 
#distance between the centroids of those clusters (i.e., the mean). Handle 
#a single point as a cluster of one point. 
def set_up_heap(clusters, hq):
	for i in range(len(clusters)):
		for k in range(i+1, len(clusters)):
			dist = euclidean_squared(clusters[i][0], clusters[k][0])
			lst = [dist, clusters[i], clusters[k]]
			heapq.heappush(hq, lst)


def euclidean_squared(X, Y):
	dist = 0
	for i in range(len(X)):
		dist += (X[i] - Y[i])**2
	return dist

def get_centroid(points):
	centroid = []
	for i in range(15):
		SUM = 0
		for k in range(len(points)):
			SUM += points[k][i]
		centroid.append(SUM/len(points))
	return centroid
	
def update_heap(new_cluster, clusters, hq):
	for i in range(len(clusters)):
		dist = euclidean_squared(clusters[i][0], new_cluster[0])
		# lst = [dist, clusters[i], new_cluster]
		heapq.heappush(hq, [dist, clusters[i], new_cluster])

def merge_clusters(cluster1, cluster2, removed_clusters):
	
	points = cluster1[1] + cluster2[1]
	centroid = get_centroid(points)
	SSE = SSE_calc(points, centroid)

	new_cluster = [centroid, points, SSE, cluster1[3] + cluster2[3]]
	removed_clusters.append(cluster1[3] + cluster2[3])
	return new_cluster

def SSE_calc(points, centroid):
	SSE = 0
	for point in points:
		SSE += euclidean_squared(point, centroid)
	return SSE

def standardize(data, averages, std_devs):
	for i in range(15):
		SUM = 0
		num_in_category = 0
		for k in range(len(data)):
			if data[k][i] != 'inf':
				num_in_category += 1
				SUM += data[k][i]
		AVG = SUM/num_in_category
		averages.append(AVG)
	
	for i in range(15):
		STD = 0
		num_in_category = 0
		for k in range(len(data)):
			if data[k][i] != 'inf':
				STD += (data[k][i] - averages[i])**2
				num_in_category += 1
		STD = math.sqrt(STD/float(num_in_category))
		std_devs.append(STD)

	for i in range(15):
		for k in range(len(data)):
			if data[k][i] != 'inf':
				data[k][i] = (data[k][i] - averages[i])/std_devs[i]
			else:
				data[k][i] = 0

# reverse the standardization process
def unstandardize(clusters, averages, std_devs):
	results = []
	for i in range(len(clusters)):
		final_cluster = []
		for j in range(15):
			final_cluster.append((clusters[i][0][j]*std_devs[j])+averages[j])
		results.append(final_cluster)
	return results

def main():
	
	#read in data
	data = read_in_data()
	#standardize data
	averages = []
	std_devs = []
	standardize(data, averages, std_devs)

	#instantiate cluster 
	clusters = []
	i = 0

	for point in data:
		# this is the centroid, the list of points in the cluster, the SSE, and the index of the point in data
		clusters.append([point, [point], 0, [i]])
		i += 1

	hq = []
	removed_clusters = []
	# calculate distance between everything 

	#GRADER: We are using the fancy Heap method
	set_up_heap(clusters, hq)


	while len(clusters) > 1:
	# for m in range(4):
		found = False
		while not found:
			found = True
			if hq:
				cluster_pair = heapq.heappop(hq)
				points1 = set(cluster_pair[1][3])
				points2 = set(cluster_pair[2][3])
				for rmvd_pts in removed_clusters:
					if points1.issubset(set(rmvd_pts)) and points1 != set(rmvd_pts):
						found = False
						break
					if points2.issubset(set(rmvd_pts)) and points2 != set(rmvd_pts):
						found = False
						break
			else:
				exit()

		new_cluster = merge_clusters(cluster_pair[2], cluster_pair[1], removed_clusters)
		
		i = 0
		
 		while i < len(clusters):
 			if len(clusters) >= 1:
				for ID in new_cluster[3]:
					if i >= 0:
						if ID in clusters[i][3]:
							clusters.remove(clusters[i])
							i -= 1	
			else:
				i = len(clusters)
			i += 1			
		
		update_heap(new_cluster, clusters, hq)

		clusters.append(new_cluster)

		print  "Cluster Length: ", len(clusters)

		SSE = 0
		for cluster in clusters:
			SSE += cluster[2]

		if len(clusters) < 21:
			# print len(clusters)
			centaurs = unstandardize(clusters, averages, std_devs)
			for horse in centaurs:
				
				print horse
			print SSE
			print 
			print	

main()