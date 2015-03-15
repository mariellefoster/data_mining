#Adaboost
#By Marielle Foster and Nick Petru

def read_in_data():
	fl = open("titanic.dat")

	passengers = []

	for line in fl:
		# class/crew, adult/child, male/female, survived/died
		line = line.split()
		for i in range(len(line)):
			line[i] = int(line[i])
		x = line[:3]
		y = line[3]
		passengers.append([x, y])
	return passengers





def main():
	passengers = read_in_data()



main()