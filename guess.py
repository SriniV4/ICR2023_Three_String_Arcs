# This files runs simultaneous perturbation stochastic approximation to try and find the best design. Either you can read from the file to start from a design, or randomly generate a design to start from. (WIP)

import numpy
from design import Design
from design import getPercent
from design import makeThreeStringDesign as mTSD
from design import cheb_roots
import random
angleBounds = [30*numpy.pi/180,75*numpy.pi/180]
COMBounds = [0,1]
lengthBounds = [1,100]
densityBounds = [.001,1]
percentage = 10
delta = []
roots = []
bestDesign = None
bestPercentage = None
parameters = []
temporaryParameter = []
numParams = 0
def getNewDesign(bitmask):#Perturbation
	newParams = [i for i in parameters]
	#print("original:" , end=' ')
	#print(parameters)
	# For each bit, apply delta
	for j in range(numParams):
		if(bitmask & (1<<j)):
			newParams[j] = newParams[j]+delta[j]
		else:
			newParams[j]-=delta[j]
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

	#print("new:" , end=' ')
	#print(newParams)
	#print()
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
	return [1e-6,rightBound]
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
	domain[1]*=10
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

def SPSA(iterations):
	#read() #uncomment if you want to read design from file
	global bestPercentage
	global bestDesign
	global parameters
	global roots
	global temporaryParameter
	generateRandomDesign()
	print(bestPercentage)
	print("start roots:" , end=' ')
	print(roots)
	for i in range(iterations):
		delta = makeDelta()
		tempRoots = roots
		for mask in range(1 << numParams):
			newDesign , newParams = getNewDesign(mask)
			rroots , newPercentage = getPercent(newDesign , getDomain(newDesign))  
			print("roots:" , end=' ')
			print(rroots)
			print("design:" , end=' ')
			print(newParams)
			if(newPercentage < bestPercentage):
				print(tempRoots)
				bestPercentage = newPercentage
				bestDesign = newDesign
				temporaryParameter = newParams
				tempRoots = rroots
		if(len(temporaryParameter)):
			parameters = temporaryParameter
		roots = tempRoots
		print()
		print()
		print("best roots:" , end=' ')
		print(roots)
		print(roots/roots[0])
		print(bestPercentage)
		print()
SPSA(1)
