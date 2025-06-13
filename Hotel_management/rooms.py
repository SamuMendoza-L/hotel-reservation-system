#Clase de las habitaciones
from Hotel_management.employee import requiere_permiso

class Room:
    def __init__(self, number_room, room_type, price):
        self.number_room = number_room
        self.room_type = room_type
        self.price = price
        self.Availability = True


class Rooms_Management:
    def __init__(self):
        self.rooms = []

    def show_rooms_availability(self, type_room):
        type_room = type_room.lower()  # Asignar el resultado de lower()

        print(f'Habitaciones tipo {type_room} disponibles')
        for r in self.rooms:
            if r.room_type.lower() == type_room:
                disponibilidad = self.check_availability(r)
                if isinstance(disponibilidad, bool):  # Verificamos si es un booleano
                    estado = "Disponible" if disponibilidad else "No disponible"
                    print(f"Habitación {r.number_room} - Tipo: {r.room_type}: {estado}")
                else:
                    print(disponibilidad)  # Imprime el mensaje de error


    def change_ava(self, num_room):
        for r in self.rooms:
            if r.number_room == num_room:
                r.Availability = False
                return r.Availability
            
    def add_room(self, room):
        self.rooms.append(room)
        print(f'Habitacion {room.number_room} registrada correctamente')

    def check_availability(self, room):
        for r in self.rooms:
            if r.number_room == room.number_room:
                return room.Availability
            
        return f'La habitación {room.number_room} no esta disponible'
    
    def show_rooms(self):
        print('Habitaciones en el sistema: ')
        for r in self.rooms:
            estado = 'Disponible' if r.Availability else 'No disponible'
            print(f'\nNumero de habitacion: {r.number_room}' + 
                  f'\nTipo de habitación: {r.room_type}' + 
                  f'\nPrecio por noche: {r.price}' +
                  f'\nEstado: {estado}'
                  )
            
    def calculate_amount(self, room_n, days):
        for r in self.rooms:
            if r.number_room == room_n:
                price_nigth = r.price
                return price_nigth * days
    
    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    def habitaciones_dispo(self, rol = None):
        for r in self.rooms:
            if r.Availability == True:
                print(f'\nNumero de habitación: {r.number_room}' +
                      f'\nTipo de habitacion: {r.room_type}' +
                      f'\nCosto por noche: {r.price}')

        

    def data_rooms(self):
        #Funcion donde creo la informacion de las habitaciones
        room1 = Room(101, 'Individual', 500.0)
        room2 = Room(102, 'Individual', 500.0)
        room3 = Room(201, 'Doble', 750.0)
        room4 = Room(202, 'Doble', 750.0)
        room5 = Room(301, 'Suite', 1500.0)
        room6 = Room(302, 'Suite', 1500.0)
        room7 = Room(401, 'Matrimonial', 900.0)
        room8 = Room(402, 'Matrimonial', 900.0)
        room9 = Room(501, 'Familiar', 1200.0)
        room10 = Room(502, 'Familiar', 1200.0)

        #Agregamos las habitaciones a la lista
        self.add_room(room1)
        self.add_room(room2)
        self.add_room(room3)
        self.add_room(room4)
        self.add_room(room5)
        self.add_room(room6)
        self.add_room(room7)
        self.add_room(room8)
        self.add_room(room9)
        self.add_room(room10)

        #Mostramos la informacion
        """ print('')
        self.show_rooms() """





