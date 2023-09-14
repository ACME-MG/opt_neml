import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evp 900 st", input_path="../data", output_path="../results")

api.define_model("evp")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.remove_damage(0.1, 0.7)

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_damage(0.1, 0.7)

api.plot_experimental()
api.set_recorder(50, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
