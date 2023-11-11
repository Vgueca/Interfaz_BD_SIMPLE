
import pyodbc

class AccesoBD:
    def __init__(self, server, db_name, user, password):
        self.server = server
        self.db_name = db_name
        self.user = user
        self.password = password
        connection_string = 'driver={Devart ODBC Driver for Oracle};Direct=True;Host=' + self.server + ';Service Name=' + self.db_name + ';uid=' + self.user + ';pwd=' + self.password
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def crear_tabla(self, nombre_tabla, columnas):
        if self.existe_tabla(nombre_tabla):
            return False
        
        columnas = ', '.join(columnas)
        sentenciaSQL = f"CREATE TABLE {nombre_tabla} ({columnas})"
        print(sentenciaSQL)
        self.cursor.execute(sentenciaSQL)
        self.connection.commit()

        return True

    def borrar_tabla(self, nombre_tabla):
        if not self.existe_tabla(nombre_tabla):
            return False
        
        sentenciaSQL = f"DROP TABLE {nombre_tabla}"
        self.cursor.execute(sentenciaSQL)
        self.connection.commit()

        return True

    def existe_tabla(self, nombre_tabla):
        sentenciaSQL = f"SELECT * FROM {nombre_tabla}"
        try:
            self.cursor.execute(sentenciaSQL)
            return True
        except:
            return False

    def insertar_datos(self, nombre_tabla, datos):
        columnas = ', '.join(datos.keys())
        valores = ', '.join(datos.values())
        sentenciaSQL = f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores})"
        print(sentenciaSQL)
        self.cursor.execute(sentenciaSQL)
        #self.connection.commit()

    def borrar_datos(self, nombre_tabla, condicion):
        sentenciaSQL = f"DELETE FROM {nombre_tabla} WHERE {condicion}"
        self.cursor.execute(sentenciaSQL)
        #self.connection.commit()

    def buscar_datos(self, nombre_tabla, columnas, condicion=None):
        columnas = ', '.join(columnas)
        sentenciaSQL = f"SELECT {columnas} FROM {nombre_tabla}"
        if condicion:
            sentenciaSQL += f" WHERE {condicion}"
        self.cursor.execute(sentenciaSQL)
        return self.cursor.fetchall()
    
    def modificar_datos(self, nombre_tabla, columnas, datos, condicion):
        columnas = ', '.join([f"{columna} = {dato}" for columna, dato in zip(columnas, datos)])
        sentenciaSQL = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condicion}"
        self.cursor.execute(sentenciaSQL)
        #self.connection.commit()
    
    def execute(self, sentenciaSQL):
        self.cursor.execute(sentenciaSQL)
        #self.connection.commit()
        return self.cursor.fetchall()
    
    def guardar_savepoint(self, nombre_savepoint):
        self.cursor.execute(f"SAVEPOINT {nombre_savepoint}")

    def deshacer_operaciones(self):
        self.connection.rollback()
    
    def aplicar_cambios(self):
        self.connection.commit()
    
    def cerrar_conexion(self):
        self.connection.close()

class Controlador:
    def __init__(self):
        self.accesoDB = AccesoBD(server = 'oracle0.ugr.es', db_name = 'practbd.oracle0.ugr.es', user = 'x2085804', password = 'x2085804')
        self.crear_tablas()
        print("Conexión establecida")

    def crear_tablas(self):
        stock_creada = self.accesoDB.crear_tabla("Stock", ["CProducto INT", "Cantidad INT", "PRIMARY KEY (CProducto)"])
        self.accesoDB.crear_tabla("Pedido", ["CPedido INT", "CCliente INT", "Fecha DATE", "PRIMARY KEY (CPedido)"])
        self.accesoDB.crear_tabla("DetallePedido", ["CPedido INT", "CProducto INT", "Cantidad INT", "FOREIGN KEY (CPedido) REFERENCES Pedido(CPedido)", "FOREIGN KEY (CProducto) REFERENCES Stock(CProducto)", "PRIMARY KEY (CPedido, CProducto)"])

        if(stock_creada):
            for i in range(10):
                self.accesoDB.insertar_datos("Stock", {"CProducto": str(i), "Cantidad": str(100 - i*10)})

    def borrar_tablas(self):
        self.accesoDB.borrar_tabla("DetallePedido")
        self.accesoDB.borrar_tabla("Stock")
        self.accesoDB.borrar_tabla("Pedido")

    def reiniciar_sistema(self):
        self.borrar_tablas()
        self.crear_tablas()

    def leer_tablas(self):
        sentenciaSQL_stock = "SELECT * FROM Stock"
        sentenciaSQL_pedido = "SELECT * FROM Pedido"
        sentenciaSQL_detalle_pedido = "SELECT * FROM DetallePedido"

        res_stock = self.accesoDB.execute(sentenciaSQL_stock)
        res_pedido = self.accesoDB.execute(sentenciaSQL_pedido)
        res_detalle_pedido = self.accesoDB.execute(sentenciaSQL_detalle_pedido)

        return res_stock, res_pedido, res_detalle_pedido
    
    def cerrar_conexion(self):
        self.accesoDB.cerrar_conexion()

    def insertar_pedido(self, cpedido, ccliente, fecha_pedido):
        #self.accesoDB.insertar_datos("Pedido", {"Cpedido" : "2", "CCliente" : "2", "Fecha" : "TO_DATE('2021-05-01', 'YYYY-MM-DD')"})
        self.accesoDB.insertar_datos("Pedido", {"CPedido": str(cpedido), "CCliente": str(ccliente), "Fecha": "TO_DATE('" + fecha_pedido + "', 'YYYY-MM-DD')"})

    def insertar_detalle_producto(self, cpedido, cproducto, cantidad):
        #Comprobar que el ID del producto existe TODO

        
        #Comprobar que hay stock del producto
        cantidad_stock = self.accesoDB.buscar_datos("Stock", ["Cantidad"], f"CProducto = {cproducto}")[0][0]

        if(cantidad_stock < cantidad):
            return False

        #Actualizar tabla stock
        self.accesoDB.modificar_datos("Stock", ["Cantidad"], [cantidad_stock - cantidad], f"CProducto = {cproducto}")
        self.accesoDB.insertar_datos("DetallePedido", {"CPedido": str(cpedido), "CProducto": str(cproducto), "Cantidad": str(cantidad)})
        return True

    def eliminar_detalles_producto(self, cpedido):
        self.accesoDB.borrar_datos("DetallePedido", f"CPedido = {cpedido}")

    def cancelar_pedido(self):
        self.accesoDB.deshacer_operaciones()
    
    def aplicar_cambios(self):
        self.accesoDB.aplicar_cambios()
            
#accesoDB = AccesoBD(server = 'oracle0.ugr.es', db_name = 'practbd.oracle0.ugr.es',user = 'x2085804', password = 'x2085804')
#accesoDB.crear_tabla("cuentas", ["Cuenta NUMBER(10)", "Saldo NUMBER(10)"])
#accesoDB.insertar_datos("cuentas", {"Cuenta": "2", "Saldo": "80"})
#accesoDB.borrar_tabla("cuentas")
#print(accesoDB.buscar_datos("cuentas", ["*"]))
#print(accesoDB.buscar_datos("mis_sesiones", ["*"]))