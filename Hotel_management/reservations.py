#Clase de las reservaciones
import random
import asyncio
from datetime import datetime
from Hotel_management.employee import requiere_permiso

class Reservations:
    def __init__(self, id_re, name_customer, ID_Customer,num_room, date_i, date_f, payment):
        self.id_re = id_re
        self.name_customer = name_customer
        self.ID_Customer = ID_Customer
        self.num_room = num_room
        self.date_i = date_i
        self.date_f = date_f
        self.payment = payment

class Reservations_Management:
    def __init__(self, customer_management, rooms_management, payments_m):
        self.reservations = []
        self.customer_management = customer_management
        self.rooms_management = rooms_management
        self.payments_m = payments_m

    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    async def register_r(self, rol=None):

        #Definimos la variable, para luego pasarla a la funcion add_customer
        rol1 = rol
        
        print('\nVamos a registrar una nueva reserva')

        try:
            id_c = int(input('Identificación del cliente: '))
        except ValueError:
            print("Error: El ID debe ser un número.")
            return

        print('\nBuscando información del cliente...')
        await asyncio.sleep(2)

        cliente_encontrado = None
        for cliente in self.customer_management.customers:
            if cliente.cust_id == id_c:
                cliente_encontrado = cliente
                break

        if cliente_encontrado:
            print(f'\n✅Información del cliente encontrada:' +
                  f'\nNombre: {cliente_encontrado.name}' +
                  f'\nNumero de ID: {cliente_encontrado.cust_id}')
            # Aquí podrías continuar solicitando fechas, número de habitación, etc.
            '''
            Aqui voy a tener que preguntar el tipo de habitacion que buscan, pasarselo a una funcion
            que me filtre la habitaciones por tipo y me devuelva el numero de habitacion que esta disponible
            si por el tipo no hay disponibles entonces que me muestre cuales estan disponibles
            '''

            print(f'\nHaremos la reserva a nombre de {cliente_encontrado.name.capitalize()}' + 
                  '\n\nDatos para la reserva -->' +
                  f'\nNombre cliente: {cliente_encontrado.name}' +
                  f'\nNumero de ID: {cliente_encontrado.cust_id}')

            foud_type_room = input('\n¿Que tipo de habitacion busca?' +
                                   '\n- Individual' +
                                   '\n- Doble' +
                                   '\n- Suite' +
                                   '\n- Matrimonial' +
                                   '\n- Familiar' + 
                                   '\nIngrese una opcion: ').lower()
            
            #Aqui debo crear una funcion en rooms, que me devuelva una lista de las habs dispo por el tipo
            print(f'\nBuscando habitaciones {foud_type_room.capitalize()} disponibles...')
            await asyncio.sleep(2)

            self.rooms_management.show_rooms_availability(foud_type_room)

            room_esp = int(input('Elige el numero de la habitacion: '))

            print(self.rooms_management.change_ava(room_esp))

            # Validar fecha de entrada
            while True:
                fecha_inicio_str = input("Ingrese la fecha de entrada (YYYY-MM-DD): ")
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
                    break
                except ValueError:
                    print("❌ Formato de fecha inválido para la fecha de entrada. Inténtalo de nuevo.\n")

            # Validar fecha de salida
            while True:
                fecha_fin_str = input("Ingrese la fecha de salida (YYYY-MM-DD): ")
                try:
                    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                    if fecha_fin <= fecha_inicio:
                        print("⚠️ La fecha de salida debe ser posterior a la fecha de entrada. Inténtalo de nuevo.\n")
                    else:
                        break
                except ValueError:
                    print("❌ Formato de fecha inválido para la fecha de salida. Inténtalo de nuevo.\n")

            # Confirmación final
            print("✅ Fechas registradas correctamente.")
            print("🗓️ Duración de la estancia:", (fecha_fin - fecha_inicio).days, "días")

            dias = (fecha_fin - fecha_inicio).days

            #Funcion para calcular el costo total de la reserva
            total_price = self.rooms_management.calculate_amount(room_esp, dias)

            print(f"Cantidad total a pagar de la reserva es: {total_price}")

            '''
            Informacion a guardar de la reserva: 
            
            -Nombre del cliente
            -Numeor de hab
            -Tipo de hab
            -Fechas
            -Cantidad de dias
            -Cantidad de pago 
            -El registro del pago
            '''

            name = cliente_encontrado.name
            id_cliente = cliente_encontrado.cust_id
            id_re = random.randint(100, 999)

            reserve = Reservations(id_re, name, id_cliente, room_esp, fecha_inicio, fecha_fin, total_price)

            self.reservations.append(reserve)

            print('-' * 30)
            print('Reservacion exitosa' +
                  '\nDatos de la reserva: ' +
                  f'\nIdentificador de la reserva: {id_re}' +
                  f'\nNombre del cliente: {name}' +
                  '\n\nFelicidades')
        
        else:
            print(f'No se encontró información para el ID: {id_c}')
            '''
            En este caso que no se encuentra el cliente, llamar a la funcion que me permite registrarlo
            '''
            print('Registro del cliente previo al registro de la reserva: ')
            self.customer_management.add_customers(rol = rol1) #Aqui le pasamos el valor de la variable para que acepte el rol
            print(f'Haremos la reserva a nombre del usuario: {id_c}')


    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    def show_reserves(self, rol = None):
        for re in self.reservations:
            print(f'\nID reserva: {re.id_re}' + 
                  f'\nNombre del cliente: {re.name_customer}' +
                  f'\nNumero de habitación: {re.num_room}' + 
                  f'\nPago total de la reserva: {re.payment}')
            
    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    def cancelar_reserva(self, rol = None):
        print('Cancelacion de reservas')

        try:
            id_cliente = int(input('Ingresa el ID del cliente: '))
            
            reservas_encontradas = False
            print('\nReservas encontradas:')
            
            for reserva in self.reservations:
                if id_cliente == int(reserva.ID_Customer):
                    print(f'Numero de la reserva: {reserva.id_re}')
                    print(f'Nombre del cliente: {reserva.name_customer}')
                    print(f'Habitación: {reserva.num_room}')
                    print('-' * 30)
                    reservas_encontradas = True
            
            if not reservas_encontradas:
                print('❌ No se encontraron reservas para este cliente.')

            if reservas_encontradas:
                self.reservations.remove(reserva)
                print('Reserva cancelada')
                
        except ValueError:
            print("❌ Error: El ID debe ser un número.")

























