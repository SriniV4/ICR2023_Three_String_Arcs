# This files runs simultaneous perturbation stochastic approximation to try and find the best design. Either you can read from the file to start from a design, or randomly generate a design to start from. (WIP)

import numpy
from design import Design
from design import getPercent
from design import makeThreeStringDesign as mTSD
from design import cheb_roots
import random
import matplotlib.pyplot as plt
angleBounds = [30*numpy.pi/180,75*numpy.pi/180]
COMBounds = [0,1]
lengthBounds = [1,100]
densityBounds = [.001,1]
percentage = 1
delta = []
roots = []
bestDesign = None
bestPercentage = None
parameters = []
temporaryParameter = []
iterations = 5000000
spectrum = numpy.zeros((iterations , 5))
numParams = 0
def getNewDesign(bitmask):#Perturbation
	newParams = [i for i in parameters]
	# For each bit, apply delta
	for j in range(numParams):
		if(bitmask & (1<<j)):
			newParams[j] = newParams[j]+delta[j]
		else:
			newParams[j] = newParams[j] - delta[j]
	for i in range(0,2):
		newParams[i] = min(newParams[i] , angleBounds[1])
		newParams[i] = max(newParams[i] , angleBounds[0])
	for i in range(2,5):
		newParams[i] = min(newParams[i] , densityBounds[1])
		newParams[i] = max(newParams[i] , densityBounds[0])
	for i in range(5,8):
		newParams[i] = min(newParams[i] , lengthBounds[1])
		newParams[i] = max(newParams[i] , lengthBounds[0])
	for i in range(8,9):
		newParams[i] = min(newParams[i] , COMBounds[1])
		newParams[i] = max(newParams[i] , COMBounds[0])
	return mTSD(newParams) , newParams

def makeDelta():
	delta.clear()
	for i in range(2):
		r = random.uniform(0,percentage/100)
		r*=angleBounds[1]-angleBounds[0]
		delta.append(r)
	for i in range(3):
		r = random.uniform(0,percentage/100)
		r*=densityBounds[1]-densityBounds[0]
		delta.append(r)	
	for i in range(3):
		r = random.uniform(0,percentage/100)
		r*=lengthBounds[1]-lengthBounds[0]
		delta.append(r)	
	for i in range(1):
		r = random.uniform(0,percentage/100)
		r*=COMBounds[1]-COMBounds[0]
		delta.append(r)	

def getDomain(someDesign):
	rightBound = numpy.inf
	for i in range(3):
		rightBound = min(rightBound , numpy.pi/(someDesign.lengths[i]*numpy.sqrt(someDesign.densities[i]/someDesign.tensions[i])))
	return [1e-6,10*rightBound]

def generateRandomDesign():
	designParameters = []
	for i in range(2):
		designParameters.append(random.uniform(angleBounds[0] ,angleBounds[1]))
	for i in range(3):
		designParameters.append(random.uniform(densityBounds[0] ,densityBounds[1]))
	for i in range(3):
		designParameters.append(random.uniform(lengthBounds[0] ,lengthBounds[1]))
	designParameters.append(random.uniform(COMBounds[0] , COMBounds[1]))
	global parameters 
	global roots
	global bestPercentage 
	global bestDesign 
	global numParams 
	parameters = designParameters
	bestDesign = mTSD(designParameters)
	domain = getDomain(bestDesign)
	roots , bestPercentage = getPercent(bestDesign ,domain)
	numParams = len(designParameters)

def read():
	file = open("best.txt", "r")
	#File Format: Design in format [Theta , Gamma , D1 , D2 , D3, L1 , L2 , L3 , COM]
	parameters = [float(i) for i in file.read().split(",")]
	bestDesign = mTSD(parameters)
	bestPercentage = float(f.read())
	numParams = len(parameters)

def write(roots):
	with open("best.txt", "w") as f:
		print(bestDesign.toString(), file=f)
		print(bestPercentage, file=f)
		print(*roots, file=f)

def graph(spectrum):
	colors = ['red' , 'blue' , 'yellow' , 'green', 'black']
	for i in range(5):
		plt.axhline(y = i*2+1, color = colors[i], linestyle = '-')
		plt.scatter([j for j in range(len(spectrum))] , spectrum[:,i] , color = colors[i])
	plt.show()

def SPSA(iterations):
	#read() #uncomment if you want to read design from file
	global bestPercentage
	global bestDesign
	global parameters
	global roots
	global temporaryParameter
	generateRandomDesign()
	for i in range(iterations):
		delta = makeDelta()
		mask1 = 0
		mask2 = (1<<numParams)-1
		design1 , param1 = getNewDesign(mask1)
		design2 , param2 = getNewDesign(mask2)
		print("Iteration " , end = str(i))
		print()
		roots1 , percentage1 = getPercent(design1 , getDomain(design1))
		roots2 , percentage2 = getPercent(design2 , getDomain(design2))
		print("Roots Of Down Perturbation: ",roots1)
		print("Percntage Of Down Perturbation: ",percentage1)
		print("Parameters Of Down Perturbation: ",param1)
		print("\n")
		print("Roots Of Up Perturbation: ",roots2)
		print("Percentage Of Up Perturbation: ",percentage2)
		print("Parameters Of Up Perturbation: ",param2)
		print("\n")
		print("\n")
		if(percentage1 > percentage2):
			if(percentage2 < bestPercentage):
				bestDesign = design2
				roots = roots2
				bestPercentage = percentage2
				parameters = param1
		else:
			if(percentage1 < bestPercentage):
				bestDesign = design1
				roots = roots1
				bestPercentage = percentage1
				parameters = param2
		spectrum[i] = roots[0:5]/roots[0]
		print("Best Spectrum: " , spectrum[i])
		print("Best Percentage: " , bestPercentage)
		print()
	graph(spectrum)

SPSA(iterations)
