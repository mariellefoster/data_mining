import math

fl = open("data.txt", "r")

#sum values and put them in useful arrays
sum_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
values = [[0]*16] #[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
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

print "Values: " + str(values[3])

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

#put it all back together
outfile = open("standard.txt", "w")
i = 0

while i < 20000:
	line = ""
	line += letters[i]
	k = 0
	while k < 16:
		line += "," + str(values[k][i])
		k+=1
	line += " \n "
	outfile.write(line)
	i+=1






