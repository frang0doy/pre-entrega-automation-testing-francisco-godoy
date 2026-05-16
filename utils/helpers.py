"""
Funciones auxiliares para los tests de SauceDemo.
Contiene funciones reutilizables para no repetir código en los tests.
"""

import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ── Constantes del sitio ──────────────────────────────────────────────────────
BASE_URL = "https://www.saucedemo.com"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
WAIT_TIME = 10  # segundos de espera máxima


# ── Función: esperar elemento ─────────────────────────────────────────────────
def esperar_elemento(driver, by, selector, tiempo=WAIT_TIME):
    """
    Espera a que un elemento sea visible en la página y lo retorna.
    Usa espera explícita para no depender de tiempos fijos (time.sleep).
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.visibility_of_element_located((by, selector)))


# ── Función: hacer login ──────────────────────────────────────────────────────
def hacer_login(driver, usuario=USERNAME, contrasena=PASSWORD):
    """
    Navega a la página de login e ingresa las credenciales recibidas.
    Por defecto usa el usuario y contraseña válidos de saucedemo.
    """
    driver.get(BASE_URL)

    # Esperar campo de usuario y completarlo
    campo_usuario = esperar_elemento(driver, By.ID, "user-name")
    campo_usuario.clear()
    campo_usuario.send_keys(usuario)

    # Completar contraseña
    campo_contrasena = driver.find_element(By.ID, "password")
    campo_contrasena.clear()
    campo_contrasena.send_keys(contrasena)

    # Hacer clic en el botón de login
    driver.find_element(By.ID, "login-button").click()


# ── Función: tomar captura de pantalla ───────────────────────────────────────
def tomar_captura(driver, nombre_test):
    """
    Toma una captura de pantalla y la guarda en la carpeta reports/screenshots.
    Se usa automáticamente cuando un test falla.
    """
    # Crear carpeta si no existe
    carpeta = "reports/screenshots"
    os.makedirs(carpeta, exist_ok=True)

    # Nombre del archivo con fecha y hora para que no se pisen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{carpeta}/{nombre_test}_{timestamp}.png"

    driver.save_screenshot(nombre_archivo)
    print(f"Captura guardada: {nombre_archivo}")
    return nombre_archivo
