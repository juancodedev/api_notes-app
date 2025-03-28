# API Notes App

Este proyecto es una API para gestionar notas y etiquetas, desarrollada con **FastAPI** y **SQLAlchemy**. A continuación, se detallan las instrucciones para configurar y ejecutar el proyecto localmente, las tecnologías utilizadas y un apartado para justificar la elección de cada una.

---

## Tecnologías utilizadas

- **Python**: Lenguaje de programación principal.
- **FastAPI**: Framework para construir APIs rápidas y eficientes.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **Alembic**: Herramienta para gestionar migraciones de base de datos.
- **PostgreSQL**: Base de datos relacional utilizada.
- **Pydantic**: Validación de datos y creación de esquemas.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.
- **Pytest**: Framework de pruebas para garantizar la calidad del código.

---

## Configuración del proyecto

### Prerrequisitos

1. **Python 3.10 o superior**: Asegúrate de tener instalado Python en tu máquina.
2. **PostgreSQL**: Instala y configura PostgreSQL como base de datos.
3. **Virtualenv (opcional)**: Para crear un entorno virtual y aislar las dependencias del proyecto.

### Pasos para configurar

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/juancodedev/api_notes-app.git
   cd api_notes-app

2. **Crear un entorno virtual (opcional)**:
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
3. **Instalar dependencias**
    pip install -r requirements.txt

4. **Configurar variables de entorno**
    Crea un archivo .env en la raíz del proyecto con las siguientes variables

        DB_URL=postgresql://usuario:contraseña@localhost:5432/notes_app
=SECRET_KEYtu_clave_secreta
5. **Crear la base de datos**
    Crear la base de datos en PostgreSQL
        
        CREATE DATABASE notes_app;

    Aplicar las migraciones:
        
        alembic upgrade head
6. **Ejecutar la aplicación**
    ejecutamos el comando para iniciar el servidor local

    fastapi run dev

7. **Probar la API**

    La API estará disponible en: http://localhost:8000
    La documentación interactiva estará en: http://localhost:8000/docs


**Razones para elegir las tecnologias/frameworks**
*   **FastAPI**: Es un framework de Python que me permite crear APIs de alta velocidad y escalabilidad, ademas cuenta con soporte nativo para la documentacion interactiva con Swagger y OpenAPI.
*   **Alembic**: Para facilitar la gestion de las migraciones de los esquemas de datos de la base de datos.
*   **PostgreSQL**: Base de datos relacional confiable y con características avanzadas y con soporte para JSON.
*   **Python**: Lenguaje de programación versatil y con una gran cantidad de documentacion diponible.
*   **SQLAlchemy**: Proporciona un ORM robusto y flexible para interactuar con bases de datos relacionales y su compatibilidad con varios motores de base de datos como PostgreSQL.
*  **Pytest**: Framework de pruebas sencillo y extensible para garantizar la calidad del código.

**Estrategia de bloqueo**
*   **Bloqueo de la base de datos de forma pesimista**: Para evitar que multiples transacciones se ejecucion, lo cual me permite el poder mantener la integridad de datos, donde se bloquea el registro en la base de datos mientras lo estoy trabajando, evitando que otro usaurio pueda acceder a el mismo registro, evitando sobre escrituras o perdida de información.

**Desafios enfrentados**
* **FastAPI**: fue una herramienta de la cual tuve que aprender mucho, ya que la conocia, pero nunca la había utilizado en un proyecto real, por lo que tuve que investigar y aprender sobre su funcionamiento, configuración e implementacion.
* **Problemas de concurrencia**: Nunca habia trabajado con esta dinamica en la integridad de los datos, por lo que investigue y aprendi sobre los diferentes tipos de bloqueo y como implementarlos en este proyecto, si bien no lo logré completar, aprendi mucho de la experiencia.




**Licencia**
    ste proyecto está bajo la licencia MIT.
