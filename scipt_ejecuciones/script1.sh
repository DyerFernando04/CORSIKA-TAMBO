#!/bin/bash

# Directorios (Aquí cambiar la direccion de estas carpetas y crear una carpeta llamada DATA_SCRIPT que contenga la carpeta DATA)
DATA_SCRIPT_DIR="/home/vboxuser/corsika-77500/DATA_SCRIPT"
RUN_DIR="/home/vboxuser/corsika-77500/run"
DATA_DIR="${DATA_SCRIPT_DIR}/DATA"

# Rango de energía inicial y final
START_ENERGY='1 * 10^5'
END_ENERGY='1.3 * 10^5'
INCREMENT='0.1 * 10^5'

# Variable para el número de ejecución (RUNNR)
run_number=1

# Imprime la energía, y tambien sirve para formatear la energía en notación científica estándar
format_energy() {
    printf "%.1E" $(echo "$1" | bc -l)
}

# Energía actual
current_energy=$START_ENERGY

# Bucle principal
while [ $(echo "$current_energy <= $END_ENERGY" | bc -l) -eq 1 ]; do
    formatted_energy=$(format_energy "$current_energy")

    # Modificar RUNNR y ERANGE en all-inputs. En este caso se usa conex-3D-inputs, pero cambiarlo por all-inputs que se usará
    sed -i "s/^RUNNR.*/RUNNR   $run_number                          run number/" "${RUN_DIR}/conex-3D-inputs"
    sed -i "s/^ERANGE.*/ERANGE  $formatted_energy  $formatted_energy/" "${RUN_DIR}/conex-3D-inputs"

    # Ejecutar corsika77500. Aquí tambien cambia depende del ejecutable de run que se tenga y el all-inputs
    (cd "$RUN_DIR" && ./corsika77500Linux_QGSII_urqmd_thin_coast < conex-3D-inputs > output.txt)

    # Crear subcarpeta para la energía actual
    energy_dir="${DATA_DIR}/Energy ${formatted_energy}"
    mkdir -p "$energy_dir"

    # Mover y copiar archivos
    cp "${RUN_DIR}/conex-3D-inputs" "$energy_dir"
    cp "${RUN_DIR}/output.txt" "$energy_dir"
    mv "${RUN_DIR}/DAT"* "$energy_dir"

    # Incrementar la energía y el número de ejecución para la siguiente iteración
    current_energy=$(echo "$current_energy + $INCREMENT" | bc -l)
    run_number=$((run_number + 1))
done

echo "Proceso completado."

