"""
 Title:         The Elastic Viscoplastic Creep Damage Model
 Description:   Incorporates elasto-viscoplasticity and creep damage
 Author:        Janzen Choi

"""

# Libraries
import modules.models.__model__ as model
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage
from neml.nlsolvers import MaximumIterations

# Model Parameters
STRESS_RATE  = 0.0001
HOLD         = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 1001
STRAIN_MAX   = 0.5

# The Elastic Visco Plastic Creep Damage Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):
        self.add_param("evp_s0",  0.0e1, 1.0e2)
        self.add_param("evp_R",   0.0e1, 1.0e2)
        self.add_param("evp_d",   0.0e1, 1.0e2)
        self.add_param("evp_n",   1.0e0, 1.0e2)
        self.add_param("evp_eta", 0.0e1, 1.0e6)
        self.add_param("cd_A",    0.0e1, 1.0e4)
        self.add_param("cd_xi",   0.0e1, 1.0e2)
        self.add_param("cd_phi",  0.0e1, 1.0e2)
    
    # Gets the predicted curve
    #   Alloy 617 @ 800:    [48.96021,17.82262,9.568748,2.031041,56309.59,1995.801,5.438601,6.79012]
    #   Alloy 617 @ 900:    [0.567351,24.64534,34.15175,2.103748,31803.17,2679.531,4.155071,9.270845]
    #   Alloy 617 @ 1000:   [7.805677767,0.036500284,6.99330568,2.186529312,20539.05913,2388.920806,3.591732525,6.751795258]
    def get_prd_curve(self, exp_curve, evp_s0, evp_R, evp_d, evp_n, evp_eta, cd_A, cd_xi, cd_phi):

        # Define model
        elastic_model = elasticity.IsotropicLinearElasticModel(exp_curve["youngs"], "youngs", exp_curve["poissons"], "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator)
        effective_stress = damage.VonMisesEffectiveStress()
        cd_model      = damage.ModularCreepDamage(elastic_model, cd_A, cd_xi, cd_phi, effective_stress)
        evpcd_model   = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, cd_model)

        # Get predictions
        if exp_curve["type"] == "creep":
            stress_max = exp_curve["stress"]
            try:
                creep_results = drivers.creep(evpcd_model, stress_max, STRESS_RATE, HOLD, T=exp_curve["temp"], verbose=False,
                                              check_dmg=False, dtol=0.95, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
                return {"x": list(creep_results["rtime"] / 3600), "y": list(creep_results["rstrain"])}
            except MaximumIterations:
                return
        elif exp_curve["type"] == "tensile":
            strain_rate = exp_curve["strain_rate"] / 3600
            try:
                tensile_results = drivers.uniaxial_test(evpcd_model, erate=strain_rate, T=exp_curve["temp"], emax=STRAIN_MAX, nsteps=NUM_STEPS)
                return {"x": list(tensile_results["strain"]), "y": list(tensile_results["stress"])}
            except MaximumIterations:
                return