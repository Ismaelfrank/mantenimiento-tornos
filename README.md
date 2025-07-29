
# Sistema de Mantenimiento de Tornos 🛠️

Este proyecto es una aplicación de escritorio construida en Python usando `tkinter`, `sqlite3`, y `openpyxl` para el control de mantenimientos preventivos y correctivos de tornos industriales.

## Funcionalidades principales ✅

- Registrar mantenimientos (correctivos o preventivos)
- Consultar historial por torno o por rango de fechas
- Programar mantenimientos futuros
- Generar alertas automáticas para mantenimientos próximos (30 días)
- Enviar alertas por correo electrónico (Gmail)
- Guardar automáticamente en una base de datos SQLite y un archivo Excel

## Tecnologías usadas 🧠

- Python 3
- Tkinter (Interfaz gráfica)
- SQLite (Base de datos)
- OpenPyXL (Manejo de Excel)
- SMTPLib / EmailMessage (Envío de correos)

## Estructura del proyecto 📁

```
sistema_mantenimiento_con_alertas.py   # Script principal
funcion_envio_alertas.py               # (Opcional si se separa)
mantenimientos.xlsx                    # Archivo Excel generado automáticamente
mantenimiento_torno.db                 # Base de datos SQLite
.gitignore                             # Archivos que Git no sube
README.md                              # Este archivo
```

## Configuración del correo ✉️

- El sistema usa un correo Gmail con contraseña de aplicación
- El envío de alertas se hace automáticamente si hay mantenimientos programados próximos
- Puedes cambiar los destinatarios en el código

## Cómo ejecutar 🚀

1. Asegúrate de tener Python instalado
2. Instala dependencias (si no las tienes):
   ```
   pip install openpyxl
   ```
3. Ejecuta el script:
   ```
   python sistema_mantenimiento_con_alertas.py
   ```

## Cómo subir a GitHub 🌐

1. Crea un repositorio en GitHub
2. Ejecuta esto desde la terminal:

```
git init
git add .
git commit -m "Primer commit del sistema de mantenimiento"
git remote add origin https://github.com/tuusuario/tu-repo.git
git branch -M main
git push -u origin main
```

¡Listo! 🎉

## Autor

Ismael Paillacho
