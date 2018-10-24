#author: Jacob Battipaglia

#This program parses a JSON input file of shapes (convex polygons) and analyzes
#the relationship between each shape. Shapes either intersect, are separate, or surround
#one another (or are inside). This analysis is based off the separating axis theorem, 
#which states that two convex objects do not overlap if there exists a line onto which the
#two objects' projections do not overlap.

import json
import sys
from math import sqrt


def openjson():
	#read json file as command line argument
	if (len(sys.argv) > 1):
		jsonfn = sys.argv[1]
	#if no json file is input as argument, the default.json file is used
	else:
		jsonfn = 'default.json'

	#use json standard library to open/load json files
	data = json.load(open(jsonfn))
	return data

#helper function used to print the data from the json file to make sure it is loaded properly
def printshapes(data):
	i = 0
	shapes = getpts(data)
	print("List of shapes and their points:")
	while (i < len(data['shapes'])):
		print(data['shapes'][i]['id'],": ",shapes[i])
		i = i + 1

#used to get the points of each shape stored in an array.
def getpts(data):
	vertices = []
	i = 0
	while (i < len(data['shapes'])):
		vertices.append(data['shapes'][i]['points'])
		i = i + 1
	return vertices

#calculates the vector from one vertex to the next vertex in the list
def getvector(v1, v2):
	return (v2[0] - v1[0], v2[1] - v1[1])

#calculates the perpendicular/orthogonal vector
def perpendicular(vector):
	return (vector[1], (-1 * vector[0]))

#normalizes the vector to a unit vector
def getunit(vector):
	mag = sqrt(vector[0] ** 2 + vector[1] ** 2)
	return (vector[0] / mag, vector[1] / mag)

#calculates the dot product of two vectors. used to find the projection of a vector onto an axis.
def dotproduct(v1, v2):
	return v1[0] * v2[0] + v1[1] * v2[1]

#calculates projection of vectors onto an axis
def project(pts, axis):
	i = 0
	products = []
	while (i < len(pts)):
		products.append(dotproduct(pts[i], axis))
		i = i + 1
	return [min(products), max(products)]

#determines if the projections of vectors overlap at all.
def overlapping(a, b, axes):
	i = 0
	while (i < len(axes)):
		a_proj = project(a, axes[i])
		b_proj = project(b, axes[i])
		#print(a_proj, b_proj)
		flag = intersection(a_proj, b_proj)
		if flag is False:
			return False
		i = i + 1
	return True

#returns the vectors of the edges of shapes as a list, calculated from the vertices of a shape.
def getedges(pts):
	i = 0
	edges = []
	while (i < len(pts)):
		edges.append(getvector(pts[i], pts[(i+1) % len(pts)]))
		i = i + 1
	return edges

#returns the perpendicular, normalized vectors which represent the axes that the program tests for intersection
def getaxes(a_edges, b_edges):
	edges = a_edges + b_edges
	i = 0
	while (i < len(edges)):
		edges[i] = perpendicular(edges[i])
		i = i + 1
	i = 0
	while (i < len(edges)):
		edges[i] = getunit(edges[i])
		i = i + 1
	return edges

#Determines if the projections of two vectors overlap at all. if they overlap, the two shapes
#are considered to be intersecting. If they do not, a separation axis exists.
def intersection(a, b):
	a_range = [min(a), max(a)]
	b_range = [min(b), max(b)]
	#print(a_range, b_range)
	if (a[0] >= b_range[0]) and (a[0] <= b_range[1]):
		return True
	if (a[1] >= b_range[0]) and (a[1] <= b_range[1]):
		return True
	if (b[0] >= a_range[0]) and (b[0] <= a_range[1]):
		return True
	if (b[1] >= a_range[0]) and (b[1] <= a_range[1]):
		return True
	return False

#if the shapes are determined to be intersection, this function is used to see if one of the shapes
#contains the other. the "containing" shape is returned as output of this function.
def surrounding(a, b):
	a_range = [min(a), max(a)]
	b_range = [min(b), max(b)]
	if (a[0] >= b_range[0]) and (a[0] <= b_range[1]) and (a[1] >= b_range[0]) and (a[1] <= b_range[1]):
		return 'b'
	if (b[0] >= a_range[0]) and (b[0] <= a_range[1]) and (b[1] >= a_range[0]) and (b[1] <= a_range[1]):
		return 'a'
	else:
		return False

#this function is used if shapes are determined to intersect to check if they surround each other.
#the string returned is used an output to the user along with the id's of the shapes.
def contains(a, b, axes):
	i = 0
	container = []
	while (i < len(axes)):
		a_proj = project(a, axes[i])
		b_proj = project(b, axes[i])
		#print(a_proj, b_proj)
		flag = surrounding(a_proj, b_proj)
		#if one projection does not completely surround the other, the shapes merely intersect.
		if flag is False:
			return 'intersects'
		container.append(flag)
		i = i + 1
	container = set(container)
	#print(container)
	if len(container) > 1:
		#there are cases in which one shape always appears to contain another, but does not actually.
		#consider the rectangles
		#	a: [0,1][0,2][3,2][3,1]
		#	b: [1,0][1,3][2,3][2,0]
		#some times a appears to contain b, and vice versa. these shapes are intersecting, not surrounding.
		return 'intersects'
	else:
		outer = container.pop()
		if outer == 'b':
			return 'is inside'
		if outer == 'a':
			return 'surrounds'

#this function initiates the algorithm and returns a string that is used in the output to the user.
def comparetwo(a, b):
	a_edges = getedges(a)
	b_edges = getedges(b)
	#print('ababab' , a_edges, b_edges)
	axes = getaxes(a_edges, b_edges)
	
	if overlapping(a, b, axes) is False:
		return "is separate from"
	#if the shapes are not separate, we must perform more tests for containment.
	else:
		 return contains(a, b, axes)

if __name__ == '__main__':
	data = openjson()
	#reformat data for later usage
	pts = getpts(data)
	i = 0; j = 0

	#compare each shape with each other
	while (i < len(data['shapes'])):
		while (j < len(data['shapes'])):
			if (j == i):
				j = j + 1
			else:
				string = comparetwo(pts[i], pts[j])
				#'<shape name> <is inside | surrounds | intersects> <shape name>'
				print('shape', data['shapes'][i]['id'], string, 'shape', data['shapes'][j]['id'])
				j = j + 1
		j = 0
		i = i + 1