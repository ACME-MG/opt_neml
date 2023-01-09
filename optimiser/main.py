"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(False, "evpwd 70,80 wide")
api.read_data(["G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# api.remove_damage()
api.define_model("evpwd")
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.prepare_objective()
api.prepare_recorder(10, 10)
api.optimise(10000, 400, 400, 0.65, 0.35)
