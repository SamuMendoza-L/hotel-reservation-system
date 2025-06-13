#Clase clientes
from Hotel_management.employee import requiere_permiso

class Customer:
    def __init__(self, cust_id, name, last_name, email, contact_num):
        self.cust_id = cust_id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.contact_num = contact_num

class Customer_management:
    def __init__(self):
        self.customers = []

    #Funcion para agregar clientes

    @requiere_permiso({'Receptionist', 'Administrator'})
    def add_customers(self, rol = None):
        print('\nVamos a registrar un nuevo cliente')
        cust_id = int(input('Ingresa el ID del cliente: '))
        name = input('Nombre del cliente: ')
        last_name = input('Apellido del cliente: ')
        email = input('Email del cliente: ')
        contact_num = input('Numero de contacto: ')

        customer = Customer(cust_id, name, last_name, email,contact_num)
        self.customers.append(customer)

        print(f'\nCliente -{customer.name}- registrado correctamente')

    @requiere_permiso({'Receptionist', 'Administrator', 'Manager'})
    def show_customers(self, rol = None):
        print('Lista de clientes registrados: ')
        for cus in self.customers:
            print(f'\nName: {cus.name}' +
                  f'\nLast name: {cus.last_name}' + 
                  f'\nCustomer ID: {cus.cust_id}'
                  f'\nEmail: {cus.email}' + 
                  f'\nContact number: {cus.contact_num}')
        



        