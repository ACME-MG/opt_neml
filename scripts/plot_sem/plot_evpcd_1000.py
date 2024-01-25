import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_oxidation()
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("dummy")

params_str = """
0.004615	6.1843	2.2823	4.8326	460.27	2357.9	3.5989	6.8388
3.9207	130.97	0.16188	3.9466	752.32	2450.1	3.5356	6.1744
0.012675	18.528	0.99367	4.8134	471.18	2932.6	3.372	5.7802
0.26123	35.054	0.42681	4.7436	490.7	2942.6	3.3807	5.9217
1.4714	3.11	5.9009	4.4241	584.77	1053.2	4.2661	7.136
4.1445	21.946	1.2583	3.9467	726.26	1609	3.8399	5.3898
3.2085	17.287	1.3622	4.0769	697.16	3844.1	3.2156	5.6135
4.3446	10.148	2.2066	3.8806	776.41	2358.5	3.5763	7.0132
3.3748	51.076	0.45747	4.0575	700.49	1035.7	4.2338	6.0336
4.2665	246.76	0.084953	3.9445	738.14	2675.8	3.4395	5.8158

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    # clip        = True,
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 1000),
                   "cd_A": (0, 10000), "cd_xi": (0, 10), "cd_phi": (0, 30)},
)
