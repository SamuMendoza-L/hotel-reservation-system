#Clase donde se reciben los pagos y se registran en una lista

import asyncio
import random
from datetime import datetime
from Hotel_management.employee import requiere_permiso


class Payments:
    def __init__(self, name_customer, id_payment, amount, id_reserve):
        self.name_customer = name_customer
        self.id_payment = id_payment
        self.amount = amount
        self.id_reserve = id_reserve

class Payments_Management:
    def __init__(self, customers_m, employees_m, reservations=None):
        self.customers_m = customers_m
        self.employees_m = employees_m
        self.reservations = reservations
        self.payments = []

    def set_reservations(self, reservations):
        self.reservations = reservations



    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    def procesar_pago(self, rol = None): 
        id_reserva = int(input('Ingresa el identificador de la reserva: '))

        reserva_encontrada = None
        for reserva in self.reservations.reservations:
            if reserva.id_re == id_reserva:
                reserva_encontrada = reserva
                break

        if reserva_encontrada:
            print('\n✅Información de la reseva encontrada: ')
            id_cliente = reserva_encontrada.ID_Customer
            nombre_cliente = reserva_encontrada.name_customer
            numero_hab = reserva_encontrada.num_room
            cantidad_pago = reserva_encontrada.payment

            print(f'\nNombre del cliente: {nombre_cliente}' +
                  f'\nIdentificación del cliente: {id_cliente}' +
                  f'\nNumero de la habitacion: {numero_hab}' +
                  f'\nMonto total: {cantidad_pago}')
            
        id_pago = random.randint(1011, 9999)
        id_re = reserva_encontrada.id_re
            
        payment = Payments(nombre_cliente, id_pago, cantidad_pago, id_re)
        self.payments.append(payment)

        print(f'El pago a nombre de {nombre_cliente} fue registrado correctamente' +
              f'\npor la cantidad de {cantidad_pago}' +
              f'Numero de referencia de pago: {id_pago}')
        
    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    def mostrar_pagos(self, rol = None):
        for p in self.payments:
            print(f'\nNumero de pago: {p.id_payment}' +
                  f'\nNombre del cliente: {p.name_customer}' +
                  f'\nNumero de la reserva: {p.id_reserve}' +
                  f'\nMonto total: {p.amount}')
            



    









