import easygui as eg

texto = ['En este espacio puede cargar una lista, una tupla',
         'las líneas de un archivo y... después editarlo']
MensajeMasivo = eg.codebox(msg='Entrada de fuente',
                title='Control: codebox',
                text=texto)

print(len(MensajeMasivo))

print(MensajeMasivo)

print(type(MensajeMasivo))

# Dividir el mensaje en párrafos
            parrafos = MensajeMasivo.split('\n')

            # Escribir cada párrafo en el área de texto
            for i, parrafo in enumerate(parrafos):
                # Escribir el párrafo actual
                browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(parrafo)

                # Si no es el último párrafo, enviar con "Shift + Enter" para empezar uno nuevo
                if i < len(parrafos) - 1:
                    ActionChains(browser).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

            # Enviar el último párrafo
            browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)

