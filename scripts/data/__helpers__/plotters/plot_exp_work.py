# Libraries
import matplotlib.pyplot as plt
import numpy as np, math
from copy import deepcopy
from scipy.interpolate import splev, splrep, splder
from scipy.integrate import simps

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list, y_list, resolution=50, smooth=False):
        thin_x_list = get_thinned_list(x_list, resolution)
        thin_y_list = get_thinned_list(y_list, resolution)
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(thin_x_list, thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self):
        self.spl = splder(self.spl)

    # Evaluate
    def evaluate(self, x_list):
        return list(splev(x_list, self.spl))

# For differentiating a curve
def differentiate_curve(curve, x_label, y_label):
    curve = deepcopy(curve)
    interpolator = Interpolator(curve[x_label], curve[y_label])
    interpolator.differentiate()
    curve[y_label] = interpolator.evaluate(curve[x_label])
    return curve

# Returns a thinned list
def get_thinned_list(unthinned_list:list, density:int) -> list:
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Tries to float cast a value
def try_float_cast(value:str) -> float:
    try:
        return float(value)
    except:
        return value

# Converts CSV data into a curve dict
def get_curve_dict(headers:list, data:list) -> dict:
    
    # Get indexes of data
    list_indexes = [i for i in range(len(data[2])) if data[2][i] != ""]
    info_indexes = [i for i in range(len(data[2])) if data[2][i] == ""]
    
    # Create curve
    curve = {}
    for index in list_indexes:
        value_list = [float(d[index]) for d in data]
        value_list = get_thinned_list(value_list, 200)
        curve[headers[index]] = value_list
    for index in info_indexes:
        curve[headers[index]] = try_float_cast(data[0][index])

    # Return curve
    return curve

# Initialise
work_failure_list = []
avg_work_rate_list = []

# File names
file_path_list = [
    "../../creep/inl_1/AirBase_900_36_G22.csv",
    "../../creep/inl_1/AirBase_900_31_G50.csv",
    "../../creep/inl_1/AirBase_900_28_G45.csv",
    "../../creep/inl_1/AirBase_900_26_G59_unox.csv",
    "../../tensile/inl/AirBase_900_D10.csv",
]

# Iterate through curves
for file_path in file_path_list:

    # Read file
    with open(file_path, "r") as file:
        headers = file.readline().replace("\n","").split(",")
        data = [line.replace("\n","").split(",") for line in file.readlines()]
        curve = get_curve_dict(headers, data)

    # Get stress
    if curve["type"] == "creep":
        curve["stress"] = [curve["stress"]] * len(curve["strain"])
    
    # Get work rate
    work_failure = simps(curve["stress"], curve["strain"], axis=-1, even='avg')
    # work_failure = curve["stress"][-1] * curve["strain"][-1]
    work_failure = math.log(work_failure)
    work_failure_list.append(work_failure)

    # Get average work rate
    curve["time"] = [t * 3600 for t in curve["time"]]
    d_curve = differentiate_curve(curve, "time", "strain")
    work_rate_list = [curve["stress"][i] * d_curve["strain"][i] for i in range(len(curve["stress"]))]
    avg_work_rate = np.average(work_rate_list)
    avg_work_rate = math.log(avg_work_rate)
    avg_work_rate_list.append(avg_work_rate)
    
    # Plot the results
    plt.scatter([avg_work_rate], [work_failure])

# Gets the gradient and intercept
polynomial = np.polyfit(avg_work_rate_list, work_failure_list, 1)
print(f"M = {polynomial[0]}")
print(f"B = {polynomial[1]}")

# Save the plot
plt.xlabel("log_e(avg_work_rate)")
plt.ylabel("log_e(work_failure)")
plt.legend([file_path.split("/")[-1] for file_path in file_path_list] + ["LOBF"])
plt.savefig("plot")