from datetime import datetime
import os
# Obtiene la fecha y hora actual
now = datetime.now()

# Formatea la fecha y hora en el formato que desees para la carpeta (año-mes-día_hora-minuto-segundo)
folder_name = now.strftime("Chrome "+"%d-%m-%Y_%H-%M-%S")

# Ruta completa para la carpeta
folder_path = os.path.join('Google', folder_name)

# Crea la carpeta
os.makedirs(folder_path)

print("Carpeta creada:", folder_path)