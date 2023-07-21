# Design class with a few methods to find roots,percentage accuracy,etc.
import pychebfun
import math
import numpy
from matplotlib import pyplot as plt

class Design:
	def __init__(self , numStrings,angles , tensions , densities , lengths , centerMass):
		self.tensions = tensions
		self.numStrings = numStrings
		self.densities = densities
		self.lengths = lengths
		self.centerMass = centerMass
		self.angles = angles
	def getFunction(self):
		def s(wavelength):
			def f(wavelength):
				totalSum = 0
				for j in range(self.numStrings):
					addend = numpy.sqrt(self.tensions[j] * self.densities[j])
					addend *= numpy.cos(self.lengths[j] * numpy.sqrt(self.densities[j]) * wavelength/numpy.sqrt(self.tensions[j]))
					for k in range(self.numStrings):
						if(j==k):
							continue
						addend*=numpy.sin(self.lengths[k] * wavelength * numpy.sqrt(self.densities[k]) / numpy.sqrt(self.tensions[k]))
					totalSum+=addend
				return totalSum
			def g(wavelength):
				totalSum = 1
				for j in range(self.numStrings):
					totalSum *= numpy.sin(self.lengths[j] * wavelength * numpy.sqrt(self.densities[j]) / numpy.sqrt(self.tensions[j]))
				return totalSum
			return f(wavelength) + self.centerMass * wavelength * g(wavelength)
		return s
	def toString(self):
		return *self.angles , *self.densities , *self.lengths , self.centerMass
def cheb_roots(function, domain):  
    f_se_cheb = pychebfun.Chebfun.from_function(function, domain=domain)

    return f_se_cheb.roots()
def percentage(roots):
	totalError = 0
	numRoots = 5
	if(len(roots)<numRoots):
		return numpy.inf
	for i in range(1 , numRoots*2 , 2):
		diff = abs(i - roots[i//2]/roots[0])
		totalError += (diff/i)
	return totalError/numRoots
def getPercent(design , domain):
	s = design.getFunction()
	roots = cheb_roots(s, domain)
	roots.sort()
	return roots , percentage(roots)
def makeThreeStringDesign(allParams):
	theta , gamma = allParams[0:2] # Angle 1 is Theta , Angle 2 is Gamma
	densities = allParams[2:5]
	lengths = allParams[5:8]
	centerMass = allParams[-1]
	t3 = 1
	t2 = 1/(numpy.cos(theta)*(1 + (numpy.sin(theta)*numpy.cos(gamma)/(numpy.sin(gamma)*numpy.cos(theta)))))
	t1 = 1/(numpy.cos(gamma)*(1 + (numpy.sin(gamma)*numpy.cos(theta)/(numpy.sin(theta)*numpy.cos(gamma)))))
	return Design(3 , [theta , gamma] , [t1,t2,t3] , densities , lengths , centerMass) 	
def test():
	lengths = [5,10,1]
	densities = [0.001, 0.0015, 0.001]
	tensions = [180, 185, 180]
	centerMass = 0
	"""
	lengths = [7.729248288664657, 7.892457169530038, 1]
	densities = [0.2777940075904079, 0.22263848609368753, 0.8297746591606884]
	tensions = [7.24497034634028, 6.57358320536199, 23.23799760493053]
	centerMass = 0.8494808959423903
		lengths = [5,10,1]
		densities = [0.001, 0.0015, 0.001]
		tensions = [180, 185, 180]
		centerMass = 0
	"""
	numStrings = 3
	testDesign = Design(numStrings , [0,0] , tensions , densities , lengths, centerMass)
	s = testDesign.getFunction()
	domain = [0,500]
	roots = cheb_roots(s , domain)
	roots.sort()
	print(*roots)
	# Generate x and y values for the plot
	x = numpy.linspace(1, 501, 1000)
	y = [s(i) for i in x]

	# Plot the function
	plt.plot(x, y, color='red')

	# Plot the roots as larger purple dots
	for i in roots:
		plt.plot(i, 0, 'o', markersize=2, color='purple')

	# Display the plot
	plt.show()												
	
def main():
	a = [1,2,3,4,5]
	print(percentage(a) , percentage([1,3,5,7,9]))
if __name__ == "__main__":
    main()

