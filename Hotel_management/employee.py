#Trabajadores del hotel

class Employee:
    def __init__(self, name, rol, user_id):
        self.name = name
        self.rol = rol
        self.user_id = user_id

class Employee_Management:

    def __init__(self):
        self.employess = []

    #Funcion para agregar los empleados al sistema
    def add_employee(self, employee):
        self.employess.append(employee)
        print(f'Trabajador {employee.name} registrado en el sistema')

    #Funcion para mostrar los trabja
    def show_employees(self):
        print('Trabajadores registrados')
        for emp in self.employess:
            print(f'Name: {emp.name} - Rol: {emp.rol} - ID: {emp.user_id}')

    #Funcion para validar la llave de acceso
    def check_access(self, user_id):
        for emp in self.employess:
            if user_id == emp.user_id:
                print('\nLLave de acceso aceptada' + 
                      f'\nUsuario: {emp.name}')
                
    #Funcion para retornar el rol del empleado ingresado
    def check_role(self, user_id):
        for emp in self.employess:
            if user_id == emp.user_id:
                return emp.rol
            
        return f'Usuario -{user_id}- no encontrado'
    
    #Funcion con la informacion base
    def data_employees(self):
        #Aqui voy a crear los trabajadores
        employee1 = Employee('Samuel', 'Receptionist', 10050)
        employee2 = Employee('Ana', 'Manager', 10060)
        employee3 = Employee('Esteban', 'Administrator', 10070)
        employee4 = Employee('Sebastian', 'Cleanliness', 10080)
        employee5 = Employee('Elena', 'Counter', 10090)

        #Aqui voy a guardar los trabajadores en la lista
        self.add_employee(employee1)
        self.add_employee(employee2)
        self.add_employee(employee3)
        self.add_employee(employee4)
        self.add_employee(employee5)  
    
#Decorador para la validacion de los roles
def requiere_permiso(roles_permitidos):
    def decorador(func):
        def wrapper(*args, **kwargs):
            rol_empleado = kwargs.get('rol')
            if rol_empleado in roles_permitidos:
               return func(*args, **kwargs)
            else:
                print(f"\n❌ Acceso denegado: El rol '{rol_empleado}' no tiene permiso para ejecutar esta acción.")
        return wrapper
    return decorador
            

            
                

        



        

        
        

        