# 📝 Blog Backend con Django

Proyecto de **aplicación web tipo blog** desarrollado con **Django** y **PostgreSQL**, enfocado en buenas prácticas de backend, modelado de datos y búsquedas avanzadas a nivel base de datos.

---

## 🎯 Objetivo del proyecto

Demostrar conocimientos sólidos en:

* Desarrollo backend con Django
* Integración con PostgreSQL
* Uso de búsquedas avanzadas a nivel SQL
* Organización de proyectos y buenas prácticas
* Manejo de datos, migraciones y fixtures

---

## 🚀 Funcionalidades

* Publicación de posts con estados (borrador / publicado)
* Sistema de etiquetas (tags)
* Comentarios asociados a los posts
* Búsqueda avanzada de contenido:

  * Full Text Search nativo de PostgreSQL
  * Ranking de relevancia por campo
  * Trigram similarity para coincidencias aproximadas
* Paginación de resultados
* Panel de administración personalizado

---

## 🛠️ Tecnologías utilizadas

* **Python 3.12**
* **Django 5**
* **PostgreSQL**
* **Docker** (opcional para la base de datos)
* **HTML / CSS**
* **django-taggit**
* **psycopg**

---

## 🔍 Búsqueda avanzada (PostgreSQL)

El sistema de búsqueda no depende únicamente del ORM tradicional de Django.

Se implementa:

* **SearchVector** con pesos distintos por campo

  * Título → mayor relevancia
  * Cuerpo → relevancia secundaria
* **SearchRank** para ordenar resultados según coincidencia
* **Trigram similarity (`pg_trgm`)** para mejorar búsquedas con errores de tipeo

Esto permite búsquedas más precisas, eficientes y escalables.

---

## ⚙️ Instalación

```bash
git clone https://github.com/Yamila-Navas/blog.git
cd tu-repo
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📦 Base de datos

* Motor: PostgreSQL
* Soporte para extensiones (`pg_trgm`)
* Backups vía `pg_dump`
* Opción de ejecución mediante contenedor Docker

---

## 🧠 Aprendizajes clave

* Diseño de modelos relacionales
* Uso avanzado de PostgreSQL desde Django
* Optimización de búsquedas
* Manejo de migraciones y datos
* Separación de responsabilidades en el proyecto
