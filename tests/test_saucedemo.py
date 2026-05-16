"""
Tests de automatización para saucedemo.com
Cubre: Login, Catálogo de productos y Carrito de compras.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Importamos nuestras funciones auxiliares
from utils.helpers import hacer_login, esperar_elemento, tomar_captura


# ── Configuración del driver (se ejecuta antes/después de cada test) ──────────
@pytest.fixture
def driver():
    """
    Crea el navegador Chrome antes de cada test y lo cierra al terminar.
    El fixture es la forma estándar de Pytest para setup/teardown.
    """
    opciones = Options()
    opciones.add_argument("--start-maximized")       # abre maximizado
    opciones.add_argument("--disable-notifications") # sin popups

    navegador = webdriver.Chrome(options=opciones)
    yield navegador          # acá corre el test
    navegador.quit()         # esto se ejecuta siempre al final, aunque falle


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: Login exitoso
# ═══════════════════════════════════════════════════════════════════════════════
def test_login_exitoso(driver):
    """
    Verifica que el login con credenciales válidas redirige a /inventory.html
    y que la página muestra el título 'Products' o 'Swag Labs'.
    """
    try:
        # Ejecutar el login con usuario y contraseña válidos
        hacer_login(driver)

        # Esperar a que aparezca el título de la página de inventario
        titulo = esperar_elemento(driver, By.CLASS_NAME, "title")

        # Validar que la URL cambió a la página de inventario
        assert "/inventory.html" in driver.current_url, (
            f"Se esperaba /inventory.html en la URL, pero se obtuvo: {driver.current_url}"
        )

        # Validar que el título de la página es el correcto
        assert titulo.text in ["Products", "Swag Labs"], (
            f"Título inesperado: '{titulo.text}'"
        )

        print(f"✓ Login exitoso. URL actual: {driver.current_url}")
        print(f"✓ Título de página: {titulo.text}")

    except Exception as error:
        # Si algo falla, tomamos captura de pantalla
        tomar_captura(driver, "test_login_exitoso")
        raise error


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: Verificación del catálogo de productos
# ═══════════════════════════════════════════════════════════════════════════════
def test_catalogo_productos(driver):
    """
    Verifica que la página de inventario muestra productos correctamente.
    Valida: título, presencia de productos, menú, filtros y datos del primer producto.
    """
    try:
        # Primero hacemos login para poder acceder al catálogo
        hacer_login(driver)

        # ── Validar título de la página ──────────────────────────────────────
        titulo = esperar_elemento(driver, By.CLASS_NAME, "title")
        assert titulo.text == "Products", (
            f"Título incorrecto. Se esperaba 'Products', se obtuvo: '{titulo.text}'"
        )
        print(f"✓ Título correcto: {titulo.text}")

        # ── Validar que haya al menos un producto visible ────────────────────
        productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(productos) > 0, "No se encontraron productos en la página"
        print(f"✓ Productos encontrados: {len(productos)}")

        # ── Obtener nombre y precio del primer producto ──────────────────────
        nombre_producto = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        precio_producto = driver.find_element(By.CLASS_NAME, "inventory_item_price")
        print(f"✓ Primer producto: {nombre_producto.text} - {precio_producto.text}")

        # ── Validar que el menú hamburguesa está presente ────────────────────
        menu = driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu.is_displayed(), "El menú no está visible"
        print("✓ Menú visible")

        # ── Validar que el filtro/selector de orden está presente ────────────
        filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
        assert filtro.is_displayed(), "El filtro de productos no está visible"
        print("✓ Filtro de productos visible")

    except Exception as error:
        tomar_captura(driver, "test_catalogo_productos")
        raise error


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: Agregar producto al carrito
# ═══════════════════════════════════════════════════════════════════════════════
def test_carrito_compras(driver):
    """
    Verifica el flujo completo de agregar un producto al carrito:
    1. Agrega el primer producto
    2. Verifica que el contador del carrito sube a 1
    3. Navega al carrito
    4. Comprueba que el producto aparece en el carrito
    """
    try:
        # Primero hacemos login
        hacer_login(driver)

        # Esperar a que cargue la página de inventario
        esperar_elemento(driver, By.CLASS_NAME, "inventory_list")

        # ── Guardar el nombre del producto antes de agregarlo ────────────────
        nombre_producto = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        print(f"Producto a agregar: {nombre_producto}")

        # ── Hacer clic en el botón "Add to cart" del primer producto ─────────
        boton_agregar = driver.find_element(By.CLASS_NAME, "btn_inventory")
        boton_agregar.click()

        # ── Verificar que el contador del carrito muestra "1" ────────────────
        contador_carrito = esperar_elemento(driver, By.CLASS_NAME, "shopping_cart_badge")
        assert contador_carrito.text == "1", (
            f"El contador del carrito debería ser 1, pero muestra: '{contador_carrito.text}'"
        )
        print(f"✓ Contador del carrito: {contador_carrito.text}")

        # ── Navegar al carrito haciendo clic en el ícono ─────────────────────
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # ── Verificar que estamos en la página del carrito ───────────────────
        assert "/cart.html" in driver.current_url, (
            f"No se redirigió al carrito. URL actual: {driver.current_url}"
        )

        # ── Verificar que el producto aparece en el carrito ──────────────────
        items_carrito = esperar_elemento(driver, By.CLASS_NAME, "cart_item")
        nombre_en_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text

        assert nombre_en_carrito == nombre_producto, (
            f"El producto en el carrito es '{nombre_en_carrito}', "
            f"pero se agregó '{nombre_producto}'"
        )

        print(f"✓ Producto en carrito: {nombre_en_carrito}")
        print("✓ Test de carrito completado con éxito")

    except Exception as error:
        tomar_captura(driver, "test_carrito_compras")
        raise error
