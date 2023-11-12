import tkinter as tk
import customtkinter as ctk
from time import *
from datetime import datetime

from AccesoBD import *

class TipoVentana(Enum):
    MENU_PRINCIPAL = 0
    TABLAS_INICIADAS = 1
    NUEVO_PEDIDO = 2
    TABLAS_CARGADAS = 3
    OPCIONES_PEDIDO = 4
    AÑADIR_DETALLES = 5

class VentanaMenu:
    ya_iniciado = False
    controlador = None
    current_id_pedido = -1
    current_tabla_stock = []
    current_tabla_pedido = []
    current_tabla_detalle = []

    def __init__(self, tipo_ventana = TipoVentana.MENU_PRINCIPAL):
        self.root = tk.Tk()

        window_width = 400
        window_height = 225

        # Tomamos las dimensiones de la pantalla
        p_width = self.root.winfo_screenwidth()
        p_height = self.root.winfo_screenheight()

        # Buscamos el centro de la pantalla
        self.center_x = int(p_width/2 - window_width / 2)
        self.center_y = int(p_height/2 - window_height / 2)

        # Ajustamos la posición de la ventana al centro de la pantalla
        self.root.geometry(f'{window_width}x{window_height}+{self.center_x}+{self.center_y}')

        match tipo_ventana:
            case TipoVentana.MENU_PRINCIPAL:
                self.root.title("MENÚ:")

                # Creamos los botones, su texto y les asignamos una función
                self.btn1 = ctk.CTkButton(master=self.root, text="Iniciar Tablas", command=self.v_iniciar_tablas).pack(expand=True)

                self.btn2 = ctk.CTkButton(master=self.root, text="Nuevo Pedido", command=self.v_nuevo_pedido).pack(expand=True)

                self.btn3 = ctk.CTkButton(master=self.root, text="Mostrar Tablas", command=self.v_mostrar_tablas).pack(expand=True)

                self.btn4 = ctk.CTkButton(master=self.root, text="Salir", command=self.salir).pack(expand=True)


                # ------------ CÓDIGO DE LA BD ------------------

                #   Iniciamos conexión con la BD 

                # solo se crea el VentanaMenu.controlador una vez (solo se conecta una vez a la base de datos)
                if not VentanaMenu.ya_iniciado:
                    try:
                        VentanaMenu.controlador = Controlador() # Instanciamos el VentanaMenu.controlador. Al hacerlo se llama al constructor que inicia la conexión con la BD y crea las tablas si no existen
                        VentanaMenu.ya_iniciado = True
                    except pyodbc.Error as error:
                        self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
                        return

                # ------------ CÓDIGO DE LA BD ------------------

            case TipoVentana.TABLAS_INICIADAS:
                self.root.title("Opción 1: INICIAR TABLAS")
                self.lbl_1=tk.Label(self.root, text="Tablas iniciadas!").pack(pady=10)
                self.btn_continuar=tk.Button(master=self.root, text='Continuar', command=self.continuar_principal, bg="#00B2EE").pack(side=tk.BOTTOM, pady=20)

            case TipoVentana.NUEVO_PEDIDO:
                self.root.columnconfigure(0, weight=1)
                self.root.columnconfigure(1, weight=1)
                self.root.rowconfigure(5, weight=1)

                self.root.title("Opción 2: NUEVO PEDIDO")

                self.lbl_2=tk.Label(self.root, text="Alta de un nuevo pedido.")
                self.lbl_2.grid(padx=10, pady=10, row=0, column=0, columnspan=2)
                self.lbl_3=tk.Label(self.root, text="Introduzca el id de cliente requerida")
                self.lbl_3.grid(padx=10, pady=10, row=1, column=0, columnspan=2)

                # Consultamos la base de datos para saber el ID que tendría el pedido siguiente
                VentanaMenu.current_id_pedido = VentanaMenu.controlador.consultar_ultimo_id_pedido() + 1

                self.lbl_p=tk.Label(self.root, text='ID Pedido : ' + str(VentanaMenu.current_id_pedido),  anchor="e").grid(padx=10, row=2, column=0, columnspan=2)
                self.lbl_c=tk.Label(self.root, text='ID Cliente :',  anchor="e").grid(padx=10, row=3, column=0, sticky=tk.W + tk.E)
                self.t_id_cliente = tk.StringVar()
                self.intro_id_cliente=tk.Entry(master=self.root, textvariable=self.t_id_cliente).grid(row=3, column=1, sticky=tk.W)

                # fecha actual
                fecha = datetime.now()
                #formato fecha
                formato = '%Y-%m-%d'
                #pasamos la fecha a string
                self.fecha_pedido = fecha.strftime(formato)

                self.lbl_fecha=tk.Label(self.root, text='Fecha:  ' + self.fecha_pedido)
                self.lbl_fecha.grid(padx=10, pady=10, row=4, column=0, columnspan=2)
        
                self.btn_pedido=tk.Button(master=self.root, text='Añadir Pedido', command=self.procesar_datos_pedido, bg="#00B2EE")
                self.btn_pedido.grid(padx=10, pady=10, row=5, column=0, columnspan=2)

            case TipoVentana.TABLAS_CARGADAS:
                self.root.title("Opción 3: CONTENIDO DE LA BASE DE DATOS")
                lbl_3=tk.Label(self.root, text="Tablas de datos cargadas!").pack(pady=10)
                self.btn_continuar=tk.Button(master=self.root, text='Continuar', command=self.continuar_principal, bg="#00B2EE").pack(side=tk.BOTTOM, pady=20)

                ventana_stock = tk.Toplevel()
                ventana_stock.title("Tabla Stock")
                if len(VentanaMenu.current_tabla_stock) > 0:
                    ancho_tabla_stock = len(VentanaMenu.current_tabla_stock[0])
                    alto_tabla_stock = len(VentanaMenu.current_tabla_stock)

                    #Mostrar primero los nombres de las columnas
                    columnas_stock = ["CProducto", "Cantidad"]
                    for i in range(len(columnas_stock)):
                        entry_text = tk.StringVar()
                        entry = tk.Entry(ventana_stock, width=10, state="readonly", textvariable=entry_text, justify = tk.CENTER, font = ("TkDefaultFont", 10, "bold"))
                        entry.grid(row=0, column=i)
                        entry_text.set(columnas_stock[i])

                    for i in range(alto_tabla_stock):
                        for j in range(ancho_tabla_stock):
                            entry_text = tk.StringVar()
                            entry = tk.Entry(ventana_stock, width=10, state="readonly", textvariable=entry_text, justify = tk.CENTER, font = ("TkDefaultFont", 10))
                            entry.grid(row=i+1, column=j)
                            entry_text.set(VentanaMenu.current_tabla_stock[i][j])

                for fila in VentanaMenu.current_tabla_pedido:
                    fila[2] = fila[2].strftime("%d/%m/%Y")

                ventana_pedido = tk.Toplevel()
                ventana_pedido.title("Tabla Pedido")
                if len(VentanaMenu.current_tabla_pedido) > 0:
                    ancho_tabla_pedido = len(VentanaMenu.current_tabla_pedido[0])
                    alto_tabla_pedido = len(VentanaMenu.current_tabla_pedido)

                    #Mostrar primero los nombres de las columnas
                    columnas_pedido = ["CPedido", "CCliente", "Fecha"]
                    for i in range(len(columnas_pedido)):
                        entry_text = tk.StringVar()
                        entry = tk.Entry(ventana_pedido, width=10, state="readonly", textvariable=entry_text, justify = tk.CENTER, font = ("TkDefaultFont", 10, "bold"))
                        entry.grid(row=0, column=i)
                        entry_text.set(columnas_pedido[i])

                    for i in range(alto_tabla_pedido):
                        for j in range(ancho_tabla_pedido):
                            entry_text = tk.StringVar()
                            entry = tk.Entry(ventana_pedido, width=10, state="readonly", textvariable=entry_text, justify = tk.CENTER, font = ("TkDefaultFont", 10))
                            entry.grid(row=i+1, column=j)
                            entry_text.set(VentanaMenu.current_tabla_pedido[i][j])

                ventana_detalle_pedido = tk.Toplevel()
                ventana_detalle_pedido.title("Tabla Detalle-Pedido")
                if len(VentanaMenu.current_tabla_detalle) > 0:
                    ancho_tabla_detalle_pedido = len(VentanaMenu.current_tabla_detalle[0])
                    alto_tabla_detalle_pedido = len(VentanaMenu.current_tabla_detalle)

                    #Mostrar primero los nombres de las columnas
                    columnas_detalle_pedido = ["CPedido", "CProducto", "Cantidad"]
                    for i in range(len(columnas_detalle_pedido)):
                        entry_text = tk.StringVar()
                        entry = tk.Entry(ventana_detalle_pedido, width=10, state="readonly", textvariable=entry_text, justify = tk.CENTER, font = ("TkDefaultFont", 10, "bold"))
                        entry.grid(row=0, column=i)
                        entry_text.set(columnas_detalle_pedido[i])

                    for i in range(alto_tabla_detalle_pedido):
                        for j in range(ancho_tabla_detalle_pedido):
                            entry_text = tk.StringVar()
                            entry = tk.Entry(ventana_detalle_pedido, width=10, state="readonly", textvariable=entry_text, justify = tk.CENTER, font = ("TkDefaultFont", 10))
                            entry.grid(row=i+1, column=j)
                            entry_text.set(VentanaMenu.current_tabla_detalle[i][j])            
            case TipoVentana.OPCIONES_PEDIDO:
                self.root.title("OPCIONES DEL PEDIDO: " + str(VentanaMenu.current_id_pedido))

                # Creamos los botones para las distintas opciones
                self.btn1 = tk.Button(master=self.root, text="1. Añadir detalles del pedido", command=self.v_añadir_detalles, bg="#00B2EE").pack(expand=True)

                self.btn2 = tk.Button(master=self.root, text="2. Eliminar todos los detalles del pedido", command=self.eliminar_detalles, bg="#00B2EE").pack(expand=True)

                self.btn3 = tk.Button(master=self.root, text="3. Cancelar pedido", command=self.cancelar_pedido, bg="#00B2EE").pack(expand=True)

                self.btn4 = tk.Button(master=self.root, text="4. Finalizar pedido", command=self.finalizar_pedido, bg="#00B2EE").pack(expand=True)

            case TipoVentana.AÑADIR_DETALLES:
                self.root.columnconfigure(0, weight=1)
                self.root.columnconfigure(1, weight=1)
                self.root.rowconfigure(5, weight=1)

                self.root.title("AÑADIR DETALLES DEL PEDIDO: " + str(VentanaMenu.current_id_pedido))

                self.lbl_2=tk.Label(self.root, text="Introduzca los detalles del pedido.")
                self.lbl_2.grid(padx=10, pady=10, row=0, column=0, columnspan=2)
                self.lbl_3=tk.Label(self.root, text="Introduzca el id del producto y la cantidad requerida")
                self.lbl_3.grid(padx=10, pady=10, row=1, column=0, columnspan=2)

                self.lbl_prod=tk.Label(self.root, text='ID Producto :',  anchor="e").grid(padx=10, row=2, column=0, sticky=tk.W + tk.E)
                self.t_id_producto = tk.StringVar()
                self.intro_id_producto=tk.Entry(master=self.root, textvariable=self.t_id_producto).grid(row=2, column=1, sticky=tk.W)

                self.lbl_cant=tk.Label(self.root, text='Cantidad :',  anchor="e").grid(padx=10, row=3, column=0, sticky=tk.W + tk.E)
                self.t_cantidad = tk.StringVar()
                self.intro_cant=tk.Entry(master=self.root, textvariable=self.t_cantidad).grid(row=3, column=1, sticky=tk.W)

                self.btn_pedido=tk.Button(master=self.root, text='Aceptar', command=self.insertar_detalles, bg="#00B2EE")
                self.btn_pedido.grid(padx=10, pady=10, row=5, column=0, columnspan=2)

        self.root.mainloop()

    def continuar_principal(self):
        # Se destruye la ventana actual
        self.root.destroy()

        # Se instancia una ventana del menú principal
        VentanaMenu()

    def continuar_opciones_pedido(self):
        # Se destruye la ventana actual
        self.root.destroy()

        # Se instancia una ventana del menú de opciones del pedido
        VentanaMenu(tipo_ventana = TipoVentana.OPCIONES_PEDIDO)
    
    def v_iniciar_tablas(self):

        # ------------ CÓDIGO DE LA BD ------------------
                
        # 1. Borrado de la BD
        # 2. Creación Tablas nuevas
        # 3. Inserción de 10 tuplas predefinidas en Stock:
        #     3.1: Definir tuplas.
        #     3.2: Insertarlas

        try:
            VentanaMenu.controlador.reiniciar_sistema() # Borramos las tablas y las volvemos a crear
        except pyodbc.Error as error:
            self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
            return

        # ------------ CÓDIGO DE LA BD ------------------
        

        # Se destruye la ventana del menú principal
        self.root.destroy()

        # Se instancia una ventana que indica que las tablas se han creado
        VentanaMenu(tipo_ventana = TipoVentana.TABLAS_INICIADAS)
        
    def procesar_datos_pedido(self):
        # Recoger las variables necesarias
        try:
            id_cliente = int(self.t_id_cliente.get())
            if id_cliente < 0:
                raise ValueError
        except ValueError:
            self.mostrar_ventana_error(TipoError.ID_CLIENTE_MAL_INTRODUCIDO)
            return
        

        # ------------ CÓDIGO DE LA BD ------------------
          
        # 1. Insertar datos de pedido recogidos arriba
        
        try:
            VentanaMenu.controlador.insertar_pedido(ccliente=id_cliente, fecha_pedido=self.fecha_pedido)
        except pyodbc.Error as error:
            self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
            return
        
        # ------------ CÓDIGO DE LA BD ------------------


        # Crear menú para Detalles de Pedido

        # Se destruye la ventana actual
        self.root.destroy()
        
        # Se instancia una ventana del menú de opciones del pedido
        VentanaMenu(tipo_ventana = TipoVentana.OPCIONES_PEDIDO)
        
    def v_nuevo_pedido(self):
        # Se destruye la ventana del menú principal
        self.root.destroy()

        # Se instancia una ventana del menú de creación de un nuevo pedido
        VentanaMenu(tipo_ventana = TipoVentana.NUEVO_PEDIDO)
    
    def v_añadir_detalles(self):
        # Destruimos la ventana actual
        self.root.destroy()

        # Se instancia una ventana del menú de añadir detalles del pedido
        VentanaMenu(tipo_ventana = TipoVentana.AÑADIR_DETALLES)

    def insertar_detalles(self):
        # Recoger las variables necesarias
        try:
            id_producto = int(self.t_id_producto.get())
            cantidad = int(self.t_cantidad.get())
            print(id_producto, " ", cantidad)
            if id_producto < 0 or cantidad < 0:
                raise ValueError
            if id_producto > 9:
                raise CustomError(TipoError.ID_PRODUCTO_NO_EXISTE)
        except ValueError:
            self.mostrar_ventana_error(TipoError.NUMERO_MAL_INTRODUCIDO)
            return
        except CustomError as custom_error:
            self.mostrar_ventana_error(custom_error.tipo_error, custom_error.string_error)
            return

        # ------------ CÓDIGO DE LA BD ------------------
         
        # 1. Insertar detalles del pedido recogidos arriba
        
        try:
            insertado = VentanaMenu.controlador.insertar_detalle_pedido(cproducto=id_producto, cantidad=cantidad)
        except CustomError as custom_error:
            self.mostrar_ventana_error(custom_error.tipo_error, custom_error.string_error)
            return
        except pyodbc.Error as error:
            self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
            return
        
        # ------------ CÓDIGO DE LA BD ------------------
        
        v_conf = tk.Toplevel()
        v_conf.title("CONFIRMACIÓN DE DETALLES AÑADIDOS")
        v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf, text="Detalles del pedido AÑADIDOS con éxito").pack(expand=True)
        c_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_opciones_pedido).pack(expand=True)

    def eliminar_detalles(self):

        # ------------ CÓDIGO DE LA BD ------------------
        
        # 1. Llamar a función que deshace los detalles introducidos (rollback_to savepoint).
        
        try:
            VentanaMenu.controlador.eliminar_detalles_producto()
        except pyodbc.Error as error:
            self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
            return

        # ------------ CÓDIGO DE LA BD ------------------   


        # Crear ventana de confirmación de eliminación de detalles
        v_conf_1 = tk.Toplevel()
        v_conf_1.title("CONFIRMACIÓN DE ELIMINACIÓN")
        v_conf_1.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf_1, text="Detalles del pedido eliminados con éxito").pack(expand=True)
        c_btn = ctk.CTkButton(master=v_conf_1, text="Aceptar", command=self.continuar_opciones_pedido).pack(expand=True)

    def cancelar_pedido(self):        

        # ------------ CÓDIGO DE LA BD ------------------

        # 1. Llamar a la funcion que deshace la operación completa del pedido (rollback).
        
        try:
            VentanaMenu.controlador.cancelar_pedido()
        except pyodbc.Error as error:
            self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
            return

        # ------------ CÓDIGO DE LA BD ------------------


        v_conf_1 = tk.Toplevel()
        v_conf_1.title("CONFIRMACIÓN DE ELIMINACIÓN")
        v_conf_1.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf_1, text="Detalles del pedido eliminados con éxito").pack(expand=True)
        c_btn = ctk.CTkButton(master=v_conf_1, text="Aceptar", command=lambda : v_conf_1.destroy()).pack(expand=True)
        
        v_conf = tk.Toplevel()
        v_conf.title("CONFIRMACIÓN DE ELIMINACIÓN")
        v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf, text="Pedido eliminado con éxito").pack(expand=True)
        e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_principal).pack(expand=True)
        

    def finalizar_pedido(self):

        # ------------ CÓDIGO DE LA BD ------------------
        
        # 1. Llamar a la funcion que haga permanentes los cambios
        
        try:
            VentanaMenu.controlador.aplicar_cambios()
        except pyodbc.Error as error:
            self.mostrar_ventana_error(TipoError.BD_ERROR, str(error.args[1]))
            return

        # ------------ CÓDIGO DE LA BD ------------------


        v_conf = tk.Toplevel()
        v_conf.title("CONFIRMACIÓN DE PEDIDO")
        v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf, text="Pedido finalizado correctamente").pack(expand=True)
        e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_principal).pack(expand=True)
        
    def v_mostrar_tablas(self):

        # ------------ CÓDIGO DE LA BD ------------------
                
        # 1. Leer datos de la BD
        
        VentanaMenu.current_tabla_stock, VentanaMenu.current_tabla_pedido, VentanaMenu.current_tabla_detalle = VentanaMenu.controlador.leer_tablas()

        # ------------ CÓDIGO DE LA BD ------------------

        # Se destruye la ventana del menú principal
        self.root.destroy()

        # Se instancia una ventana de la función correspondiente
        VentanaMenu(tipo_ventana = TipoVentana.TABLAS_CARGADAS)

    def mostrar_ventana_error(self, tipo_error, string_error = ""):
        ventana_error = tk.Toplevel()
        funcion_boton = None

        bd_error = ""
        match tipo_error:
            case TipoError.ID_CLIENTE_MAL_INTRODUCIDO:
                string_error = "ERROR! ID DEL CLIENTE MAL INTRODUCIDO. DEBE SER UN NÚMERO NATURAL."
                funcion_boton = self.v_nuevo_pedido
            case TipoError.NUMERO_MAL_INTRODUCIDO:
                string_error = "ERROR! ID DEL PRODUCTO MAL INTRODUCIDO. DEBE SER UN NÚMERO NATURAL."
                funcion_boton = self.v_añadir_detalles
            case TipoError.ID_PRODUCTO_NO_EXISTE:
                string_error = "ERROR! ID DEL PRODUCTO NO EXISTE EN LA BASE DE DATOS."
                funcion_boton = self.v_añadir_detalles
            case TipoError.STOCK_INSUFICIENTE:
                string_error = "ERROR! STOCK INSUFICIENTE."
                funcion_boton = self.v_añadir_detalles
            case TipoError.BD_ERROR:
                bd_error = string_error
                string_error = "ERROR! ERROR EN LA BASE DE DATOS. INFO: "
                funcion_boton = self.salir

        ancho_ventana = len(string_error) * 10
        alto_ventana = 150

        ventana_error.title("ERROR")
        tk.Label(ventana_error, text=string_error).pack(expand=True)
        
        if tipo_error == TipoError.BD_ERROR:
            tk.Label(ventana_error, text=bd_error).pack(expand=True)
            alto_ventana = 200

        ventana_error.geometry(f"{ancho_ventana}x{alto_ventana}+{self.center_x}+{self.center_y}")

        ctk.CTkButton(master=ventana_error, text="Aceptar", command=funcion_boton).pack(expand=True)
    
    def salir(self):
        # ------------ CÓDIGO DE LA BD ------------------

        # Función para CERRAR CONEXION CON LA BD

        try:
            VentanaMenu.controlador.cerrar_conexion()
            exit()
        except pyodbc.Error as error:
            exit()
        
        # ------------ CÓDIGO DE LA BD ------------------

ventana=VentanaMenu()