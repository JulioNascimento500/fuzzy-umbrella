import glob
import fuzzy_umbrela_functions


if __name__ == '__main__':


    lista          = ['PBAND_A11_UP.dat']#glob.glob('PBAND*')

    DataBase = fuzzy_umbrela_functions.readDataBase(lista)


    Atoms          = [11]
    SpinCh         = ['UP']
    #ListOrbitals   = ['dxy','dyz','dz2','dxz','x2-y2']
    ListOrbitals   = ['s','py','pz','px','dxy','dyz','dz2','dxz','x2-y2','fy3x2','fxyz','fyz2','fz3','fxz2','fzx2','fx3','tot']
    fileName       = './file.html'

    fuzzy_umbrela_functions.plotEnergies(DataBase,Atoms,SpinCh,ListOrbitals,fileName='./fileEnergy.html',marker_Multiplier=10)
    fuzzy_umbrela_functions.plotBands(DataBase,Atoms,SpinCh,ListOrbitals,fileName='./file.html')
    fuzzy_umbrela_functions.plotBands(DataBase,Atoms,SpinCh,ListOrbitals,fileName='./fileBands.html',marker_Multiplier=10)