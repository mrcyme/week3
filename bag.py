# %%
from build123d import *
from ocp_vscode import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.optimize import minimize

def optimize_spline_length(control_points, target_length, plot=False):
    # Sort control points by x in ascending order
    x = control_points[:, 0]
    y = control_points[:, 1]
    sorted_indices = np.argsort(x)
    sorted_x = x[sorted_indices]
    sorted_y = y[sorted_indices]

    # Define bounds for the optimization variables (y coordinates), ensuring y > 0
    bounds = [(0.1, None) for _ in sorted_y[1:-1]]

    # Objective function: Computes the difference between the current spline length and the target length
    def objective(variable_y):
        y_coordinates = np.hstack(([sorted_y[0]], variable_y, [sorted_y[-1]]))
        cs_opt = CubicSpline(sorted_x, y_coordinates)
        def derivative_opt(t):
            dx_dt = cs_opt(t, 1)
            dy_dt = cs_opt(t, 1, True)
            return np.sqrt(dx_dt**2 + dy_dt**2)
        length_opt = quad(derivative_opt, sorted_x.min(), sorted_x.max())[0]
        return abs(length_opt - target_length)

    # Optimize the y coordinates with bounds (excluding the first and last points)
    result = minimize(objective, sorted_y[1:-1], method='L-BFGS-B', bounds=bounds)
    optimized_y = np.hstack(([sorted_y[0]], result.x, [sorted_y[-1]]))

    # Compute the length of the optimized spline to verify
    cs_optimized = CubicSpline(sorted_x, optimized_y)
    length_optimized = quad(lambda t: np.sqrt(cs_optimized(t, 1)**2 + cs_optimized(t, 1, True)**2),
                            sorted_x.min(), sorted_x.max())[0]

    # Reconstruct the control points array in the original format
    optimized_control_points = np.column_stack((sorted_x, optimized_y))

    # Optional plotting
    if plot:
        plt.figure(figsize=(8, 6))
        dense_t = np.linspace(sorted_x.min(), sorted_x.max(), 400)
        plt.plot(dense_t, cs_optimized(dense_t), label='Optimized Cubic Spline', color='blue')
        plt.plot(sorted_x, optimized_y, 'o', label='Optimized Control Points', color='red')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Optimized Cubic Spline to Length {target_length} with y > 0')
        plt.legend()
        plt.grid(True)
        plt.show()

    return optimized_control_points, length_optimized

def generate_control_points(n, x_max, y_max, y_min):
    # Ensure n is at least 4 to include the starting, ending points, and at least two random points
    n = max(n, 4)

    # Generate n-2 random x coordinates between 0 and x_max
    x_coords = np.random.uniform(0, x_max, n-2)
    x_coords = np.round(np.sort(x_coords), 2)  # Sort and round to two decimal places
    
    # Generate n-2 random y coordinates between y_min and y_max
    y_coords = np.random.uniform(y_min, y_max, n-2)
    y_coords = np.round(y_coords, 2)  # Round to two decimal places
    
    # Combine x and y coordinates
    control_points = np.column_stack((x_coords, y_coords))

    # Prepend (0,0) and append (x_max, y_max), rounded to two decimals
    start_point = np.array([[0, 0]])
    end_point = np.array([[x_max, y_max]])
    control_points = np.vstack([start_point, control_points, end_point])

    return control_points

def create_profile(n, x_max, y_min, y_max, length, circle_radius, circle_heigth, plot=False):
    control_points = generate_control_points(n, x_max, y_max, y_min)
    optimized_control_points, length = optimize_spline_length(control_points, length, plot=plot)
    l1 = Spline(*optimized_control_points)
    l1 += Line(optimized_control_points[n-1], (x_max, 0))
    l1 += mirror(l1, Plane.XZ)
    f = make_face(l1)
    c = Pos(X=circle_heigth)*Circle(circle_radius)
    return f-c

def create_quarter_spiral(edge_width, edge_height, label="quarter_spiral"):
    a = Line((0,0),(edge_width,0))
    b = Line((edge_width,0), (edge_width, edge_height))
    c = Line((edge_width,edge_height), (edge_width/2, edge_height))
    d = Line((edge_width/2, edge_height), (edge_width/2, edge_height/2))

    return Compound(label=label, children=[a,b,c,d])

def create_spiral(edge_width, edge_height, label="spiral"):
    a = create_quarter_spiral(edge_width, edge_height)
    b = Rot(Z=90)*create_quarter_spiral(edge_height, edge_width)
    c = Rot(Z=180)*create_quarter_spiral(edge_width, edge_height)
    d = Rot(Z=270)*create_quarter_spiral(edge_height, edge_width)
    return Compound(label=label, children=[a,b,c,d])

def create_array(width, height, n_col, n_row, label="swag"):
    edge_width = 4*width/(10*n_col + 3)
    edge_height = 4*height/(10*n_row + 3)
    fabric=[]
    for i in range (n_col):
        for j in range(n_row):
            fabric+= Pos(i*(5*edge_width/2), j*(5* edge_height/2) )*create_spiral(edge_width, edge_height,label="spiral")
            fabric+= Pos(5*edge_width/4+ i*(5*edge_width/2), 5*edge_height/4+ j*(5*edge_height/2))*create_spiral(edge_width, edge_height, label="spiral")
    r= Rectangle(width, height, align=(Align.MIN, Align.MIN))
    return Pos(edge_width, edge_height)*Compound(label=label, children=fabric), r


bag_heigth = 50  # Maximum x value
bag_width = 10  # y value for all points except the last
bag_length = 20
min_width = 2.5
min_cut_border=5
circle_radius = 2.5
circle_height = 45
profile_length = 70
n = 5 
n_col = 10
n_row = 15

p1 = create_profile(n, bag_heigth, min_width ,bag_width, profile_length, circle_radius, circle_height,plot=False)
p2 = Pos(Z = 3*bag_length)*create_profile(n, bag_heigth, min_width ,bag_width, profile_length, circle_radius, circle_height,plot=False)


p1 = create_profile(n, bag_heigth, min_width ,bag_width, profile_length, circle_radius, circle_height,plot=False)
p2 = Pos(Y = 3*bag_width)*create_profile(n, bag_heigth, min_width ,bag_width, profile_length, circle_radius, circle_height,plot=False)

f1, r1 = create_array(bag_length, profile_length, n_col, n_row, label="swag")
f1 = Pos(Y = 6*bag_width)*f1
r1 = Pos(Y = 6*bag_width)*r1

f2, r2 = create_array(bag_length, profile_length, n_col, n_row, label="swag")
f2 = Pos(Y = 6*bag_width + profile_length + profile_length/10)*f2
r2 = Pos(Y = 6*bag_width + profile_length + profile_length/10)*r2


exporter = ExportSVG(unit=Unit.MM, line_weight=5)
exporter.add_layer("Layer 1", fill_color=None, line_color=(0, 0, 255))
exporter.add_shape([r1,r2], layer="Layer 1")
exporter.add_layer("Layer 2", fill_color=None, line_color=(0, 255, 0))
exporter.add_shape([p1, p2, f1,f2], layer="Layer 2")
exporter.write("./bag2.svg")

show(p1, p2, f1, f2, r1, r2)


