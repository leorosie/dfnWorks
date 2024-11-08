'''
   mapdfn2pflotran.py

   Call methods in mapdfn.py to take output of dfnWorks-Version2.0, create
   equivalent continuous porous medium representation, and write parameters
   (permeability, porosity, tortuosity) to files for use with PFLOTRAN.

   Usage: Edit values for origin, nx, ny, nz, d, k_background, bulk_por,
          tortuosity factor, and h5origin.
          Paths and filenames are hardwired and may also need to be checked.
          As written, they assume script is being called from a subdirectory.
          Then: python mapdfn2pflotran.py

   Dependencies: mapdfn.py
                 numpy
                 h5py

   Author: 

   Date: 07/13/18
   SAND Number: SAND2018-7605 O

'''
import time

from pydfnworks.dfnGen.meshing.mapdfn_ecpm.mapdfn_upscale import mapdfn_porosity, mapdfn_perm_iso, mapdfn_perm_aniso
from pydfnworks.dfnGen.meshing.mapdfn_ecpm.mapdfn_io import write_h5_files
from pydfnworks.dfnGen.meshing.mapdfn_ecpm.mapdfn_helper_functions import setup_output_dir, setup_domain


def mapdfn_ecpm(self,
                matrix_perm,
                matrix_porosity,
                cell_size,
                matrix_on = False, 
                tortuosity_factor=0.001,
                lump_diag_terms=False,
                correction_factor=True,
                sub_domain = None,
                sub_origin = None,
                sub_directory = "sub",
                output_dir="mapdfn_ecpm"):
    """ This script takes the top-level directory of the dfn and maps it to an ecpm, saving the ecpm files in that directory
  
    Parameters
    -----------------
        self : dfnWorks object
        
        cell_size : float
            The cell size (meters) to use for the meshing

        correction_factor : boolean
            Apply stairstep correction from EDFM to  not applied to permeability

        
    Returns
    -----------------
        None

    Authors
    -----------------
        Emily Stein (ergiamb@sandia.gov)
        Applied Systems Analysis and Research, 8844
        Sandia National Laboratories
    
        Edited by Teresa Portone (tporton@sandia.gov) 11/2020 to take arguments.

        Rosie Leone 

        Jeffrey Hyman 07/2023 - Integration with pydfnWorks 

    Notes
    -----------------


    """
    print("\n")
    print('=' * 80)
    print("* Starting MAPDFN - ECPM")
    print('=' * 80)

    # setup the domain

    if isinstance(cell_size, float) or isinstance(cell_size, int):
       cell_size = [cell_size, cell_size, cell_size]
    elif len(cell_size) != 3:
       error_msg = f"Error: The cell size must be a float or list of three values"
       sys.stderr.write(error_msg)
       sys.exit(1)

    if sub_origin and sub_domain:
      if len(sub_origin) != 3:
         error_msg = f"Error: The sub_origin size must be a list of three values"
         sys.stderr.write(error_msg)
         sys.exit(1)
      if len(sub_domain) != 3:
         error_msg = f"Error: The sub_domain must be a list of three values"
         sys.stderr.write(error_msg)
         sys.exit(1)
      domain = {'x':sub_domain[0],'y':sub_domain[1],'z':sub_domain[2]}
      origin = [-1 * domain['x'] / 2, -1 * domain['y'] / 2, -1 * domain['z'] / 2]
      
      h5origin = sub_origin
      filenames = setup_output_dir(output_dir, self.jobname,sub_directory)
    elif sub_domain or sub_origin:
      error_msg = f"Error: Must specify both sub_domain and sub_origin"
      sys.stderr.write(error_msg)
      sys.exit(1)
    else:
      domain = self.domain
      # Origin of area to map in DFN domain coordinates (0,0,0 is center of DFN)
      origin = [-1 * domain['x'] / 2, -1 * domain['y'] / 2, -1 * domain['z'] / 2]
      h5origin = [0,0,0]
      filenames = setup_output_dir(output_dir, self.jobname)
      
    nx, ny, nz, num_cells = setup_domain(domain, cell_size)

    # id cells that intersect the DFN

    cell_fracture_id = self.mapdfn_tag_cells(origin, num_cells, nx, ny, nz,
                                             cell_size)

    porosity, k_iso, k_aniso = self.mapdfn_upscale(num_cells, cell_fracture_id,
                                                   cell_size, matrix_porosity,
                                                   matrix_perm,
                                                   lump_diag_terms,
                                                   correction_factor)

    # write evereything to files
    #add origin as keyword
    write_h5_files(filenames, nx, ny, nz, cell_size, cell_fracture_id, k_iso,
                   k_aniso, porosity, matrix_perm, tortuosity_factor, matrix_on,
                   h5origin)

    print('=' * 80)
    print("* MAPDFN Complete")
    print('=' * 80)
    print("\n")
