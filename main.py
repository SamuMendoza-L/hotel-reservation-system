import asyncio
from Hotel_management.employee import Employee_Management #Aqui importo la clase de los empleados
from Hotel_management.customers import Customer_management #Aqui importo la clase de los empleados
from Hotel_management.rooms import Rooms_Management
from Hotel_management.reservations import Reservations_Management
from Hotel_management.payments import Payments_Management



async def main ():

    #Iniciar sistemas
    emp_management = Employee_Management()
    cust_management = Customer_management()
    room_management = Rooms_Management()

    # Crear instancia de payments sin reservations inicialmente
    payments_management = Payments_Management(cust_management, emp_management, None)

    # Crear reservations con payments
    reservations_mng = Reservations_Management(cust_management, room_management, payments_management)

    # Actualizar la referencia de reservations en payments
    payments_management.set_reservations(reservations_mng)

    #Crear informacion para el sistema
    print('')
    emp_management.data_employees()
    print('')
    room_management.data_rooms()


    while True:
        print('\nMostrar la informacion de sistema? ' +
              '\nSi'
              '\nNo')
        
        opt = input('Ingresa una opcion: ').lower()

        if opt == 'si':
            #Funcion que crea la informacion de los empleados
            emp_management.show_employees()

            #Funcion para crear la informacion de las habitaciones
            print('')
            room_management.show_rooms()

            print('Mostrando menu principal...')
            break
            
        elif opt == 'no':
            print('Mostrando menu principal...')
            break
              
    #Validacio de credenciales
    key_employe = int(input('\nInserta tu llave de acceso para mostrar el menu: '))
    emp_management.check_access(key_employe) #Aqui llamo la función que valida la informacion del trabajador

    #En esta variable estoy guardando el rol del empleado que ingresa al sitema
    emp_role = emp_management.check_role(key_employe) 
    print(f'User role: {emp_role}')

    print('\nSistema del Hotel')
    while True:
        print('\nMenu' +
              '\n1. Registrar nuevo cliente' +
              '\n2. Lista de clientes registrados' +
              '\n3. Crear nueva reserva' +
              '\n4. Cancelar una reserva' +
              '\n5. Ver habitaciones disponibles' +
              '\n6. Procesar pago de una reserva' +
              '\n7. Ver historial de pagos' +
              '\n8. Ver reservas activas' +
              '\n9. Generar reporte mensual' + 
              '\n10. salir')
        
        option = int(input('Ingresa un numeral del menu: '))

        if option == 1:
            cust_management.add_customers(rol=emp_role)

        elif option == 2:
            cust_management.show_customers(rol=emp_role)

        elif option == 3:
            """ reservations_mng.register_r(rol=emp_role) """
            await reservations_mng.register_r(rol= emp_role)

        elif option == 4:
                
                reservations_mng.cancelar_reserva(rol = emp_role)

        elif option == 5:
                print('\nHabitaciones disponibles')
                room_management.habitaciones_dispo(rol = emp_role)

        elif option == 6:
                print('\nProcesando pago...')
                payments_management.procesar_pago(rol=emp_role)
            
        elif option == 7:
                print('\nHistorial de pagos')
                payments_management.mostrar_pagos(rol = emp_role)

        elif option == 8:
                print('\nReservas activas')
                reservations_mng.show_reserves(rol = emp_role)

        elif option == 9:
                print('\nGenerando informe mensual')
            
        elif option == 10:
                print('Saliendo del sistema...')
                break
                
        else:
                print('Opcion no valida')
    
                
if __name__ == "__main__":
    asyncio.run(main())
