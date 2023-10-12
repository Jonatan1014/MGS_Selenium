import requests
image =r"C:\Users\ASUS\Desktop\MGS_Selenium\2.jpeg"
url = "https://uguu.se/upload.php"
files = [("files[]", (image, open(image, "rb")))]
params = {"output": "json"}  # Puedes cambiar "json" a otro formato si lo deseas

response = requests.post(url, files=files, params=params)

if response.status_code == 200:
    # La carga fue exitosa
    response_json = response.json()
    if response_json['success']:
        file_info = response_json['files'][0]
        file_url = file_info['url']
        print("URL del archivo cargado:", file_url)
    else:
        print("Error en la carga:", response_json)
else:
    print("Error en la carga. Código de estado:", response.status_code)
