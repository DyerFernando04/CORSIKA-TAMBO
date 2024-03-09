#!/bin/bash

echo '==============SCRIPT DE CONVERSION DE DAT A TXT================'
echo ' '
echo '   OOO      OOO     OOOO       OOOO    OO   O      O      O    '
echo '  O   O    O   O    O    O    O    O   OO   O    O       O O   '
echo ' O        O     O   O     O   O        OO   O  O        O   O  '
echo ' O        O     O   O    O     OOOO    OO   OO         O     O '
echo ' O        O     O   OOOO           O   OO   O  O       OOOOOOO '
echo '  O   O    O   O    O   O     O    O   OO   O    O     O     O '
echo '   OOO      OOO     O     O    OOOO    OO   O      O   O     O '
echo ' '
echo '=============PARA DIFERENTES VALORES DE ENERGIA================'
echo ' '
echo '==============================================================='
echo ' '

# Directorios (Cambiar por la direccion de estas carpetas)
DATA_SCRIPT_DIR="/home/francisco/Documentos/Corsika/corsika-77500/DATA_SCRIPT"
DATA_DIR="${DATA_SCRIPT_DIR}/DATA"
CORSIKA_READER_DIR="/home/francisco/Documentos/Corsika/corsika-77500/src/utils/coast/CorsikaRead"

# Bucle para procesar cada subcarpeta Energy
for energy_dir in "${DATA_DIR}/Energy"*; do
    if [ -d "$energy_dir" ]; then
        echo "Procesando carpeta: $energy_dir"

        # Encuentra el archivo DAT en la carpeta de energía (sin incluir .long)
        for dat_file in "$energy_dir"/*inclined; do
            if [[ -f "$dat_file" ]]; then
                dat_filename=$(basename "$dat_file")

                # Mueve el archivo DAT al directorio de CorsikaReader y lo ejecuta
                mv "$dat_file" "$CORSIKA_READER_DIR"
                (cd "$CORSIKA_READER_DIR" && ./CorsikaReader "$dat_filename" > "data${dat_filename:7:-9}.txt")

                # Mueve los archivos de vuelta a la carpeta de energía
                mv "${CORSIKA_READER_DIR}/${dat_filename}" "$energy_dir"
                mv "${CORSIKA_READER_DIR}/data${dat_filename:7:-9}.txt" "$energy_dir"
            fi
        done
    fi
done

echo "Proceso completado."
