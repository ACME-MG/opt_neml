import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpwdb f 900 st ungrouped", input_path="../data", output_path="../results")

api.define_model("evpwdb")

api.fix_param("evp_s0",  4.8238)
api.fix_param("evp_R",   378.86)
api.fix_param("evp_d",   0.1423)
api.fix_param("evp_n",   4.4021)
api.fix_param("evp_eta", 1006.9)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_error("damage", weight=0.1)
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_error("damage", weight=0.1)
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("area", "strain", "stress")
api.add_error("end", "strain")
api.add_error("end", "stress")
api.add_error("damage", weight=0.1)

api.reduce_errors("square_average")
api.reduce_objectives("square_average")
api.group_errors(name=True, type=False, labels=False)

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
