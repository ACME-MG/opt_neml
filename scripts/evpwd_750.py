import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwd 750")
api.def_model("evpwd")

api.read_file("creep/inl_2/AirBase_750_137_a.csv", True)
api.read_file("creep/inl_2/AirBase_750_118_b.csv", True)
api.read_file("creep/inl_2/AirBase_750_95_a.csv", False)
api.read_file("tensile/AirBase_750_D6.csv", True)

api.visualise("creep")
api.visualise("tensile")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
api.add_error("y_area", "tensile")
api.start_rec(10, 10)
api.start_opt(10000, 200, 100, 0.65, 0.35)