
import sys


def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    listPts = []
    with open('data/'+filename) as f:
        for i, line in enumerate(f):
            if i == N: break
            split_line = line.split()  #Split x and y inline
            listPts.append((float(split_line[0]), float(split_line[1])))
    return listPts


def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]
    """
    extremity_point, k = findExtremity(listPts)
    listPts.append(extremity_point)
    i, v = 0, 0
    chull = []
    while k != len(listPts)-1:
        listPts[i], listPts[k] = listPts[k], listPts[i]  #Swap the points at k and i
        minAngle = 361
        for j in range(i+1, len(listPts)):
            angle = theta(listPts[i], listPts[j])
            if angle < minAngle and angle > v and listPts[j] != listPts[i]:
                minAngle = angle
                k = j
        i += 1
        v = minAngle
        chull.append(listPts[k])

    chull.insert(0, chull.pop())  #Take the last element and place it at the front of the list
    return chull


def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
          Graham-scan algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]
    """
    angle_list = []
    extremity_point, k = findExtremity(listPts)

    #  Sort the list of points by their angle to the horizontal line containing the extremity point
    for i in range(len(listPts)):
        angle = theta(listPts[k], listPts[i])
        angle_list.append((listPts[i], angle))
    sorted_angle_list = sorted(angle_list, key=lambda a:a[1])

    #  Process points using the Grahamscan algorithm
    chull = [extremity_point, sorted_angle_list[0][0], sorted_angle_list[1][0]]
    for i in range(2, len(sorted_angle_list)-1):
        while not isCCW(chull[-2], chull[-1], sorted_angle_list[i][0]):
            chull.pop()
        chull.append(sorted_angle_list[i][0])

    return chull


def monotonechain(listPts):
    """Returns the convex hull vertices computed using
          the monotonechain algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]
    """

    sorted_points = sorted(listPts)  #Basic tuple sort
    lower_section = processChullSection(sorted_points)
    upper_section = processChullSection(reversed(sorted_points))

    chull = list(reversed(upper_section[:-1])) + list(reversed(lower_section[:-1]))  #Concatentate both sections

    return chull


def findExtremity(listPts, func=min, axis='y', tie='right'):
    """Returns a point and it's position in a list of points
          with the specified extremity conditions:
              func --> min or max
              axis --> 'x' or 'y'
              ties --> 'left' or 'right'
              defaults are: min, 'y', 'right'
          return format: ((x, y), k)
    """
    axes, funcs, ties, extremities = ['x', 'y'], [min, max], ['left', 'right'], []  #Declare possible axes, functions, what to do in ties and init an empty extremity list
    if axis in axes and func in funcs:  #Ensure valid function input
        axis_val = axes.index(axis)  #Translate 'x' -> 0 and 'y' -> 1. Useful for indexing lists
        tie_val = ties.index(tie)  #Translate 'left' -> 0 and 'right' -> 1. Useful for indexing lists
        extremity_val = func(listPts, key=lambda t: t[axis_val])  #Use the chosen function on the list of tuples for the given axis
        for k, point in enumerate(listPts):  #Iterate through all points in the list
            if point[axis_val] == extremity_val[axis_val]:  #Check if a point has the same extremity
                extremities.append((point, k))
        extremity_points = sorted(extremities, key=lambda t: t[0][(axis_val+1)//2])  #Sort by the orthogonal axis (x->y, y->x)
    return extremity_points[-tie_val]  #Return the element given what to do when a tie occurs


def theta(pointA, pointB):
    """Computes an approximation of the angle between
          the line AB and a horizontal line through A
          Credit: R. Mukundan, mukundan@canterbury.ac.nz
    """
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        t = dy/(abs(dx) + abs(dy))

    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t

    if t == 0:
        return 360
    else:
        return t*90


def processChullSection(points):
    """Returns the processed section forming half of a
          convex hull as a list of m tuples
          [(u0,v0), (u1,v1), ...]
    """
    section = []
    for p in points:
        while len(section) >= 2 and isCCW(section[-2], section[-1], p):
            section.pop()
        section.append(p)
    return section


def lineF(pointA, pointB, pointC):
    """Returns the side of the point with respect to the line AB
          using the equation:  (Xb-Xa)(Yc-Ya) - (Yb-Ya)(Xc-Xa)
          Credit: R. Mukundan, mukundan@canterbury.ac.nz
    """
    return (
        (pointB[0] - pointA[0]) * (pointC[1] - pointA[1]) -
        (pointB[1] - pointA[1]) * (pointC[0] - pointA[0]) )


def isCCW(pointA, pointB, pointC):
    """Returns a boolean flag if the given points perform a
          counter-clockwise turn
          Credit: R. Mukundan, mukundan@canterbury.ac.nz
    """
    return lineF(pointA, pointB, pointC) > 0


def main():
    #  General cli format --> python convexhull.py <algorithm> <datafile>
    #  Sample cli command --> python convexhull.py giftwrap A_3000.dat
    if len(sys.argv) == 3:  #Called using a cli with arguments, used when running tests
        listPts = readDataPts(sys.argv[2], sys.argv[2][2:-4])
        print(globals()[sys.argv[1]](listPts))  #Call the specified function via globals()["foo"]()
    else:  #Called without arguments
        listPts = readDataPts('B_27000.dat', 27000)  #File name, numPts given as example only
        a = grahamscan(listPts)
        #print (grahamscan(listPts))  #with any code for validating your outputs
        #print (amethod(listPts))


if __name__  ==  "__main__":
    main()
