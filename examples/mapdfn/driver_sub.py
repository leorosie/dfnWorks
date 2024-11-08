#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 12:04:03 2020

@author: rosie
"""

import os, sys
from pydfnworks import *

src_path = os.getcwd()

jobname = f"{src_path}/output_subtest"

DFN = DFNWORKS(jobname)

DFN.params['domainSize']['value'] = [10.0, 10.0, 10.0]
DFN.params['domainSizeIncrease']['value'] = [1, 1, 1]
DFN.params['h']['value'] = 0.03
DFN.params['stopCondition']['value'] = 1
DFN.params['seed']['value'] = 1
DFN.params['boundaryFaces']['value'] = [1, 1, 0, 0, 0, 0]
DFN.params['visualizationMode']['value'] = True
DFN.params['seed']['value'] = 200  #seed for random generator 0 seeds off clock
DFN.params['ignoreBoundaryFaces']['value'] = False
DFN.params['boundaryFaces']['value'] = [1, 1, 0, 0, 0, 0]



DFN.add_user_fract(shape='ell',
                   radii=6,
                   translation=[-4, 0, 2],
                   normal_vector=[30, 15, 60],
                   number_of_vertices=5,
                   aperture=1.0e-3)

DFN.add_user_fract(shape='ell',
                   radii=10,
                   translation=[0, 0, 0],
                   normal_vector=[95, 5, 0],
                   number_of_vertices=5,
                   aperture=1.0e-3)

DFN.add_user_fract(shape='ell',
                   radii=6,
                   aspect_ratio=1,
                   translation=[4, 0, 2],
                   normal_vector=[30, 15, 60],
                   number_of_vertices=5,
                   aperture=1.0e-3)

DFN.add_user_fract(shape='ell',
                   radii=6,
                   aspect_ratio=1,
                   translation=[4, 0, -4],
                   normal_vector=[30, 15, 60],
                   number_of_vertices=5,
                   aperture=5.0e-5)

DFN.make_working_directory(delete=True)
DFN.define_paths()
DFN.print_domain_parameters()
DFN.check_input()
DFN.create_network()
#DFN.dump_hydraulic_values()
#DFN.mesh_network()

#DFN.dfn_flow()
mat_perm = 1e-16
mat_por = 0.1
cell_size = [1.0,1.0,1.0]

DFN.mapdfn_ecpm(mat_perm, mat_por, cell_size)

mat_perm = 1e-16
mat_por = 0.1
cell_size = [0.1,0.1,0.1]
sub_domain = [1,1,1]
sub_origin = [5,5,5]

DFN.mapdfn_ecpm(mat_perm, mat_por, cell_size,sub_domain=sub_domain,sub_origin=sub_origin)

DFN.dfnFlow_file = f"{src_path}/cpm_transport_sub.in"
DFN.local_dfnFlow_file = f"cpm_transport_sub.in"
DFN.pflotran()
