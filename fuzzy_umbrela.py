import glob
import fuzzy_umbrela_functions


if __name__ == '__main__':


    lista          = ['PBAND_A11_UP.dat']#glob.glob('PBAND*')

    DataBase = fuzzy_umbrela_functions.readDataBase(lista)


    Atoms          = [11]
    SpinCh         = ['UP']
    ListOrbitals   = ['s']
    fileName       = './file.html'

    fuzzy_umbrela_functions.plotBands(DataBase,Atoms,SpinCh,ListOrbitals,fileName)
