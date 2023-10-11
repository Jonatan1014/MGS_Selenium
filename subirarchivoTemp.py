import requests
image =r"C:\Users\ASUS\Desktop\MGS_Selenium\imagen_temporal.png"
url = "https://uguu.se/upload.php"
files = [("files[]", (image, open(image, "rb")))]
params = {"output": "json"}  # Puedes cambiar "json" a otro formato si lo deseas

response = requests.post(url, files=files, params=params)

if response.status_code == 200:
    # La carga fue exitosa
    print("Carga exitosa. Respuesta del servidor:")
    #print(response.json())
    print(response.json())# Aquí puedes acceder a la respuesta en formato JSON
else:
    print("Error en la carga. Código de estado:", response.status_code)
