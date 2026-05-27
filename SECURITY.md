# Respuestas de Seguridad - Laboratorio 4
**Desarrollador:** Jose Manuel Zamora Loor
**Aplicación:** Rastreador de Incidentes Cibernéticos en Django

---

## Pregunta de Seguridad 0
**Antes de añadir autenticación: visita /incidents/ en un navegador en modo incógnito. ¿Qué ves? Escribe una oración explicando por qué esto es un problema de seguridad para un sistema real de gestión de incidentes.**
Al acceder de forma incógnita, veo el listado completo de todos los incidentes registrados. Esto representa un problema de seguridad crítico porque, en un entorno real, estaríamos exponiendo las vulnerabilidades internas de nuestra infraestructura a internet; un atacante podría utilizar esta información para saber exactamente dónde y cómo atacar nuestros sistemas.

---

## Pregunta de Seguridad 1
**¿Cuál es la diferencia entre el modelo `User` integrado de Django y tu modelo `UserProfile`? ¿Por qué usar un `OneToOneField` en lugar de agregar campos directamente al modelo `User`?**
El modelo `User` integrado de Django maneja exclusivamente el núcleo de la autenticación, almacenando credenciales básicas como el nombre de usuario, el correo electrónico y la contraseña cifrada. Nuestro modelo `UserProfile` es una extensión que almacena información específica del negocio, en este caso, el `role` (Administrador o Analista). 
Se utiliza un `OneToOneField` porque permite relacionar nuestro perfil personalizado con el usuario de forma exclusiva sin tener que alterar el código fuente del framework de Django. Modificar directamente el modelo `User` es una mala práctica que puede romper compatibilidades con otras librerías y dificultar futuras actualizaciones del sistema.

---

## Pregunta de Seguridad 2
**¿Cuál es el propósito del parámetro `?next=` en la redirección de inicio de sesión? ¿Qué vulnerabilidad de seguridad podría surgir si Django no validara la URL `next` antes de redirigir?**
El parámetro `?next=` funciona como un marcador de memoria; su propósito es guardar la ruta a la que el usuario intentaba acceder (por ejemplo, `/incidents/new/`) antes de ser interceptado por la pantalla de login, para devolverlo allí automáticamente una vez que ingrese sus credenciales con éxito. 
Si Django no validara esta URL, el sistema sería vulnerable a un ataque de **Redirección Abierta (Open Redirect)**. Un atacante podría enviar un enlace engañoso a un empleado como `misitio.com/login/?next=http://sitio-falso-del-atacante.com`. El usuario iniciaría sesión en el sistema real, pero sería redirigido a una página clonada para robarle datos.

---

## Pregunta de Seguridad 3
**¿Cuál es la diferencia entre autenticación y autorización? Proporciona un ejemplo concreto de este laboratorio donde se apliquen ambas. ¿Qué sucede si implementas autenticación pero omites la autorización?**
* La **Autenticación** es el proceso de verificar *quién* es el usuario (comprobar que la contraseña sea correcta).
* La **Autorización** es el proceso de verificar *qué* permisos tiene ese usuario dentro del sistema.
* **Ejemplo en el laboratorio:** Cuando usamos el decorador `@login_required` sobre la vista `delete`, estamos aplicando autenticación. Cuando verificamos `if not profile.is_admin():`, estamos aplicando autorización.
Si implementamos autenticación pero omitimos la autorización, cualquier persona que logre crear una cuenta básica (como un Analista recién registrado) tendría el poder de eliminar la base de datos entera de incidentes, ya que el sistema sabría quién es, pero no limitaría sus acciones.

---

## Pregunta de Seguridad 4
**¿Por qué usamos `commit=False` antes de asignar `reported_by`? ¿Qué pasaría si permitiéramos a los usuarios enviar manualmente el campo `reported_by` a través de un campo de formulario oculto? ¿A qué ataque se relaciona esto?**
Usamos `commit=False` para generar el objeto en memoria a partir de los datos del formulario, pero deteniendo temporalmente su guardado en la base de datos. Esto nos permite asignar internamente y de forma segura el usuario actual (`request.user`) desde el backend antes de realizar el guardado final.
Si permitiéramos que este dato llegara desde un formulario (incluso uno oculto con `type="hidden"`), un usuario malicioso podría inspeccionar el código HTML en su navegador, cambiar el ID del usuario, y crear incidentes falsos haciéndose pasar por un Administrador. Esto se conoce como un ataque de **Asignación Masiva (Mass Assignment)** o Inyección de Parámetros.

---

## Pregunta de Seguridad 5
**Ocultamos los botones de Editar y Eliminar a los Analistas en la plantilla, pero también añadimos el `@login_required` y la comprobación de rol en la vista. ¿Por qué NO es suficiente con solo ocultar los botones en la plantilla? ¿Qué ataque elude la ocultación a nivel de plantilla?**
Ocultar botones mediante condicionales `{% if %}` en el HTML es únicamente una mejora en la interfaz de usuario (Frontend), no una medida de seguridad. Si no protegemos la vista en el backend, un atacante no necesita ver el botón; simplemente puede adivinar la URL (por ejemplo, escribiendo directamente `http://127.0.0.1:8000/incidents/1/delete/` en el navegador) o usar herramientas como cURL/Postman para enviar la petición HTTP de borrado. 
Este ataque se conoce como **Insecure Direct Object Reference (IDOR)** o **Bypass de Control de Acceso (Access Control Bypass)**.

---

## Pregunta de Seguridad 6 (Bonus)
**¿Qué es un ataque de fuerza bruta en un formulario de inicio de sesión? ¿Cómo lo mitiga django-axes? ¿Cuál es la desventaja de establecer `AXES_FAILURE_LIMIT` demasiado bajo? Nombra otro método para proteger un punto final de inicio de sesión más allá de la limitación de velocidad.**
* Un **ataque de fuerza bruta** ocurre cuando un atacante usa scripts automatizados para probar miles de combinaciones de contraseñas por segundo contra una cuenta hasta adivinar la correcta.
* `django-axes` lo mitiga llevando un registro de los intentos fallidos asociados a una dirección IP o nombre de usuario, bloqueando el acceso a esa cuenta temporalmente al sobrepasar un límite.
* Si el límite (`AXES_FAILURE_LIMIT`) se establece demasiado bajo (por ejemplo, en 2), la desventaja es que los usuarios legítimos bloquearán sus propias cuentas accidentalmente con mucha frecuencia por simples errores tipográficos.
* Otro método robusto para proteger el inicio de sesión es implementar **Autenticación Multifactor (MFA / 2FA)**, que exige un código de un dispositivo móvil además de la contraseña, o el uso de **CAPTCHAs** para bloquear los scripts automatizados.