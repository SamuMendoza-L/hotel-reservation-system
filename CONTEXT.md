# Contexto del Proyecto: Hotel Reservation System

## Resumen breve
Este repositorio implementa un sistema simple de gestión de hotel escrito en Python (100% del código). Está organizado como un paquete `Hotel_management` con módulos que modelan empleados, clientes, habitaciones, reservas y pagos, y un script `main.py` que orquesta la interacción por consola.

Recomendado: Python 3.8+ (se usan datetimes, asyncio y funciones modernas). No hay dependencias externas (solo la librería estándar).

---

## Estructura del repositorio

- main.py
- README.md
- Hotel_management/
  - __init__.py
  - customers.py
  - employee.py
  - rooms.py
  - reservations.py
  - payments.py
  - (otros archivos de workspace / __pycache__)

---

## Propósito y flujo general

El script `main.py` crea instancias de los gestores (Employee_Management, Customer_management, Rooms_Management, Payments_Management, Reservations_Management) y ofrece un menú por consola para: registrar clientes, ver clientes, crear/cancelar reservas, ver habitaciones disponibles, procesar pagos y ver historiales.

Flujo principal de interacción:
1. Se inicializan datos de empleados y habitaciones mediante `data_employees()` y `data_rooms()`.
2. El usuario ingresa su "llave" (user_id) y el sistema determina el rol del empleado con `check_role`.
3. Según el rol y la opción del menú, se llaman métodos con control de permisos (decorador `requiere_permiso`) para ejecutar acciones.
4. Las reservas se registran (async) en `Reservations_Management.register_r` y generan entradas en las listas internas. Los pagos se registran en `Payments_Management.payments` y referencian reservas.

---

## Módulos y clases (detallado)

A continuación se listan las clases y métodos más importantes, con su firma y comportamiento observado.

1) Hotel_management.employee

- Clase: Employee
  - __init__(self, name, rol, user_id)
    - Atributos: name (str), rol (str), user_id (int)

- Clase: Employee_Management
  - __init__(self)
    - Atributo: employess (list[Employee]) — nota: nombre de atributo contiene un typo (employess vs employees)
  - add_employee(self, employee)
    - Añade un objeto Employee a la lista. Imprime confirmación.
  - show_employees(self)
    - Imprime los empleados registrados.
  - check_access(self, user_id)
    - Recorre empleados y si el user_id coincide imprime aceptación y usuario.
    - No devuelve booleano; solo imprime.
  - check_role(self, user_id) -> str | mensaje
    - Recorre empleados y devuelve el rol si encuentra el user_id.
    - Si no encuentra, devuelve un string con mensaje "Usuario -{user_id}- no encontrado".
  - data_employees(self)
    - Crea 5 empleados por defecto y los agrega (Samuel, Ana, Esteban, Sebastian, Elena) con roles variados.

- Decorador: requiere_permiso(roles_permitidos)
  - Implementación: función que retorna un decorador. El wrapper lee el argumento `rol` de kwargs (kwargs.get('rol')).
  - Si el rol está en roles_permitidos, ejecuta la función; si no, imprime mensaje de acceso denegado.
  - Observaciones:
    - Supone que las funciones decoradas reciben el rol como keyword argument `rol`.
    - No lanza excepción, solo imprime y termina. No devuelve un valor por defecto cuando se niega.


2) Hotel_management.customers

- Clase: Customer
  - __init__(self, cust_id, name, last_name, email, contact_num)
    - Atributos: cust_id (int), name, last_name, email, contact_num

- Clase: Customer_management
  - __init__(self): self.customers = []
  - add_customers(self, rol = None)
    - Decorado con `@requiere_permiso({'Receptionist', 'Administrator'})`.
    - Pide por consola: ID, nombre, apellido, email, teléfono; crea Customer y lo añade a la lista.
  - show_customers(self, rol = None)
    - Decorado con `@requiere_permiso({'Receptionist', 'Administrator', 'Manager'})`.
    - Imprime la lista de clientes registrados.

Observaciones: el decorador requiere que el `rol` se pase como keyword en las llamadas (ej.: add_customers(rol=emp_role)).


3) Hotel_management/rooms

- Clase: Room
  - __init__(self, number_room, room_type, price)
    - Atributos: number_room (int), room_type (str), price (float), Availability (bool por defecto True)

- Clase: Rooms_Management
  - __init__(self): self.rooms = []
  - show_rooms_availability(self, type_room)
    - Convierte `type_room` a lower(), recorre habitaciones y muestra estado (Disponible/No disponible) para las del mismo tipo.
    - Maneja si check_availability devuelve un mensaje de error o booleano.
  - change_ava(self, num_room)
    - Marca Availability = False para la habitación con number_room == num_room y devuelve el nuevo estado.
    - No marca la habitación de vuelta a True (es decir, no hay check-in/out explícito para liberar la habitación).
  - add_room(self, room)
    - Agrega un Room a la lista.
  - check_availability(self, room)
    - Busca la habitación por número y retorna room.Availability o un mensaje si no existe.
  - show_rooms(self)
    - Imprime todas las habitaciones y su estado.
  - calculate_amount(self, room_n, days)
    - Busca la habitación por número y retorna price * days
  - habitaciones_dispo(self, rol = None)
    - Decorado con `@requiere_permiso({'Receptionist', 'Administrator', 'Manager'})`.
    - Imprime habitaciones con Availability == True.
  - data_rooms(self)
    - Crea 10 habitaciones de ejemplo (Individual, Doble, Suite, Matrimonial, Familiar) y las agrega.

Observaciones:
- El nombre del atributo `Availability` comienza con mayúscula; convención PEP8 sugiere snake_case (availability).
- La función change_ava marca la habitación como no disponible permanentemente (no hay método para revertir disponibilidad).


4) Hotel_management/reservations

- Clase: Reservations
  - __init__(self, id_re, name_customer, ID_Customer, num_room, date_i, date_f, payment)
    - Atributos que describen una reserva.

- Clase: Reservations_Management
  - __init__(self, customer_management, rooms_management, payments_m)
    - Atributos: reservations (lista), referencias a customer_management, rooms_management, payments_m
  - register_r(self, rol=None)  (async)
    - Decorado con `@requiere_permiso({'Receptionist', 'Administrator', 'Manager'})`.
    - Flujo:
      - Pide ID del cliente; si no existe, llama a customer_management.add_customers(rol=rol) para crearlo.
      - Muestra info del cliente si se encuentra.
      - Pregunta tipo de habitación, muestra habitaciones disponibles por tipo y pide número elegido.
      - Marca la habitación como no disponible con rooms_management.change_ava(room_esp).
      - Pide fechas de entrada y salida (Valida formatos YYYY-MM-DD y que la salida sea posterior a la entrada).
      - Calcula días y total con rooms_management.calculate_amount(room_esp, dias).
      - Crea un objeto Reservations con id aleatorio y lo agrega a self.reservations.
    - Observaciones:
      - Es `async` porque usa `await asyncio.sleep(...)` para simular búsqueda.
  - show_reserves(self, rol = None)
    - Imprime reservas activas.
  - cancelar_reserva(self, rol = None)
    - Pide ID de cliente, lista reservas coincidentes y las muestra. Si encuentra reservas, hace `self.reservations.remove(reserva)` y anuncia cancelación.
    - Posible bug: la variable `reserva` usada en remove puede corresponder solo a la última iteración del for; si hay múltiples reservas, la lógica de eliminación / selección no separa cuál eliminar (falta pedir número de reserva o confirmar cuál eliminar).


5) Hotel_management/payments

- Clase: Payments
  - __init__(self, name_customer, id_payment, amount, id_reserve)
    - Atributos: name_customer, id_payment, amount, id_reserve

- Clase: Payments_Management
  - __init__(self, customers_m, employees_m, reservations=None)
    - Atributos: referencias a managers, self.payments = []
  - set_reservations(self, reservations)
    - Guarda referencia al Reservations_Management (usado desde main para inyectar dependencia circular)
  - procesar_pago(self, rol = None)
    - Decorado con `@requiere_permiso({'Receptionist', 'Administrator', 'Manager'})`.
    - Pide id_reserva, busca en self.reservations.reservations, extrae información y crea un Payments con id aleatorio que añade a self.payments.
    - No valida que la reserva exista antes de crear el pago (aunque sí hace búsqueda; si no encuentra, `reserva_encontrada` sería None y el acceso a atributos fallaría). En el código actual asume que encontró la reserva.
  - mostrar_pagos(self, rol = None)
    - Imprime pagoss registrados.

Observaciones:
- El constructor de Payments_Management acepta `reservations=None` y en main se crea primero Payments_Management sin reservations; luego se crea Reservations_Management y se llama a payments_management.set_reservations(reservations_m) (manejo de dependencia circular correcto).

---

## Puntos importantes / detalles de implementación

- Lenguaje: Python (100%). Se recomienda indicar en el README que requiere Python 3.8+.
- No hay requisitos externos (requirements.txt). Todo usa la librería estándar: asyncio, datetime, random.
- Control de permisos: se implementó con un decorador `requiere_permiso` que comprueba el `rol` pasado por keyword argument `rol`. Si no se pasa `rol` o no coincide, la acción se deniega con un mensaje impreso.
- Asincronía: Solo `Reservations_Management.register_r` es async y usa `await asyncio.sleep(...)` para simular demora.
- Entrada/Salida por consola: la aplicación es interactiva por CLI (input/print). No hay interfaz web ni persistencia (datos en memoria solo durante ejecución).
- IDs: reservas y pagos usan `random.randint` para generar identificadores; para producción se sugiere un generador determinista/único o UUID.


## Casos de uso y ejemplo de ejecución

1. Ejecutar:
   - python main.py
2. Se muestran datos base de empleados y habitaciones.
3. Introducir llave de acceso (por ejemplo 10050 para Receptionist) — rol devuelto por check_role.
4. Usar opciones de menú para: registrar cliente (1), crear reserva (3), procesar pago (6), etc.


## Problemas conocidos y recomendaciones (mejoras sugeridas)

- Validaciones insuficientes:
  - Algunas funciones asumen que la búsqueda de reserva/cliente devuelve resultados; si es None, el código puede lanzar AttributeError (por ejemplo en payments.procesar_pago si no encuentra la reserva).
  - cancelar_reserva no solicita cuál reserva eliminar si hay varias; solo elimina la última encontrada en la iteración.

- Consistencia y estilo PEP8:
  - Atributos con mayúscula (`Availability`) y nombres con typo (`employess`) deberían corregirse.
  - Nombres de clases deberían seguir CapWords (ya lo hacen), funciones y variables en snake_case.

- Persistencia:
  - Actualmente los datos viven en memoria. Agregar persistencia (SQLite, JSON o un ORM ligero) mejoraría el proyecto.

- Manejo de fechas y zonas:
  - Se usan objetos datetime sin zona horaria; para producción considerar timezone-aware datetimes.

- Manejo de disponibilidad:
  - No existe una operación para volver a marcar una habitación como disponible (checkout).
  - Cambiar change_ava para aceptar un flag o crear métodos check_in/check_out.

- Generación de IDs:
  - Usar UUID o secuencia persistente en lugar de random.randint para evitar colisiones.

- Tests unitarios:
  - Agregar pruebas unitarias para cada gestor: customers, rooms, reservations, payments y el decorador de permisos.


## Extensiones y próximos pasos sugeridos

- Añadir persistencia con SQLite y modelar entidades con dataclasses o un pequeño ORM.
- Implementar una API REST (Flask/FastAPI) para separar la lógica de presentación de CLI.
- Añadir logging en lugar de prints y mejor manejo de errores con excepciones.
- Añadir un conjunto de pruebas automatizadas (pytest).
- Mejorar la UX de cancelación de reservas y gestión de disponibilidad (confirmaciones, listado numerado, selección granular).

---

## Glosario rápido de relaciones entre componentes

- main.py crea y coordina:
  - Employee_Management (datos y validación de rol)
  - Customer_management (clientes)
  - Rooms_Management (habitaciones y cálculo de precios)
  - Payments_Management (registra pagos; depende de Reservations)
  - Reservations_Management (registra reservas; depende de Customers y Rooms y usa Payments)

- Relación circular gestionada:
  - Payments_Management se inicializa sin la referencia a Reservations_Management y luego main llama `payments_management.set_reservations(reservations_m)` para inyectarla.

---

## Archivo creado
He generado este archivo de contexto y documentación para que sirva como referencia completa del proyecto.

---

### Notas del autor (assistant)
- Si quieres, puedo:
  - Crear una versión mejorada del README.md con instrucciones de instalación y ejecución en español o inglés.
  - Añadir ejemplos de uso con datos de prueba o scripts no interactivos para probar la lógica.
  - Abrir issues automáticos con las recomendaciones más urgentes (typos, bugs en cancelar_reserva, validación en payments.procesar_pago).

