# Automatización QA - SauceDemo

Proyecto de automatización de pruebas para el sitio [saucedemo.com](https://www.saucedemo.com), desarrollado con Python, Pytest y Selenium WebDriver.

---

## Propósito del proyecto

Automatizar los flujos principales del sitio SauceDemo para validar:

- **Login**: que el usuario pueda ingresar con credenciales válidas
- **Catálogo**: que los productos se muestren correctamente
- **Carrito**: que se puedan agregar productos y verlos en el carrito

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| Selenium WebDriver | Automatización del navegador |
| Pytest | Framework de testing |
| pytest-html | Generación de reporte HTML |
| webdriver-manager | Gestión automática del driver de Chrome |
| Git / GitHub | Control de versiones |

---

## Estructura del proyecto

```
pre-entrega-automation-testing/
│
├── tests/
│   ├── __init__.py
│   └── test_saucedemo.py     # Los 3 casos de prueba
│
├── utils/
│   ├── __init__.py
│   └── helpers.py            # Funciones auxiliares reutilizables
│
├── reports/                  # Se genera al correr los tests
│   └── screenshots/          # Capturas automáticas en caso de fallo
│
├── pytest.ini                # Configuración de pytest
├── requirements.txt          # Dependencias del proyecto
└── README.md
```

---

## Instalación de dependencias

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/pre-entrega-automation-testing-nombre-apellido.git
cd pre-entrega-automation-testing-nombre-apellido
```

### 2. (Opcional) Crear entorno virtual

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

> **Nota:** Necesitás tener Google Chrome instalado. El driver se descarga automáticamente gracias a `webdriver-manager`.

---

## Cómo ejecutar las pruebas

### Ejecutar todos los tests con reporte HTML

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

### Ejecutar un test específico

```bash
pytest tests/test_saucedemo.py::test_login_exitoso -v
pytest tests/test_saucedemo.py::test_catalogo_productos -v
pytest tests/test_saucedemo.py::test_carrito_compras -v
```

---

## Tests incluidos

| Test | Descripción |
|---|---|
| `test_login_exitoso` | Login con credenciales válidas y validación de redirección a `/inventory.html` |
| `test_catalogo_productos` | Verifica título, productos visibles, menú, filtros y datos del primer producto |
| `test_carrito_compras` | Agrega un producto, verifica el contador y comprueba que aparece en el carrito |

---

## Credenciales de prueba

```
Usuario:    standard_user
Contraseña: secret_sauce
```

---

## Evidencias

- El reporte HTML se genera en `reports/reporte.html` al ejecutar los tests.
- Las capturas de pantalla ante fallos se guardan automáticamente en `reports/screenshots/`.
