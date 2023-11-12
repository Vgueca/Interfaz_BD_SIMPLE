import tkinter as tk
import customtkinter as ctk
from time import *
from datetime import datetime

from AccesoBD import *

class VentanaMenu:
    current_id_pedido = 0
    ya_iniciado = False
    controlador = None

    #def __init__(self, num=0, n_pedido=-1):
    def __init__(self, num=0):
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

        # Definimos un entero para los ids de los pedidos, aunque luego deberá ser un natural
        #VentanaMenu.current_id_pedido = n_pedido
        #VentanaMenu.current_id_pedido = 0

        # Definimos un entero para el id de producto y otro para la cantidad, aunque luego deberán ser naturales
        self.current_id_producto= -1
        self.current_cantidad = -1
        
        if num==0:
            self.root.title("MENÚ:")

            # Creamos los botones, su texto y les asignamos una función
            self.btn1 = ctk.CTkButton(master=self.root, text="Iniciar Tablas", command=self.v_iniciar_tablas).pack(expand=True)

            self.btn2 = ctk.CTkButton(master=self.root, text="Nuevo Pedido", command=self.v_nuevo_pedido).pack(expand=True)

            self.btn3 = ctk.CTkButton(master=self.root, text="Mostrar Tablas", command=self.v_mostar_tablas).pack(expand=True)

            self.btn4 = ctk.CTkButton(master=self.root, text="Salir", command=self.salir).pack(expand=True)

            # ------------ CÓDIGO DE LA BD ------------------
            #
            #   Iniciamos conexión con la BD 
            #   **Creamos tablas en caso de que las tablas no estén creadas (primera conexión a la BD)
            #
            # ------------ CÓDIGO DE LA BD ------------------
            
            # solo se crea el VentanaMenu.controlador una vez (solo se conecta una vez a la base de datos)
            if not VentanaMenu.ya_iniciado:
                VentanaMenu.controlador = Controlador() # Instanciamos el VentanaMenu.controlador. Al hacerlo se llama al constructor que inicia la conexión con la BD y crea las tablas si no existen
                VentanaMenu.ya_iniciado = True

        elif num==1:
            self.root.title("Opción 1: INICIAR TABLAS")
            self.lbl_1=tk.Label(self.root, text="Tablas iniciadas!").pack(pady=10)

            # ------------ CÓDIGO DE LA BD ------------------
            #   
            # 1. Borrado de la BD
            # 2. Creación Tablas nuevas
            # 3. Inserción de 10 tuplas predefinidas en Stock:
            #           3.1: Definir tuplas: Crear las tuplas aleatorias con un for, haciendo que los ids sean num. del 0-9 y las cantidades naturales random.
            #           3.2: Insertarlas
            # 4. Mostrar contenido de las Tablas (SELECT o llamar a v_mostrar_tablas)
            #
            # ------------ CÓDIGO DE LA BD ------------------

            VentanaMenu.controlador.reiniciar_sistema() # Borramos las tablas y las volvemos a crear
            
            self.btn_continuar=tk.Button(master=self.root, text='Continuar', command=self.continuar_principal, bg="#00B2EE").pack(side=tk.BOTTOM, pady=20)

            #self.continuar_principal()

        elif num==2:
            self.root.columnconfigure(0, weight=1)
            self.root.columnconfigure(1, weight=1)
            self.root.rowconfigure(5, weight=1)

            self.root.title("Opción 2: NUEVO PEDIDO")

            self.lbl_2=tk.Label(self.root, text="Alta de un nuevo pedido.")
            self.lbl_2.grid(padx=10, pady=10, row=0, column=0, columnspan=2)
            self.lbl_3=tk.Label(self.root, text="Introduzca el id de cliente requerida")
            self.lbl_3.grid(padx=10, pady=10, row=1, column=0, columnspan=2)

            # TODO MOSTRAR ID_PEDIDO AL USUARIO?
            '''self.lbl_p=tk.Label(self.root, text='ID Pedido :',  anchor="e").grid(padx=10, row=2, column=0, sticky=tk.W + tk.E)
            #self.t_id_pedido = tk.StringVar()
            #self.intro_id_pedido=tk.Entry(master=self.root, textvariable=self.t_id_pedido).grid(row=2, column=1, sticky=tk.W)
            self.lbl_id_pedido=tk.Label(master=self.root, text=str(VentanaMenu.current_id_pedido)).grid(row=2, column=1, sticky=tk.W)'''

            self.lbl_c=tk.Label(self.root, text='ID Cliente :',  anchor="e").grid(padx=10, row=3, column=0, sticky=tk.W + tk.E)
            self.t_id_cliente = tk.StringVar()
            self.intro_id_cliente=tk.Entry(master=self.root, textvariable=self.t_id_cliente).grid(row=3, column=1, sticky=tk.W)

            # fecha actual
            fecha = datetime.now()
            #formato fehca
            formato = '%Y-%m-%d'
            #pasamos la fecha a string
            self.fecha_pedido = fecha.strftime(formato)

            self.lbl_fecha=tk.Label(self.root, text='Fecha:  ' + self.fecha_pedido)
            self.lbl_fecha.grid(padx=10, pady=10, row=4, column=0, columnspan=2)
    
            self.btn_pedido=tk.Button(master=self.root, text='Añadir Pedido', command=self.procesar_datos_pedido, bg="#00B2EE")
            self.btn_pedido.grid(padx=10, pady=10, row=5, column=0, columnspan=2)

        elif num==3:
            self.root.title("Opción 3: MOSTRAR TABLAS")
            lbl_3=tk.Label(self.root, text="Mostrando contenido de la BD...").pack(pady=10)

            # ------------ CÓDIGO DE LA BD ------------------
            #   
            # 1. Mostrar datos de la BD
            #
            # ------------ CÓDIGO DE LA BD ------------------
            tabla_stock, tabla_pedido, tabla_detalle_pedido = VentanaMenu.controlador.leer_tablas()

            # Mostramos el contenido de las tablas
            ancho_celda, alto_celda = 100, 50

            ventana_stock = tk.Toplevel()
            ventana_stock.title("Tabla Stock")
            if len(tabla_stock) > 0:
                ancho_tabla_stock = len(tabla_stock[0])
                alto_tabla_stock = len(tabla_stock)
                ventana_stock.geometry(f"{ancho_tabla_stock*ancho_celda}x{alto_tabla_stock*alto_celda}+{self.center_x}+{self.center_y}")
                for i in range(alto_tabla_stock):
                    for j in range(ancho_tabla_stock):
                        tk.Label(ventana_stock, text=tabla_stock[i][j]).grid(row=i, column=j)

            ventana_pedido = tk.Toplevel()
            ventana_pedido.title("Tabla Pedido")
            if len(tabla_pedido) > 0:
                ancho_tabla_pedido = len(tabla_pedido[0])
                alto_tabla_pedido = len(tabla_pedido)
                ventana_pedido.geometry(f"{ancho_tabla_pedido*ancho_celda}x{alto_tabla_pedido*alto_celda}+{self.center_x}+{self.center_y}")
                for i in range(alto_tabla_pedido):
                    for j in range(ancho_tabla_pedido):
                        tk.Label(ventana_pedido, text=tabla_pedido[i][j]).grid(row=i, column=j)

            ventana_detalle_pedido = tk.Toplevel()
            ventana_detalle_pedido.title("Tabla Detalle-Pedido")
            if len(tabla_detalle_pedido) > 0:
                ancho_tabla_detalle_pedido = len(tabla_detalle_pedido[0])
                alto_tabla_detalle_pedido = len(tabla_detalle_pedido)
                ventana_detalle_pedido.geometry(f"{ancho_tabla_detalle_pedido*ancho_celda}x{alto_tabla_detalle_pedido*alto_celda}+{self.center_x}+{self.center_y}")
                for i in range(alto_tabla_detalle_pedido):
                    for j in range(ancho_tabla_detalle_pedido):
                        tk.Label(ventana_detalle_pedido, text=tabla_detalle_pedido[i][j]).grid(row=i, column=j)

            self.btn_continuar=tk.Button(master=self.root, text='Continuar', command=self.continuar_principal, bg="#00B2EE").pack(side=tk.BOTTOM, pady=20)
        
        elif num==4:
            self.root.title("OPCIONES DEL PEDIDO: " + str(VentanaMenu.current_id_pedido))

            # Creamos los botones para las distintas opciones
            self.btn1 = tk.Button(master=self.root, text="1. Añadir detalles del pedido", command=self.añadir_detalles, bg="#00B2EE").pack(expand=True)

            self.btn2 = tk.Button(master=self.root, text="2. Eliminar todos los detalles del pedido", command=self.eliminar_detalles, bg="#00B2EE").pack(expand=True)

            self.btn3 = tk.Button(master=self.root, text="3. Cancelar pedido", command=self.cancelar_pedido, bg="#00B2EE").pack(expand=True)

            self.btn4 = tk.Button(master=self.root, text="4. Finalizar pedido", command=self.finalizar_pedido, bg="#00B2EE").pack(expand=True)

        elif num==5:
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

            self.btn_pedido=tk.Button(master=self.root, text='Aceptar', command=self.comprobar_stock, bg="#00B2EE")
            self.btn_pedido.grid(padx=10, pady=10, row=5, column=0, columnspan=2)
            
        '''elif num==5:
            self.root.title("SALIR:")
        else:
            print("Error al crear una ventana auxiliar de una opción no registrada..")'''

        self.root.mainloop()

    def continuar_principal(self):
        # Se destruye la ventana actual
        self.root.destroy()
        # Se instancia una ventana del menú principal
        back_principal = VentanaMenu(num=0)

    def continuar_v4(self):
        # Se destruye la ventana actual
        self.root.destroy()
        # Se instancia una ventana del menú principal
        back_principal = VentanaMenu(num=4)
    
    def v_iniciar_tablas(self):
        # Se destruye la ventana del menú principal
        self.root.destroy()

        # Se instancia una ventana de la función correspondiente
        ventana_aux = VentanaMenu(num=1)        
        
    def procesar_datos_pedido(self):
        # Recoger las variables necesarias
        try:
            id_cliente = int(self.t_id_cliente.get())
            #id_pedido = int(self.t_id_pedido.get())
            if id_cliente < 0:
                raise ValueError
        except ValueError:
            v_error = tk.Toplevel()
            v_error.title("ERROR 1")
            v_error.geometry(f"400x150+{self.center_x}+{self.center_y}")
            e1_lbl = tk.Label(v_error, text="ERROR! INPUT INCORRECTO").pack(expand=True)
            e2_lbl =  tk.Label(v_error, text="Los datos introducidos deben ser números naturales.").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_error, text="Aceptar", command=lambda : v_error.destroy()).pack(expand=True)
            return

        # ------------ CÓDIGO DE LA BD ------------------
        #   
        # 1. Insertar datos de pedido recogidos arriba
        #
        # ------------ CÓDIGO DE LA BD ------------------

        #VentanaMenu.controlador.insertar_pedido(cpedido=VentanaMenu.current_id_pedido, ccliente=id_cliente, fecha_pedido=self.fecha_pedido)
        VentanaMenu.controlador.insertar_pedido(ccliente=id_cliente, fecha_pedido=self.fecha_pedido)

        #Crear menú para Detalles de Pedido
        # Se destruye la ventana actual
        self.root.destroy()
        
        # Se instancia una ventana para los detalles del pedido
        ventana_detalles = VentanaMenu(num=4)  
        
    def v_nuevo_pedido(self):
        # Se destruye la ventana del menú principal
        self.root.destroy()
        # Se instancia una ventana de la función correspondiente
        ventana_aux = VentanaMenu(num=2)
    
    def añadir_detalles(self):
        #print("AÑADIR DETALLES")

        # Destruimos la ventana actual
        self.root.destroy()
        # Se instancia una ventana auxiliar
        ventana_detalles = VentanaMenu(num=5)

    def comprobar_stock(self):
        # Recoger las variables necesarias
        try:
            id_producto = int(self.t_id_producto.get())
            cantidad = int(self.t_cantidad.get())
            if (id_producto<0 | cantidad<0):
                raise ValueError
        except ValueError:
            v_error_1 = tk.Toplevel()
            v_error_1.title("ERROR 1")
            v_error_1.geometry(f"400x150+{self.center_x}+{self.center_y}")
            e1_lbl = tk.Label(v_error_1, text="ERROR! INPUT INCORRECTO").pack(expand=True)
            e2_lbl =  tk.Label(v_error_1, text="Los datos introducidos deben ser números naturales.").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_error_1, text="Aceptar", command=lambda : v_error_1.destroy()).pack(expand=True)
            return
        
        #if existe_producto(id=id_producto):
        if True:
            #if hay_stock(id=id_producto, cant=cantidad):
            if True:
                self.current_id_producto = id_producto
                self.current_cantidad = cantidad
                # LLAMAR A FUNCIÓN Nº 3 DE CÓDIGO DE LA BD de esta sección -> actualizar_stock(id=self.current_id_producto, cant=self.current_cantidad)
                v_conf = tk.Toplevel()
                v_conf.title("CONFIRMACIÓN DE DETALLES AÑADIDOS")
                v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
                c1_lbl = tk.Label(v_conf, text="Detalles del pedido AÑADIDOS con éxito").pack(expand=True)
                c_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_v4).pack(expand=True)
            else:
                v_error_3 = tk.Toplevel()
                v_error_3.title("ERROR 3")
                v_error_3.geometry(f"400x150+{self.center_x}+{self.center_y}")
                e1_lbl = tk.Label(v_error_3, text="ERROR! STOCK INSUFICIENTE").pack(expand=True)
                e2_lbl =  tk.Label(v_error_3, text="No hay stock suficiente del producto introducido.").pack(expand=True)
                e3_lbl =  tk.Label(v_error_3, text="Pruebe con otra cantidad.").pack(expand=True)
                e_btn = ctk.CTkButton(master=v_error_3, text="Aceptar", command=lambda : v_error_3.destroy()).pack(expand=True)
                return
        else:
            v_error_2 = tk.Toplevel()
            v_error_2.title("ERROR 2")
            v_error_2.geometry(f"400x150+{self.center_x}+{self.center_y}")
            e1_lbl = tk.Label(v_error_2, text="ERROR! PRODUCTO INEXISTENTE").pack(expand=True)
            e2_lbl =  tk.Label(v_error_2, text="El ID de producto introducido no está en la BD.").pack(expand=True)
            e3_lbl =  tk.Label(v_error_2, text="Pruebe con otro ID.").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_error_2, text="Aceptar", command=lambda : v_error_2.destroy()).pack(expand=True)
            return

        # ------------ CÓDIGO DE LA BD ------------------
        #   
        # 1. Crear funcion que compruebe si existe el producto introducido y devolver TRUE O FALSE -> def existe_producto(self, id):
        # 2. Crear funcion que compruebe si hay stock del producto introducido para la cantidad requerida y devolver TRUE O FALSE -> def hay_stock(self, id, cant):
        # 3. Crear una función que actualice el stock sin hacer el cambio permanente (NO COMMIT) y mostrarlo (SELECT)
        #   3.1 Hacer INSERT en detalle pedido tras intentar editar la tupla por si se hacen dos Añadir detalles seguidos e identicos
        #
        # ------------ CÓDIGO DE LA BD ------------------

        return VentanaMenu.controlador.insertar_detalle_producto(cproducto=self.current_id_producto, cantidad=self.current_cantidad)

    def eliminar_detalles(self):
        #print("ELIMINAR DETALLES")

        '''# LLAMAR A FUNCIÓN Nº 1 DE CÓDIGO DE LA BD de esta sección -> deshacer_detalles(id_pedido=VentanaMenu.current_id_pedido, id_prod=self.current_id_producto)
        #if deshacer_detalles(id_pedido=VentanaMenu.current_id_pedido, id_prod=self.current_id_producto):
        if True:
            v_conf_1 = tk.Toplevel()
            v_conf_1.title("CONFIRMACIÓN DE ELIMINACIÓN")
            v_conf_1.geometry(f"400x150+{self.center_x}+{self.center_y}")
            c1_lbl = tk.Label(v_conf_1, text="Detalles del pedido eliminados con éxito").pack(expand=True)
            c_btn = ctk.CTkButton(master=v_conf_1, text="Aceptar", command=self.continuar_v4).pack(expand=True)

        else:
            v_error_4 = tk.Toplevel()
            v_error_4.title("ERROR 4")
            v_error_4.geometry(f"400x150+{self.center_x}+{self.center_y}")
            e1_lbl = tk.Label(v_error_4, text="ERROR! BD Error").pack(expand=True)
            e2_lbl =  tk.Label(v_error_4, text="Algo no ha ido como debía..").pack(expand=True)
            e3_lbl =  tk.Label(v_error_4, text="La BD devuelve error.").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_error_4, text="Aceptar", command=self.continuar_v4).pack(expand=True)
            #return (este return es opcional para salir o no del programa según se quiera con este error)'''
        
        v_conf_1 = tk.Toplevel()
        v_conf_1.title("CONFIRMACIÓN DE ELIMINACIÓN")
        v_conf_1.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf_1, text="Detalles del pedido eliminados con éxito").pack(expand=True)
        c_btn = ctk.CTkButton(master=v_conf_1, text="Aceptar", command=self.continuar_v4).pack(expand=True)

        # ------------ CÓDIGO DE LA BD ------------------
        #   
        # 1. Crear funcion que deshaga los cambios anteriores. Simplemente pasar la clave (id_pedido + id_producto) y eliminar la tupla de la tabla Detalles Pedido  
        #
        # ------------ CÓDIGO DE LA BD ------------------   
        VentanaMenu.controlador.eliminar_detalles_producto()

    def cancelar_pedido(self):
        #print("CANCELAR PEDIDO")

        #comentado porque no debería haber errores (simplemente se hace rollback() en la BD)
        '''# LLAMAR A FUNCIÓN Nº 1 DE CÓDIGO DE LA BD de esta sección -> deshacer_detalles(id_pedido=VentanaMenu.current_id_pedido, id_prod=self.current_id_producto)
        #if deshacer_detalles(id_pedido=VentanaMenu.current_id_pedido, id_prod=self.current_id_producto):
        if True:
            v_conf_1 = tk.Toplevel()
            v_conf_1.title("CONFIRMACIÓN DE ELIMINACIÓN")
            v_conf_1.geometry(f"400x150+{self.center_x}+{self.center_y}")
            c1_lbl = tk.Label(v_conf_1, text="Detalles del pedido eliminados con éxito").pack(expand=True)
            c_btn = ctk.CTkButton(master=v_conf_1, text="Aceptar", command=lambda : v_conf_1.destroy()).pack(expand=True)

            # LLAMAR A FUNCIÓN Nº 2 DE CÓDIGO DE LA BD de esta sección -> eliminar_pedido(id_pedido=VentanaMenu.current_id_pedido)
            #if eliminar_pedido(id_pedido=VentanaMenu.current_id_pedido):
            if True:
                v_conf = tk.Toplevel()
                v_conf.title("CONFIRMACIÓN DE ELIMINACIÓN")
                v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
                c1_lbl = tk.Label(v_conf, text="Pedido eliminado con éxito").pack(expand=True)
                e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_principal).pack(expand=True)
            else:
                v_conf = tk.Toplevel()
                v_conf.title("ERROR 4")
                v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
                e1_lbl = tk.Label(v_conf, text="ERROR! BD Error").pack(expand=True)
                e2_lbl =  tk.Label(v_conf, text="Algo no ha ido como debía..").pack(expand=True)
                e3_lbl =  tk.Label(v_conf, text="La BD devuelve error.").pack(expand=True)
                e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_v4).pack(expand=True)
                #return (este return es opcional para salir o no del programa según se quiera con este error pero no funciona por el continuar)

        else:
            v_error_4 = tk.Toplevel()
            v_error_4.title("ERROR 4")
            v_error_4.geometry(f"400x150+{self.center_x}+{self.center_y}")
            e1_lbl = tk.Label(v_error_4, text="ERROR! BD Error").pack(expand=True)
            e2_lbl =  tk.Label(v_error_4, text="Algo no ha ido como debía..").pack(expand=True)
            e3_lbl =  tk.Label(v_error_4, text="La BD devuelve error.").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_error_4, text="Aceptar", command=self.continuar_v4).pack(expand=True)
            #return (este return es opcional para salir o no del programa según se quiera con este error)'''
        
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

        self.current_id_producto = -1
        self.current_cantidad = -1

        # ------------ CÓDIGO DE LA BD ------------------
        #   
        # 1. Llamar a la funcion que deshaga (elimine) los detalles (la de antes). Simplemente pasar la clave (id_pedido + id_producto) y eliminar la tupla de la tabla Detalles Pedido  
        # 2. Crear una función que elimine el pedido de la tabla Pedido. 
        #
        # ------------ CÓDIGO DE LA BD ------------------
        VentanaMenu.controlador.cancelar_pedido()

    def finalizar_pedido(self):
        #print("FINALIZAR PEDIDO")

        #comentado porque no debería haber errores (simplemente se hace commit() en la BD)
        '''# LLAMAR A FUNCIÓN Nº 1 DE CÓDIGO DE LA BD de esta sección -> finalizar_pedido(id_pedido=VentanaMenu.current_id_pedido, id_producto=self.current_id_producto)
        #if finalizar_pedido(id_pedido=VentanaMenu.current_id_pedido, id_producto=self.current_id_producto):
        if True:
            VentanaMenu.current_id_pedido += 1

            v_conf = tk.Toplevel()
            v_conf.title("CONFIRMACIÓN DE PEDIDO")
            v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
            c1_lbl = tk.Label(v_conf, text="Pedido finalizado correctamente").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_principal).pack(expand=True)
        else:
            v_conf = tk.Toplevel()
            v_conf.title("ERROR 4")
            v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
            e1_lbl = tk.Label(v_conf, text="ERROR! BD Error").pack(expand=True)
            e2_lbl =  tk.Label(v_conf, text="Algo no ha ido como debía..").pack(expand=True)
            e3_lbl =  tk.Label(v_conf, text="La BD devuelve error.").pack(expand=True)
            e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_v4).pack(expand=True)
            #return (este return es opcional para salir o no del programa según se quiera con este error pero no funciona por el continuar)'''


        VentanaMenu.current_id_pedido += 1

        v_conf = tk.Toplevel()
        v_conf.title("CONFIRMACIÓN DE PEDIDO")
        v_conf.geometry(f"400x150+{self.center_x}+{self.center_y}")
        c1_lbl = tk.Label(v_conf, text="Pedido finalizado correctamente").pack(expand=True)
        e_btn = ctk.CTkButton(master=v_conf, text="Aceptar", command=self.continuar_principal).pack(expand=True)

        # ------------ CÓDIGO DE LA BD ------------------
        #   
        # 1. Llamar a la funcion que haga permanentes los cambios
        #
        # ------------ CÓDIGO DE LA BD ------------------

        VentanaMenu.controlador.aplicar_cambios()
        
    def v_mostar_tablas(self):
        # Se destruye la ventana del menú principal
        self.root.destroy()
        # Se instancia una ventana de la función correspondiente
        ventana_aux = VentanaMenu(num=3)
        
    def salir(self):
        # ------------ CÓDIGO DE LA BD ------------------
        #       función para CERRAR CONEXION CON LA BD
        # ------------ CÓDIGO DE LA BD ------------------
        
        VentanaMenu.controlador.cerrar_conexion()

        exit()

ventana=VentanaMenu()

#accesoDB = AccesoBD(server = 'oracle0.ugr.es', db_name = 'practbd.oracle0.ugr.es',user = 'x2085804', password = 'x2085804')

#print(accesoDB.buscar_datos("mis_sesiones", ["*"]))
#print(accesoDB.borrar_tabla("DetallePedido"))
#print(accesoDB.crear_tabla("Stock", ["CProducto INT", "Cantidad INT", "PRIMARY KEY (CProducto)"]))
#print(accesoDB.borrar_tabla("Stock"))
#print(accesoDB.crear_tabla("Pedido", ["CPedido INT", "CCliente INT", "Fecha DATE", "PRIMARY KEY (CPedido)"]))
#print(accesoDB.borrar_tabla("Pedido"))
#print(accesoDB.crear_tabla("Detalle", ["CPedido INT", "CProducto INT", "Cantidad INT", "FOREIGN KEY (CPedido) REFERENCES Pedido(CPedido)", "FOREIGN KEY (CProducto) REFERENCES Stock(CProducto)", "PRIMARY KEY (CPedido, CProducto)"]))
#print(accesoDB.execute("SELECT * FROM USER_TABLES"))

#accesoDB.insertar_datos("Pedido", {"Cpedido" : "2", "CCliente" : "2", "Fecha" : "TO_DATE('2021-05-01', 'YYYY-MM-DD')"})

#print(accesoDB.buscar_datos("Pedido", ["*"]))

#accesoDB.cerrar_conexion()