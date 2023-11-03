from application.config.database import Database


class ClienteDTO():
    def __init__(self, id, nombre, telefono, email):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email


class ClienteDAO():
    def __init__(self):
        # Inicializamos la conexión a la base de datos
        self.db = Database()
        self.mysql = self.db.get_connection()

    def get_all_clientes(self):
        # Obtiene todos los clientes de la base de datos
        cur = self.mysql.connection.cursor()
        cur.execute('''SELECT * FROM cliente''')
        data = cur.fetchall()
        # Mapea los resultados a objetos ClienteDTO y los retorna como una lista
        return [ClienteDTO(*row) for row in data]

    def add_cliente(self, cliente_dto):
        try:
            # Añade un nuevo cliente a la base de datos
            cur = self.mysql.connection.cursor()
            cur.execute('INSERT INTO cliente (nombre, telefono, email) VALUES (%s, %s, %s)',
                        (cliente_dto.nombre, cliente_dto.telefono, cliente_dto.email))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error 001 function add_cliente: {e}")

    def delete_cliente(self, id):
        try:
            # Elimina un cliente de la base de datos por su ID
            cur = self.mysql.connection.cursor()
            sql = f"DELETE FROM cliente WHERE id = {id}"
            cur.execute(sql)
            self.mysql.connection.commit()
            print(cur.rowcount, "record(s) deleted")
            return cur.rowcount
        except Exception as e:
            print(f"Error 002 function delete_cliente: {e}")

    def get_by_id(self, id: int) -> ClienteDTO:
        try:
            # Obtiene un cliente por su ID
            cur = self.mysql.connection.cursor()
            sql = f"SELECT * FROM cliente WHERE id = {id}"
            cur.execute(sql)
            data = cur.fetchone()
            if data:
                # Si se encuentra un cliente, retorna un objeto ClienteDTO
                return ClienteDTO(*data)
            return None
        except Exception as e:
            print(f"Error function get_by_id: {e}")

    def update_cliente(self, cliente_dto):
        try:
            # Actualiza los datos de un cliente en la base de datos
            cur = self.mysql.connection.cursor()
            sql = 'UPDATE cliente SET nombre = %s, telefono = %s, email = %s WHERE id = %s'
            values = (cliente_dto.nombre, cliente_dto.telefono, cliente_dto.email, cliente_dto.id)
            cur.execute(sql, values)
            self.mysql.connection.commit()
            print(cur.rowcount, "record(s) updated")
            return cur.rowcount
        except Exception as e:
            print(f'Error function update_cliente: {e}')


class ServiceLocator():
    def __init__(self):
        # Inicializa el DAO del Cliente
        self.cliente_dao = ClienteDAO()

