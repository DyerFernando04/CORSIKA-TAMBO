import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl
from timeit import default_timer
from datetime import timedelta
from tqdm import tqdm

#FUNCTIONS
def formato_tiempo(segundos):
    delta_tiempo = timedelta(seconds=segundos)
    # Construye la cadena de tiempo
    tiempo_formateado = f"({delta_tiempo.days})D ({delta_tiempo.seconds//3600})H ({(delta_tiempo.seconds//60)%60})M ({(delta_tiempo.seconds%60)})S"
    return tiempo_formateado
def imprimir_barra_de_carga(tiempo,iteracion, total, longitud=50):
    porcentaje = int(iteracion / total * 100)
    carga = int(iteracion / total * longitud)
    tiempo_promedio=tiempo/iteracion
    tiempo_faltante=(tiempo_promedio*(total-iteracion))
    barra_de_carga = f"[{'■' * carga}{' ' * (longitud - carga)}] {porcentaje}%            REMAINING TIME: {formato_tiempo(segundos=tiempo_faltante)}"
    print(barra_de_carga, end='\r', flush=True)
def txt_to_df(path,xlims=None,ylims=None,inclined=True):
    # Lists to save the data
    ids = []
    x_values = []
    y_values = []
    t_values = []
    px_values = []
    py_values = []
    pz_values = []
    ek_values = []
    w_values = []
    lev_values = []

    # accessing the .txt
    with open(path, 'r') as archivo:
        for linea in archivo:
            try:
                # Divide la línea en partes usando el espacio como separador
                partes = linea.split()

                # Extrae los valores que contienen 'x=', 'y=', 't=', etc.
                id_valor = int(partes[1])
                x_valor = float(partes[2].split('=')[1])/(100)   #en kilometros
                y_valor = float(partes[3].split('=')[1])/(100)   #en kilometros          
                t_valor = float(partes[4].split('=')[1])
                px_valor = float(partes[5].split('=')[1])
                py_valor = float(partes[6].split('=')[1])
                pz_valor = float(partes[7].split('=')[1])
                if inclined==True:
                    x_valor,y_valor= (-y_valor),x_valor
                    px_valor,py_valor= (-py_valor),px_valor
                    pz_valor=-pz_valor
                    #Now Y means upwards the inclined plane and X means to the right 
                ek_valor = float(partes[8].split('=')[1])
                w_valor = float(partes[9].split('=')[1])
                lev_valor = int(partes[10].split('=')[1])

                #if (det_X_inf<=x_valor<=det_X_sup) and (det_Y_inf<=y_valor<=det_Y_sup):
                    # Agrega los valores a las listas
                ids.append(id_valor)
                x_values.append(x_valor)
                y_values.append(y_valor)
                t_values.append(t_valor)
                px_values.append(px_valor)
                py_values.append(py_valor)
                pz_values.append(pz_valor)
                ek_values.append(ek_valor)
                w_values.append(w_valor)
                lev_values.append(lev_valor)
            except:
                pass

    # Crea un DataFrame de Pandas
    data = {
        'id': ids,
        'x': x_values,
        'y': y_values,
        't': t_values,
        'px': px_values,
        'py': py_values,
        'pz': pz_values,
        'ek': ek_values,
        'w': w_values,
        'lev': lev_values,
        'detector': np.nan
    }

    all_data = pd.DataFrame(data).astype({'detector':object})
    if xlims != None:
        all_data = all_data[(all_data['x']>= xlims[0]) & (all_data['x']<= xlims[1])].reset_index(drop=True)
    if ylims != None:
        all_data = all_data[(all_data['y']>= ylims[0]) & (all_data['y']<= ylims[1])].reset_index(drop=True)
    
    return all_data
def assign_to_detector(det_position,df,tol,pf_tol=(None,None)):
    '''
    given a detector position and a tolerance (radius), assign_to_detector(det_position,df,tol) filters the particles that fall
    inside that given detector and updates the dataframe of particles, assigning the
    detector position to the 'detector' column of those entries that fall inside the detector
    
    it also deletes the entries that are in the neighbourhood of the detector but do not fall inside the detector
    
    the parameters are:
    det_position:              a tuple that contains the position (x,y) of the detector
    df:                        the DataFrame of all entries
    tol:                       a tolerance for particle detection (radius of the detector)
    pf_tol=(pf_tolx,pf_toly):  [IGNORE] a tolerance for a preliminary filtering of particles in a rectangular neighbourhood of the detector 
                               (dimensions: 2*pf_tolx by 2*pf_toly) centered at the detector.
                               it is necesary that tol<=pf_tol(both components). large values will cause problems if the rectangular
                               neighbourhood is too big and overlaps with the bounds of other detectors 
    
    the function returns the updated DataFrame
                          
    '''
    if pf_tol==(None,None):
        pf_tol=(1.01*tol,1.01*tol)
    
    det_x,det_y=det_position
    pf_tolx,pf_toly=pf_tol
    possible_particles_index=df.index[(df['x']<=det_x+pf_tolx) & (df['x']>=det_x-pf_tolx) & (df['y']<=det_y+pf_toly) & (df['y']>=det_y-pf_toly)].tolist()
    for index in possible_particles_index:
        x,y=df.loc[index,'x'],df.loc[index,'y']
        if (x-det_x)**2 + (y-det_y)**2 <= tol**2:
            df.at[index,'detector']= det_position
        else:
            df.drop(index, inplace=True, axis=0)
    return df    
def assign_to_detector2(det_position,df,d_side=1):
    '''
    given a detector position and a tolerance (radius), assign_to_detector(det_position,df,tol) filters the particles that fall
    inside that given detector and updates the dataframe of particles, assigning the
    detector position to the 'detector' column of those entries that fall inside the detector
    
    it also deletes the entries that are in the neighbourhood of the detector but do not fall inside the detector
    
    the parameters are:
    det_position:              a tuple that contains the position (x,y) of the detector
    df:                        the DataFrame of all entries
    tol:                       a tolerance for particle detection (radius of the detector)
    pf_tol=(pf_tolx,pf_toly):  [IGNORE] a tolerance for a preliminary filtering of particles in a rectangular neighbourhood of the detector 
                               (dimensions: 2*pf_tolx by 2*pf_toly) centered at the detector.
                               it is necesary that tol<=pf_tol(both components). large values will cause problems if the rectangular
                               neighbourhood is too big and overlaps with the bounds of other detectors 
    
    the function returns the updated DataFrame
                          
    '''
        
    det_x,det_y=det_position
    possible_particles_index=df.index[(df['x']<=det_x+d_side/2.0) & (df['x']>=det_x-d_side/2.0) & (df['y']<=det_y+d_side/2.0) & (df['y']>=det_y-d_side/2.0)].tolist()
    for index in possible_particles_index:
        df.at[index,'detector']= det_position
    return df    

## PARAMETERS
# Paths
txt_path='8-12/DAT000008-inclined (2).txt'
# Array parameters
xlims=(-5000,5000)
ylims=(-1375.5,2000)
sep=150
# Detector dimensions
d_side=1

## TXT to Dataframe
all_data=txt_to_df(txt_path,xlims=(-5000,5000),ylims=(-2000,2000),inclined=True)

## DEFINING DETECTOR ARRAY
x_dets=[]
y_dets=[]

x_low= xlims[0]
y_low= ylims[0]
x_hi = xlims[1]
y_hi = ylims[1]

x=0
y=0

#x values (rectangular grid)
while x < x_hi:
    x_dets.append(x)
    x=x+sep/2
x_dets=list(-1*np.round(x_dets, decimals=2)[:0:-1])+list(np.round(x_dets, decimals=2))

#y values (rectangular grid)
while y < y_hi:
    y_dets.append(y)
    y=y+sep*np.sqrt(3)/2
y_dets=list(-1*np.round(y_dets, decimals=2)[:0:-1])+list(np.round(y_dets, decimals=2))
y_dets=list(np.asarray(y_dets)[np.asarray(y_dets)>y_low])

#complete detector grid list (rectangular array)
complete_grid_list=[]
for y in y_dets:
    for x in x_dets:
        complete_grid_list.append((x,y))
#detector grid list (triangular array)
detector_grid_list=complete_grid_list[1::2]

## DETECTOR ASSIGNMENT AND GEOMETRIC FILTERING
i=0
filtered_data=all_data.copy()
start=default_timer()
for det_position in detector_grid_list:
    assign_to_detector2(det_position,filtered_data,d_side=1)
    i+=1
    now=default_timer()
    imprimir_barra_de_carga(now-start,i,len(detector_grid_list), longitud=50)
filtered_data.dropna(inplace=True)
filtered_data=filtered_data.reset_index(drop=True)

## ENERGY IN EACH DETECTOR
count=0
energies=[]

for det_position in complete_grid_list:
    det_data=filtered_data[filtered_data['detector']==det_position]
    deposited_energy=sum(det_data['ek'])
    energies.append(deposited_energy)
    
y_dets=np.unique(np.asarray(complete_grid_list)[:,1])
x_dets=np.unique(np.asarray(complete_grid_list)[:,0])
len_x=len(x_dets)
len_y=len(y_dets)

det_matrix=np.zeros((len_y,len_x,3)) #det_matrix[i,j,:] (position_x,position_y,energy)

for i in range(len_y):
    y_pos=y_dets[-i-1]
    for j in range(len_x):
        x_pos=x_dets[j]
        det_matrix[i,j,0]=x_pos
        det_matrix[i,j,1]=y_pos
        det_matrix[i,j,2]=float(energies[complete_grid_list.index((x_pos,y_pos))])

## GRAPHS

