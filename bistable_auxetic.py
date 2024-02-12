

#%%
from build123d import *
from ocp_vscode import *
import math

edge_length=25
t=3
theta=15
thickness=2
hinge_length=1
gap=.5
rows = 3
columns=5



# Projects point along vector defined by angle & distance.
def proj(coord, alpha, k):
    return (coord[0] + k * math.cos(math.radians(alpha)), coord[1] + k * math.sin(math.radians(alpha)))

# Define intersection between two vectors defined by angle & distance.
def inters(p1, p2, angle1, angle2):
    x = -(p1[1] - p2[1] - p1[0] * math.tan(math.radians(angle1)) + p2[0] * math.tan(math.radians(angle2))) / (math.tan(math.radians(angle1)) - math.tan(math.radians(angle2)))
    return (x, p1[1] + (x - p1[0]) * math.tan(math.radians(angle1)))

# Distance between two points.
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)



# Function to generate a triangle shape
def create_triangle(edge_length, t, theta, hinge_length, gap):
    t1 = (0, 0)
    t2 = (edge_length, 0)
    t3 = proj(t1, 60, edge_length)
    plength = distance(proj(t1, 60, t+gap), inters(proj(t1, 60, t+gap), [edge_length-t-gap, 0], theta, theta+120)) - hinge_length
    r1 = proj(t1, 60, t),
    r2 = proj(t1, 60, t+gap),
    r3 = proj(proj(t1, 60, t+gap), theta, plength),
    r4 = proj(proj(t1, 60, t), theta, plength),
    triangle = Polygon(t1, t2, t3, align=(Align.MIN, Align.MIN))
    rectangle = Polygon(r1, r2, r3, r4, align=(Align.MIN, Align.MIN))
    proj1 = proj(t1, 60, t)
    proj2 = proj(t1, 0, edge_length-t-gap)
    proj3 = proj(proj(t1, 60, edge_length), -60,t)
    g1 = Pos(proj1[0], proj1[1])*rectangle
    g2 = Pos(proj2[0], proj2[1])*Rot(Z=120)*rectangle
    g3 = Pos(proj3[0], proj3[1])*Rot(Z=-120)*rectangle
    return triangle - g1 - g2 - g3


# Function to generate a hexagon shape
def create_hexagon(edge_length, t, theta, hinge_length, gap):
    h = []
    i = 0
    for a in range(0, 360, 60):
        if i % 2 !=  0:
            h+= Rot(Y=180)*Rot(Z=a)*create_triangle(edge_length, t, theta, hinge_length, gap)
        else:
            h+= Rot(Z=a)*create_triangle(edge_length, t, theta, hinge_length, gap)
        i+=1
    return Compound(label="hex", children=h)

hex = create_hexagon(edge_length, t, theta, hinge_length, gap)
hex2 = Pos(Y=math.sqrt(3)*edge_length)*create_hexagon(edge_length, t, theta, hinge_length, gap)
show(hex, hex2)


a = edge_length*math.sin(math.radians(60))*2
b = edge_length*1.5
c = a


def bistable_auxetic(edge_length, t, theta, hinge_length, gap, rows, columns):
    ba = []
    vertical_dist = edge_length*math.sin(math.radians(60))*2
    for i in range(0, rows-1):
        for j in range (0,columns-1):
            ba += Pos(edge_length*j*1.5, vertical_dist*(i+(j%2)*.5), 0)*hexagon(edge_length, t, theta, hinge_length, gap)
            show(ba)
            break
    return ba

show(bistable_auxetic(edge_length, t, theta, hinge_length, gap, rows, columns))


   

# %%
