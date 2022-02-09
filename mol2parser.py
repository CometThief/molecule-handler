import pandas as pd
import numpy as np
from tqdm import tqdm
import glob
import gzip
import time
import sys

#script, file = sys.argv

ATOM_COLUMN_NAMES = (
 'atom_id',
 'atom_name',
 'x',
 'y',
 'z',
 'atom_type',
 'subst_id',
 'subst_name',
 'charge'
)

BOND_COLUMN_NAMES = (
'bond_id',
'origin_atom_id',
'target_atom_id',
'bond_type'
)

ATOM_COLUMN_TYPES = (int, str, float, float, float, str, int, str, float)
BOND_COLUMN_TYPES = (int, int, int, str)

class mol2pandas:
    def __init__(self,_df_ATOM=None,_df_BOND=None,zinc_code=None):
        self._df_ATOM = _df_ATOM
        self._df_BOND = _df_BOND
        self.zinc_code = zinc_code
        

    @staticmethod
    def chemspace_reduction_size(min, max):
        '''Creates chemical subspace according to min/max criteria in nm'''

        alltranches = mol2pandas()._all_tranches()

        for single_tranche in tqdm(alltranches):

            if single_tranche.endswith('.mol2.gz'):
                single_tranche = mol2pandas().open_zip(single_tranche)
            elif single_tranche.endswith('.mol2'):
                pass
            else:
                print('File could not be parsed. Accepted file extensions are .mol2 and .mol2.gz')

            for ATOM, BOND, zincid in mol2pandas().molecule_generator(single_tranche):
            
                current_molecule = mol2pandas(ATOM, BOND, zincid)
                a = mol2pandas().maxdist_all(ATOM)
                #a = mol2pandas().all_distances(ATOM)
                print(a)
                #print(a.info(verbose=True))
                input()



                #BOND['size_condition'] = ( (BOND['bond_length'] < max) & (BOND['bond_length'] > min))
                #print(BOND)
                #pupu horrible
                #if BOND['size_condition'].any():
                    #print('TRANCHES: ', tranche_counter)
                    #time.sleep(1)

    @staticmethod
    def open_zip(file):
        with gzip.open(file, 'rb') as f:
            return f.read().decode('utf-8').split('\n')

    @staticmethod
    def _all_tranches(dir='./tranches/*'):
        '''Returns sorted list of all filenames in specified directory. Default is ./tranches'''

        return sorted(glob.glob(dir))

    @staticmethod
    def molecule_generator(file):
        '''Generator that accepts a tranche and yields @<TRIPOS>ATOM, @<TRIPOS>BOND, 
        and ZINCXXXX (in that order).'''

        current_tranche = mol2pandas().fetch_tranche_list(file)
        
        for ATOM, BOND, zincid in zip(mol2pandas().get_atomsection(current_tranche),
                    mol2pandas().get_bondsection(current_tranche), 
                    mol2pandas().get_zincid(current_tranche)):

            df_ATOM = mol2pandas()._section_to_pandas(ATOM, ATOM_COLUMN_NAMES, ATOM_COLUMN_TYPES)
            df_BOND = mol2pandas()._section_to_pandas(BOND, BOND_COLUMN_NAMES, BOND_COLUMN_TYPES)

            yield df_ATOM, df_BOND, zincid

    @staticmethod
    def fetch_tranche_list(file):
        '''Transforms raw tranche into usable list (maybe use tuple instead?)'''

        current_tranche = []
        for line in file:
            current_tranche.append(line)
        return current_tranche

    @staticmethod
    def molecule_count(mol2_list):
        total_molecules = 0
        for line in mol2_list:
            if line.startswith('@<TRIPOS>MOLECULE'):
                total_molecules += 1
        if total_molecules == 0:
            raise ValueError(
                    "Structural data could not be loaded. "
                    "Is the input file/text in the mol2 format?"
                )
        return total_molecules

    @staticmethod
    def get_atomsection(mol2_list):
        """Returns atom section from mol2 provided as list of strings.
        Raises ValueError if data is not provided in the mol2 format or file is empty."""

        started = False

        for idx, s in enumerate(mol2_list):
            if s.startswith('@<TRIPOS>ATOM'):
                first_idx = idx + 1
                started = True
            elif started and (s.startswith('@<TRIPOS>') or s.strip() == '' ):
                last_idx_plus1 = idx
                yield mol2_list[first_idx:last_idx_plus1]
                started = False
        if first_idx is None:
            # Raise error when file contains no @<TRIPOS>ATOM
            # (i.e. file is no mol2 file)
            raise ValueError(
                    "Structural data could not be loaded. "
                    "Is the input file/text in the mol2 format?"
                )

    @staticmethod
    def get_bondsection(mol2_list):
        """Returns bond section from mol2 provided as list of strings.
        Raises ValueError if data is not provided in the mol2 format or file is empty."""

        started = False

        for idx, s in enumerate(mol2_list):
            if s.startswith('@<TRIPOS>BOND'):
                first_idx = idx + 1
                started = True
            elif started and (s.startswith('@<TRIPOS>') or s.strip() == '' ):
                last_idx_plus1 = idx
                yield mol2_list[first_idx:last_idx_plus1]
                started = False
        if first_idx is None:
            # Raise error when file contains no @<TRIPOS>ATOM
            # (i.e. file is no mol2 file)
            raise ValueError(
                    "Structural data could not be loaded. "
                    "Is the input file/text in the mol2 format?"
                )

    @staticmethod
    def get_zincid(mol2_list):

        started = False

        for s in mol2_list:
            if s.startswith('ZINC'):
                yield s

    @staticmethod
    def _section_to_pandas(mol2_atom_list, col_names, col_types):
        df = pd.DataFrame([line.split() for line in mol2_atom_list])
        #print(df)
        #print(df.columns)
        #print(col_names)
        #df.columns = col_names
        df.columns = col_names[ :df.shape[1] ]

        for i in range(df.shape[1]):
            df[col_names[i]] = df[col_names[i]].astype(col_types[i])
        return df

    @staticmethod
    def all_distances(molecule):

        cols = ['x', 'y','z']
        
        for i in range(molecule.shape[0]):
            a = molecule.loc[i, cols]
            b = molecule.loc[:, cols]
            c = (a - b)**2
            d = np.sqrt((c['x'] + c['y'] + c['z']).astype(float))

            molecule[ 'd' + str(i+1) ] = d
        
        return molecule

    '''sqrt( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )'''

    @staticmethod
    def maxdist_all(molecule):
        
        molecule = mol2pandas().all_distances(molecule)
        a = molecule.loc[ : , ['d1']: ]
        print(a)
        input()


    @staticmethod
    def _bond_lengths_df(ATOM, BOND):
        cols = ['x', 'y', 'z']
        origin_atoms = ATOM.loc[BOND['origin_atom_id'] - 1, cols].reset_index(drop = True)
        target_atoms = ATOM.loc[BOND['target_atom_id'] - 1, cols].reset_index(drop = True)
        BOND['bond_length'] = np.sqrt(((origin_atoms - target_atoms)**2).sum(axis = 1))

        '''sqrt( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )'''

'''for i, j in mol2pandas().molecule_generator(file):
    print(i)
    print(j)
    #print(j, '\n', j['origin_atom_id'][0], j['origin_atom_id'][0])
    time.sleep(5)'''

#mol2pandas()._all_tranches()

mol2pandas().chemspace_reduction_size(3.5, 4.5)
