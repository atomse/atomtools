"""
test atomtools
"""
import os
import glob
import numpy as np
import ase.build




import atomtools
import atomtools.fileutil
import atomtools.geo
import atomtools.name
import atomtools.types
import atomtools.filetype


BASEDIR = os.path.dirname(os.path.abspath(__file__))
np.set_printoptions(precision=3, suppress=True, linewidth=100)


class Test_Atoms(object):
    """docstring for Test_Atoms"""

    def __init__(self, positions, cell):
        super(Test_Atoms, self).__init__()
        self.positions = positions
        self.cell = cell


def test_get_distance_matrix():
    test_cases = [
        {
            'positions': np.array([
                [0., 0., 0.],
                [0., 0., -1.11],
                [0.92, -0.61, -0.11],
                [-0.99, -0.49, -0.11],
                [0.07, 1.1, -0.11],
                [0., 0., 1.76]])
        },
        {
            'positions': np.array([
                [0.7579, 0., 0.],
                [1.8679, 0., 0.],
                [0.8679, -0.8569, -0.6959],
                [0.8679, 1.0326, -0.3922],
                [0.8679, -0.1758, 1.0881],
                [-1.0021, 0., 0.]]),
        },
        {
            'positions': Test_Atoms(positions=np.array([
                [0.7579, 0., 0.],
                [1.8679, 0., 0.],
                [0.8679, -0.8569, -0.6959],
                [0.8679, 1.0326, -0.3922],
                [0.8679, -0.1758, 1.0881],
                [-1.0021, 0., 0.]])+np.array([1.5, 1.5, 1.5]), cell=np.array([
                    [3, 0, 0], [0, 3, 0], [0, 0, 3]]))
        },
    ]

    for case in test_cases:
        case.update({'debug': True})
        print(atomtools.geo.get_distance_matrix(**case))

    print(atomtools.geo.dist_change_matrix(test_cases[0]['positions'], 1))


def test_zmat():
    """
    test zmat
    def input_standard_pos_transform(inp_pos, std_pos, t_vals,
        std_to_inp=True, is_coord = False, debug=False):

    """
    test_cases = [
        {
            'inp_pos': np.array([
                [0., 0., 0.],
                [0., 0., -1.11],
                [0.92, -0.61, -0.11],
                [-0.99, -0.49, -0.11],
                [0.07, 1.1, -0.11],
                [0., 0., 1.76]]),
            'std_pos': np.array([
                [0.7579, 0., 0.],
                [1.8679, 0., 0.],
                [0.8679, -0.8569, -0.6959],
                [0.8679, 1.0326, -0.3922],
                [0.8679, -0.1758, 1.0881],
                [-1.0021, 0., 0.]]),

        },
        {
            'inp_pos': np.array([
                [-1.4951, 0.7264, 0.],
                [-1.5688, -0.6965, 0.],
                [-2.6259, -0.0039, 0.],
                [-0.868, 1.8174, 0.]]),
            'std_pos': np.array([
                [-0.0018, 0.475, 0.],
                [0.6433, 1.7454, 0.],
                [-0.6183, 1.6716, 0.],
                [-0.0018, -0.7834, 0.]]),
        },
        {
            'inp_pos': np.array([[0.493, 0., 0.],
                                 [-0.6573, 0., 0.]]),
            'std_pos': np.array([[0., 0., 0.493],
                                 [0., 0., -0.6573]]),
        },
    ]

    for case in test_cases:
        case.update({'debug': True, 'std_vec': case['inp_pos'][0:2]})
        print(atomtools.geo.input_standard_pos_transform(**case))


def test_get_contact_matrix():
    # import atomse.io
    test_cases = [
        {
            'positions': ase.build.molecule('CH4')
        },
        {
            'positions': ase.build.molecule('HCN')
        },
        {
            'positions': ase.build.molecule('C6H6')
        },
        {
            'positions': ase.build.molecule('H2CO')
        },
        # {
        #     'positions' : atomse.io.read(BASEDIR+'/6.log')
        # },
    ]
    for case in test_cases:
        case.update({'debug': True, })
        print('get_contact_matrix', atomtools.geo.get_contact_matrix(**case))


def test_get_atoms_name():
    x = ase.build.molecule("CH4")
    print(atomtools.name.get_atoms_name(x))


def test_get_atoms_size():
    x = ase.build.molecule("CH4")
    print(atomtools.geo.get_atoms_size(x))


def test_filetype():
    testfiles = os.path.join(BASEDIR, 'chem_file_samples', '*')
    for fname in glob.glob(testfiles):
        if os.path.isfile(fname):
            print(os.path.realpath(fname))
            print(atomtools.filetype.filetype(fname))

    testfiles = os.path.join(BASEDIR, 'chem_file_samples', 'future', '*')
    for fname in glob.glob(testfiles):
        if os.path.isfile(fname):
            print(os.path.realpath(fname))
            print(atomtools.filetype.filetype(fname))


def test_ExtDict():
    test_cases = {
        'positions': np.zeros((10, 3)),
        'numbers': np.zeros((10,)),
        'calc_arrays': {
            'command': 'test',
            'basis': ['6-31G(d)'] * 10,
            'ecp': ['lanl2dz'] * 10,
        }
    }
    x = atomtools.types.ExtDict(test_cases)
    print('-'*25+'\n'+'test get/set')
    print(x.get_positions())
    x.set_positions(np.ones((10, 3)))
    print(x.get_positions())

    print('-'*25+'\n'+'test getitem/setitem')
    print(x['calc_arrays/command'])
    x['calc_arrays/command'] = 'test_again'
    print(x['calc_arrays/command'])

    print('-'*25+'\n'+'test get_all_keys()')
    print(x.get_all_keys())

    print('-'*25+'\n'+'test has_key()')
    print('/calc_arrays/basis', x.has_key('/calc_arrays/basis'))
    print('/xyz', x.has_key('/xyz'))


def test():
    print(atomtools.__file__)
    print(atomtools.version())
    print('-'*50+'\n'+'test_get_distance_matrix()')
    test_get_distance_matrix()
    print('-'*50+'\n'+'test_get_contact_matrix()')
    test_get_contact_matrix()
    print('-'*50+'\n'+'test_get_atoms_name()')
    test_get_atoms_name()
    print('-'*50+'\n'+'test_get_atoms_size()')
    test_get_atoms_size()
    print('-'*50+'\n'+'# test_filetype()')
    test_filetype()
    print('-'*50+'\n'+'# test_zmat()')
    # test_zmat()
    print('-'*50+'\n'+'test_ExtDict()')
    test_ExtDict()


if __name__ == '__main__':
    test()
