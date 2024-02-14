import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("dummy")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5	58.766	342.03	350.26	787.33	2.1695	10.774
5.6908	66.627	1.9851	4.7723	1621.6	72.451	405.41	243.18	615.7	2.4798	11.349
19.2	52.204	1.7579	4.5105	1614.6	42.521	267.95	334.54	705.41	2.4141	9.9943
31.327	104.92	0.8548	3.7508	2575.8	54.389	332.02	305.08	649.63	1.9969	6.8035
22.393	462.57	0.13573	4.314	1828.1	39.27	260.65	413.34	811.22	1.9452	6.8817
11.45	53.151	7.1666	3.9502	2221.6	30.864	224.62	344.66	727.88	1.3497	5.9263
18.768	89.18	0.88069	4.5055	1677.4	38.712	255.73	442.25	873.64	1.9576	7.3303
23.304	306.58	0.32123	4.2592	1822.6	23.273	176.69	324.24	666.96	1.6099	11.785
31.137	31.413	4.6003	3.6958	2583	33.186	237.43	530.65	982.77	1.6338	18.083
29.726	45.991	2.3174	3.9613	2101.3	32.4	230.15	430.89	764.95	1.6494	19.93

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
)
