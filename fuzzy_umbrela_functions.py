import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import glob
import plotly.express as px

def readDataBase(lista):
    '''
        Function to read the the PBANDS files and store them into a Pandas DataFrame object
                        kpoint     Energy    s   py   pz   px  dxy  dyz  dz2  dxz  ...
        Atom Spin Band                                                               
        11   UP   1     0.00000 -82.180764  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  1     0.00581 -82.180764  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  1     0.01163 -82.180764  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  1     0.01744 -82.180764  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  1     0.02325 -82.180764  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
        ...                 ...        ...  ...  ...  ...  ...  ...  ...  ...  ... ...  
        6    UP   336   0.02325   3.178702  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  336   0.01744   3.183863  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  336   0.01163   3.174539  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  336   0.00581   3.183356  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
                  336   0.00000   3.181194  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0   
    
        Which has: 
            indexes:   Atom(integer), Spin(char), Band(integer).
            Collumns:  kpoint, Energy, {Orbitals} (All char)

        Inputs:  lista: A list with the names of the PBANDS files to be used to write the DataBase
    '''

    StartKeys=["kpoint"]

    AtomList=[]
    SpinList=[]
    BandList=[]

    DataDict={}

    flag=True
    counter=0
    for File in lista:
        f = open(File)
        AtomVal=int(File.split('_')[1][1:])
        SpinCharacter=File.split('_')[2][:-4]
        
        for l in f.readlines():
            Temp = l.split()
            if len(Temp)!=0:
                if Temp[0]=='#K-Path':
                    EndKeys=Temp[1:]
                if Temp[1]=='Band-Index':
                    BandVal=int(Temp[2])
                if len(Temp)>4 and Temp[0]!='#K-Path' and Temp[0]!='#':
                    AtomList.append(AtomVal)
                    SpinList.append(SpinCharacter)
                    BandList.append(BandVal)
                    
                    for (key, DataNum) in zip(DataDict.keys(), Temp):
                        DataDict[key][counter]=DataNum

                        
                    counter+=1
            if len(Temp)>2 and flag:
                if Temp[1]=='NKPTS' and Temp[3]=='NBANDS:':
                    nkpts=int(Temp[4])
                    nbands=int(Temp[5])
                    for el in StartKeys+EndKeys:
                        if el=="Spin":
                            DataDict[el]=np.zeros([len(lista)*nkpts*nbands], dtype='object') 
                        else:
                            DataDict[el]=np.zeros([len(lista)*nkpts*nbands], dtype='float')
                    flag=False 
        f.close()     
        
    tuples = list(
        zip(
            AtomList,
            SpinList,
            BandList
        )
    )

    index = pd.MultiIndex.from_tuples(tuples, names=["Atom", "Spin", "Band"])

    DataDict=pd.DataFrame.from_dict(DataDict)

    DataDict = DataDict.set_index(index)

    return(DataDict)

def plotBands(DataDict,Atoms,SpinCh,ListOrbitals,fileName='./file.html',marker_Multiplier=10):
    '''
        Function that reads the DataBase and plots the bands with the orcbital character

        Inputs:  
            DataDict: DataBase created from the readDataBase function
            Atoms: List of integers that label which atoms you want to include in the plot (integers)
            SpinCh: List of Spin Channels you want to plot ['UP'] or ['DW'] or ['UP','DW']
            ListOrbitals: List of Obitals to be ploted ['s','px','py','pz', ... ] (characters)
            fileName: Path and name of the HTML file where the plot will be saved
            marker_Multiplier: Affects the size of the marker on the plot (float/integer)
    

    '''
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly

    DataDict_copy = DataDict.copy()

    DataDict[DataDict.columns[2:]] = DataDict[DataDict.columns[2:]].replace({0:np.nan})

    for At in Atoms:
        for SpinT in SpinCh:
            nkpts=len(DataDict.loc[At,SpinT,1]['kpoint'])
            nbands=int(len(DataDict.loc[At,SpinT,])/nkpts)
            for i in range(1,nbands+1):
                customdataAt = np.array(nkpts*[At])           # Customdata to customize the hover window
                customdataSpin = np.array(nkpts*[SpinT])      # Customdata to customize the hover window
                customdatai = np.array(range(1,nkpts+1))      # Customdata to customize the hover window
                fig.add_traces(go.Scatter(x=DataDict.loc[At,SpinT,i]['kpoint'],
                                          y=np.where(np.isnan(DataDict.loc[At,SpinT,i][ListOrbitals].sum(axis=1)) ,np.nan, DataDict.loc[At,SpinT,i]['Energy']),
                                          customdata=np.stack((customdataAt,customdataSpin,customdatai),axis=-1),
                                          # Custom data shows as [[At,SpinT,i],
                                          #                       [At,SpinT,i],
                                          #                       [At,SpinT,i],
                                          #                       .
                                          #                       .
                                          #                       .
                                          #                       [At,SpinT,i]]
                                          name='Band '+str(i),
                                          hovertemplate="<b>Atom: %{customdata[0]} </b><br>Spin: %{customdata[1]}", #<extra></extra>
                                          mode = 'markers',
                                          showlegend = True,
                                          marker=dict(size=marker_Multiplier*DataDict_copy.loc[At,SpinT,i][ListOrbitals].sum(axis=1),
                                                      line=dict(width=0))))



    fig.write_html(fileName) 

def plotEnergies(DataDict,Atoms,SpinCh,ListOrbitals,fileName='./fileEnergy.html',opacity=0.5):

    pd.options.plotting.backend = "plotly"
    fig = DataDict.loc[Atoms,SpinCh,:].plot(barmode = 'overlay',kind="hist",nbins=1000,x='Energy',y=ListOrbitals,opacity=opacity)
    fig.write_html(fileName)

def plotBandsWeight(DataDict,Atoms,SpinCh,ListOrbitals,fileName='./fileBands.html',marker_Multiplier=10):

    pd.options.plotting.backend = "plotly"
    df_sum = DataDict.loc[Atoms,SpinCh,:].groupby(level=[2]).sum()
    fig = df_sum.plot(y = ListOrbitals)
    fig.write_html(fileName)

