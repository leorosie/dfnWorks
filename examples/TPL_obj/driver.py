#"""
#   :synopsis: Driver run file for TPL example 
#   :version: 2.0
#   :maintainer: Jeffrey Hyman
#.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>
#"""

from pydfnworks import * 
import os

jobname = os.getcwd() + "/output"
DFN = DFNWORKS(jobname)
<<<<<<< HEAD

DFN.params['domainSize']['value'] = [10,10,10]
DFN.params['h']['value'] = .1
=======
DFN_2 = DFNWORKS(jobname)
DFN.params['domainSize']['value'] = [10,10,10]
DFN.params["h"]["value"] = 0.1
exit(1)
>>>>>>> 0708a103771fb4b3613feebf40808a6cccb2b31f

DFN.add_fracture_family(shape = "ell", distribution = "tpl", kappa = 10.0,
        probability = .5, aspect = 2, 
        beta_distribution = 1, beta = 45.0, theta = 0.0, phi = 0.0, 
        alpha = 1.8, min_radius = 1.0, max_radius = 5.0, p32 = .5)

DFN.add_fracture_family(shape = "ell", distribution = "tpl", kappa = 10.0,
            probability = .5, aspect = 2, beta_distribution = 1, beta = 0.0, 
            theta = 90.0, phi = 45.0, alpha = 1.8, min_radius = 1.0, 
            max_radius = 5.0, p32 = .5)
 
DFN.print_family_information(1)    
 
DFN.make_working_directory(delete = True)

DFN.check_input()

<<<<<<< HEAD

for key in DFN.params.keys():
    print(key, DFN.params[key]['value'])


define_paths()
DFN.create_network()
DFN.output_report()
DFN.mesh_network(coarse_factor=10)

DFN.dfn_flow()
=======
DFN.create_network()
# DFN.output_report()
# DFN.mesh_network(coarse_factor=10)
# DFN.dfn_flow()
>>>>>>> 0708a103771fb4b3613feebf40808a6cccb2b31f
# DFN.dfn_trans()
