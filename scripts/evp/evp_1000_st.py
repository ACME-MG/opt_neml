import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evp 1000 st", input_path="../data", output_path="../results")

api.define_model("evp")

api.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
api.remove_damage(0.2, 0.8)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
api.remove_damage(0.2, 0.8)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_1000_12_G52.csv")
api.remove_damage(0.2, 0.8)

api.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
api.remove_damage(0.2, 0.8)

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, 10, True, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
