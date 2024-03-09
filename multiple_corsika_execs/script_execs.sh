#!/bin/bash

# Directorios (Aquí cambiar la direccion de estas carpetas y crear una carpeta llamada DATA_SCRIPT que contenga la carpeta DATA)
DATA_SCRIPT_DIR="/corsika-77500/DATA_SCRIPT"
RUN_DIR="/corsika-77500/run"                    #cambiar segun el corsika que se este usando 
DATA_DIR="${DATA_SCRIPT_DIR}/DATA"
status_log="${DATA_SCRIPT_DIR}/statuslog1.txt"  #cambiar el numero segun el identificador del proceso 
# Rango de energía inicial y final
START_ENERGY='1. * 10^6'
END_ENERGY='40 * 10^6'
INCREMENT='1 * 10^6'

# Imprime la energía, y tambien sirve para formatear la energía en notación científica estándar
format_energy() {
    LC_NUMERIC=C printf "%.2E" $(echo "$1" | bc -l)
}

# initializes statuslog
general_start_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "start: Script is running simulations from $START_ENERGY GeV to $END_ENERGY GeV with steps of $INCREMENT GeV; general_start=$general_start_time" >> "$status_log"

# Energía actual
current_energy=$START_ENERGY

# Bucle principal
while [ $(echo "$current_energy <= $END_ENERGY" | bc -l) -eq 1 ]; do

    formatted_energy=$(format_energy "$current_energy")
    
    #updates status_log
    start_time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "current_sim=$formatted_energy; start_time=$start_time" >> "$status_log"
    
    # Modificar RUNNR y ERANGE en all-inputs. En este caso se usa conex-3D-inputs, pero cambiarlo por all-inputs que se usará
    sed -i "s/^ERANGE.*/ERANGE  $formatted_energy  $formatted_energy/" "${RUN_DIR}/all-inputs-inclined"
    
    # Crear subcarpeta para la energía actual
    energy_dir="${DATA_DIR}/Energy_${formatted_energy}"
    mkdir -p "$energy_dir"
    
    for run_number in 1 2 3 4 5
    do
    	# Generar número aleatorio
    	seed_a=$((1 + $RANDOM % 1000))
    	seed_b=$((1 + $RANDOM % 1000))
    	
    	sed -i "s/^RUNNR.*/RUNNR   $run_number                          run number/" "${RUN_DIR}/all-inputs-inclined"
    	
    	# Cambiar SEEDs
    	sed -i "s/^SEED    1   0   0.*/SEED    1   $seed_a   0                  seed for 1. random number sequence/" "${RUN_DIR}/all-inputs-inclined"
    	sed -i "s/^SEED    2   0   0.*/SEED    1   $seed_b   0                  seed for 2. random number sequence/" "${RUN_DIR}/all-inputs-inclined"
    	
    	# Ejecutar corsika77500. Aquí tambien cambia depende del ejecutable de run que se tenga y el all-inputs
    	(cd "$RUN_DIR" && ./corsika77500Linux_QGSII_urqmd_inclined < all-inputs-inclined > output$run_number.txt)
    	
    	# Mover y copiar archivos
    	mv "${RUN_DIR}/output$run_number.txt" "$energy_dir"
    	mv "${RUN_DIR}/DAT"* "$energy_dir"
    done
	
    # Incrementar la energía y el número de ejecución para la siguiente iteración
    current_energy=$(echo "$current_energy + $INCREMENT" | bc -l)
done


#ends statuslog
general_finish_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "finished at $general_finish_time" >> "$status_log"
echo "Proceso completado."

