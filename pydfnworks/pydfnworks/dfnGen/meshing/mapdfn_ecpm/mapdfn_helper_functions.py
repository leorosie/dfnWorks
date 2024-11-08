import os, sys


def setup_output_dir(output_dir_local, jobname, sub_directory=None):
    """ Create ECPM output directory

    Parameters
    ----------------
        output_dir : string
            relative path name of output directory. 

    Returns
    ------------
        filenames : dict
            Dictionary of h5 filenames 

    Notes
    ------------
        The name is combined with DFN.jobname to be an absolute path DFN.jobname + / + output_dir
    """
    print(f"--> Creating output directory {output_dir_local}")
    output_dir = jobname + os.sep + output_dir_local
    if sub_directory is not None:
        output_dir += os.sep + output_dir_local + "_" + sub_directory

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.chdir(output_dir)
    filenames = {
        "mapdfn": output_dir + '/mapdfn.h5',
        'isotropic_k': output_dir + '/isotropic_k.h5',
        'anisotropic_k': output_dir + '/anisotropic_k.h5',
        'tortuosity': output_dir + '/tortuosity.h5',
        'porosity': output_dir + '/porosity.h5',
        'materials': output_dir + '/materials.h5'
    }

    return filenames


def setup_domain(domain, cell_size,sub_origin=None):
    """ Initialize domain and discretization

    Parameters
    -----------------
        domain : dictionary
            Domain size in x, y, z from DFN object
        cell_size : list
            Hexahedron cell size in x, y, z

    Returns
    -----------------
        nx : int
            Number of cells in x direction 
        ny : int
            Number of cells in y direction
        nz : int
            Number of cells in z direction 
        num_cells : int 
            Total number of cells in the domain

    Notes
    -----------------
    
    
    
    """
    print("--> Computing discrete domain parameters")

    [nx, ny, nz] = [
        int(domain['x'] / cell_size[0]),
        int(domain['y'] / cell_size[1]),
        int(domain['z'] / cell_size[2])
    ]

    num_cells = nx * ny * nz

    #Check to see if evenly divides the domain, considering non integer cell sizes

    #Convert cell_size to integer if it isn't one already
    cell_size_x,domain_x = convert_to_integer(cell_size[0],domain['x'])
    cell_size_y,domain_y = convert_to_integer(cell_size[1],domain['y'])
    cell_size_z,domain_z = convert_to_integer(cell_size[2],domain['z'])
    
    if domain_x % cell_size_x + domain_y % cell_size_y + domain_z % cell_size_z:
        error_msg = f"Error: The cell size you've specified, {cell_size} m, does not evenly divide the domain. Domain size: {domain['x']} x {domain['y']} x {domain['z']} m^3."
        sys.stderr.write(error_msg)
        sys.exit(1)
    print(f"--> Hexahedron edge length {cell_size} m")
    print(f"--> Domain is {nx} x {ny} x {ny} cells. ")
    print(f"--> Total number of cells {num_cells}\n")
    return nx, ny, nz, num_cells


def convert_to_integer(cell_size,domain):

    if (cell_size == int(cell_size)):
        pass
    else:
        while ((cell_size) != int(cell_size)):
            cell_size *= 10
            domain *= 10

    return cell_size,domain
            
