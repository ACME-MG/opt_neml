import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp 750")
api.def_model("evp")

api.read_file("creep/inl_2/AirBase_750_137_a.csv", True)
api.rm_damage(200, 0.8)
api.read_file("creep/inl_2/AirBase_750_118_b.csv", True)
api.rm_damage(200, 0.8)
api.read_file("creep/inl_2/AirBase_750_95_a.csv", False)
api.rm_damage(50, 0.6)
api.read_file("tensile/AirBase_750_D6.csv", True)
api.rm_manual(0.4)

api.visualise("creep")
api.visualise("tensile")
api.add_error("y_area", "creep")
api.add_error("y_area", "tensile")
api.start_rec(10, 10)
api.start_opt(10000, 200, 100, 0.65, 0.35)