import math
import random
import numpy as np
import sys
from design import Design
from design import cheb_roots as cr
import matplotlib.pyplot as plt
angleBounds = [30*np.pi/180,75*np.pi/180]
COMBounds = [0,1]
lengthBounds = [1,100]
densityBounds = [.001,1]

def makeDesign(angles , densities , lengths , COM):
	theta , gamma = angles
	T3 = 1 #arbitrary value ( scaling laws )
	T2 = T3/(np.cos(theta) * (1 + (np.sin(theta) * np.cos(gamma))/(np.sin(gamma)*np.cos(theta))))
	T1 = T2 * (np.sin(theta) / np.sin(gamma))
	return Design(3 , [theta , gamma] , [T1 , T2 , T3] , densities , lengths , COM)

def generateRandom():
	theta , gamma = [random.uniform(angleBounds[0] , angleBounds[1]) for i in range(2)]
	d1 , d2 , d3= [random.uniform(densityBounds[0] , densityBounds[1]) for i in range(3)]
	l1 , l2 , l3 = [random.uniform(angleBounds[0] , angleBounds[1]) for i in range(3)]
	COM = random.uniform(COMBounds[0] , COMBounds[1])
	return makeDesign([theta , gamma] , [d1 , d2 ,d3] , [l1 , l2 , l3] , COM)

def getDomain(design):
	rightBound = np.inf
	for i in range(3):
		rightBound = min(rightBound , np.pi/(design.lengths[i]*np.sqrt(design.densities[i]/design.tensions[i])))
	return [1e-6,10*rightBound]

def getSpectrumPercentage(spectrum):
	if(len(spectrum)<5):
		return np.inf
	totalPercentage = 0
	for i in range(5):
		expected = i*2+1
		got = spectrum[i]
		totalPercentage += abs((got - expected)/expected)
	return totalPercentage/5

def makeDelta(percentage):
	theta , gamma = [random.uniform(0,percentage/100) * (angleBounds[1] - angleBounds[0]) for i in range(2)]
	d1 , d2 , d3 =  [random.uniform(0,percentage/100) * (densityBounds[1] - densityBounds[0]) for i in range(3)]
	l1 , l2 , l3 =  [random.uniform(0,percentage/100) * (lengthBounds[1] - lengthBounds[0]) for i in range(3)]
	COM =  random.uniform(0,percentage/100) * (COMBounds[1] - COMBounds[0])
	return [theta , gamma , d1 , d2 , d3 , l1 , l2 , l3 , COM]

def applyDelta(delta , mask , bestDesign):
	startingParameters = bestDesign.getParameters()
	for i in range(len(delta)):
		startingParameters[i] = startingParameters[i] + (delta[i] if (mask & (1<<i)) else -(delta[i]))
	for i in range(0,2):
		startingParameters[i] = max(startingParameters[i] , angleBounds[0])
		startingParameters[i] = min(startingParameters[i] , angleBounds[1])
	for i in range(2,5):
		startingParameters[i] = max(startingParameters[i] , densityBounds[0])
		startingParameters[i] = min(startingParameters[i] , densityBounds[1])
	for i in range(5,8):
		startingParameters[i] = max(startingParameters[i] , lengthBounds[0])
		startingParameters[i] = min(startingParameters[i] , lengthBounds[1])
	for i in range(8,9):
		startingParameters[i] = max(startingParameters[i] , COMBounds[0])
		startingParameters[i] = min(startingParameters[i] , COMBounds[1])
	return startingParameters

def graphSpectrum(spectrum):
	colors = ['red' , 'blue' , 'yellow' , 'green', 'black']
	for i in range(5):
		plt.axhline(y = i*2+1, color = colors[i], linestyle = '-')
		plt.scatter([j for j in range(len(spectrum))] , spectrum[:,i] , color = colors[i])
	plt.gca().set_xlabel("Iterations")
	plt.gca().set_ylabel("Spectrum")
	plt.show()
def linearFunction(percent):
	return percent*100 if percent*100<=100 else 100
def SPSA(iterations):
	bestDesign = generateRandom()
	bestRoots = cr(bestDesign.getFunction() , getDomain(bestDesign)) 
	bestRoots.sort()
	bestSpectrum = bestRoots/bestRoots[0]
	bestPercentage = getSpectrumPercentage(bestSpectrum)
	lastParameters = bestDesign.getParameters()
	count = 0
	threshold = 5000
	spectrumGraph = np.zeros((iterations+1 , 5))
	spectrumGraph[0] = bestSpectrum[0:5]
	# [Theta , Gamma , L1 , L2 , L3 , D1 , D2 , D3 , COM]
	for i in range(iterations):
		print("Iteration: " , i)
		print("Best Parameters: " , bestDesign.getParameters())
		print("Best Spectrum: " , bestSpectrum)
		print("Best Percentage:" , bestPercentage)
		print(count)
		print()
		delta = makeDelta(linearFunction(bestPercentage))
		#delta = makeDelta(quadraticFunction(bestPercentage)) # Uncomment this for quadratic percentage
		temporaryDesign = bestDesign
		temporarySpectrum = bestSpectrum
		temporaryPercentage = bestPercentage
		temporaryRoots = bestRoots
		# 101010100
		for mask in range(1 << len(delta)):
			newParameters = applyDelta(delta , mask , bestDesign)
			#print("New parameters: " , newParameters)
			newDesign = makeDesign([newParameters[i] for i in range(0,2)] , [newParameters[i] for i in range(2,5)] , [newParameters[i] for i in range(5,8)] , newParameters[8])
			# [.01 , .01  , .023 ,.0123 , 2 , 3]
			newRoots = cr(newDesign.getFunction() , getDomain(newDesign))
			newRoots.sort()
			#print("New Roots: " , newRoots)
			newSpectrum = newRoots/newRoots[0]
			#print("New Spectrum: " , newSpectrum)
			newPercentage = getSpectrumPercentage(newSpectrum)
			#print("New Percentage: " , newPercentage)
			#print()
			if(newPercentage < temporaryPercentage):
				temporaryDesign = newDesign
				temporarySpectrum = newSpectrum
				temporaryPercentage = newPercentage
				temporaryRoots = newRoots
		bestDesign = temporaryDesign
		bestSpectrum = temporarySpectrum
		bestRoots = temporaryRoots
		bestPercentage = temporaryPercentage
		with open('best.txt', 'w') as f:
		    f.write("\n\n")
		    f.write(" ".join([str(i) for i in bestDesign.getParameters()]))
		    f.write("\n")
		    f.write("\n")
		    f.write(" ".join([str(i) for i in bestRoots]))
		    f.write("\n")
		    f.write("\n")
		    f.write(" ".join([str(i) for i in bestSpectrum]))
		    f.write("\n")
		    f.write("\n")
		    f.write(str(bestPercentage))
		    f.write("\n")
		    f.write("\n")
		if(lastParameters==bestDesign.getParameters()):
			count+=1
		else:
			count = 0
		lastParameters = bestDesign.getParameters()
		spectrumGraph[i+1] = bestSpectrum[0:5]
		if(count==threshold):
			with open("all.txt" , "a") as file1:
				file1.write("\n\n")
				L = " ".join([str(i) for i in bestDesign.getParameters()])	
				file1.write(L)
				file1.write("\n\n")
				L = 	" ".join([str(i) for i in bestSpectrum])
				file1.write(L)
				file1.write("\n\n\n")
			bestDesign = generateRandom()
			bestRoots = cr(bestDesign.getFunction() , getDomain(bestDesign)) 
			bestRoots.sort()
			bestSpectrum = bestRoots/bestRoots[0]
			bestPercentage = getSpectrumPercentage(bestSpectrum)
			lastParameters = bestDesign.getParameters()
			count = 0
	print(bestSpectrum)
	graphSpectrum(spectrumGraph)
if(len(sys.argv)<=1):
	SPSA(int(input("Iterations? ")))
else:
	SPSA(int(sys.argv[1]))
