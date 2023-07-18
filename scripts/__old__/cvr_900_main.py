import sys; sys.path += [".."]
from moga_neml.api import API

api = API("cvr 900 all")
api.define_model("cvr")

api.read_data("tensile/AirBase_900_D10.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.remove_damage(0.4, 0.8)
api.add_error("y_area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.remove_damage(0.4, 0.8)
api.add_error("y_area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.remove_damage(0.4, 0.8)
api.add_error("y_area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_damage(0.4, 0.8)
api.add_error("y_area", "time", "strain")

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

api.set_recorder(10, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)