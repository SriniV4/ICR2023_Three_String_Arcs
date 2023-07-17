from design import Design
from design import getPercent
from design import makeThreeStringDesign as mTSD
from design import cheb_roots
import random
domain = [0,500]
angleBounds = [30,75]
COMBounds = [0,1]
lengthBounds = [1,100]
densityBounds = [.001,1]
percentage = 10
delta = []
def updateDesign(newParams, bitmask):
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
def read():
	file = open("best.txt", "r")
	#File Format: Design in format [Theta , Gamma , 
for i in range(1):
	for i in range(1<<numParams):
		newParams = [allParams[j] for j in range(numParams)]
	with open("best.txt", "w") as f:
		print(bestDesign.toString(), file=f)
		print(bestPercentage, file=f)
		print(*sorted(cheb_roots(bestDesign.getFunction() , domain)), file=f)
