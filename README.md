# Description:

This program parses a JSON input file of shapes (convex polygons) and nalyzes the relationship between each shape. Shapes either intersect, are eparate, or surround one another (or are inside). This analysis is based off the separating xis theorem,  which states that two convex objects do not overlap if there exists a ine onto which the two objects' projections do not overlap.

# Building/Running the program: 

This program accepts the path to the JSON file the user would like to arse as its first argument. If no JSON file is specfied, it will use the "default.json" file in the same directory. 

To use a specified file ("file.json" in this case):
```
python parser.py file.json
```
To use "default.json" file:
```
python parser.py
```

#

Author: Jacob Battipaglia

