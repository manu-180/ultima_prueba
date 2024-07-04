import reflex as rx
import firebase_admin
import os
import asyncio
import requests as rq
import smtplib
import http.cookies
from firebase_admin import auth, db, credentials
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime, timedelta



async def check_database_periodically():
    while True:
        firebase = FireBase()
        data = firebase.data()
        rx.State.update_forward_refs()  
        await asyncio.sleep(10)  

class Horarios(rx.Base):
    id: int
    dia: dict

    

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

firebase_sdk = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(firebase_sdk, {"databaseURL": DATABASE_URL})

class CookieState:

    def _init_(self):
        self.cookie = "2"
    
    def change_cookie(self, email):
        self.cookie = email
            
            
cookie_state = CookieState()


class FireBase():
    ref = db.reference("/Horarios/")

    def obtener_fechas_proximas_semanas(self):
        today = datetime.now()
        
        next_monday = today + timedelta(days=(7 - today.weekday() + 0) % 7)
        fechas = []
        for i in range(5):
            lunes = next_monday + timedelta(weeks=i)
            
            for j in range(5):  # Solo lunes a viernes
                fecha = lunes + timedelta(days=j)
                fechas.append(fecha.strftime("%d/%m"))
        
        return fechas

    def data(self):

        class_data = []
        
        data = self.ref.get("dia")
        print(data)
        

    def horarios(self):
        horarios = []
        for i in self.data():
            horarios.append(i.horario)
        return horarios

                
            
    def cant_users(self, semana, dia, hora):
        horario_ref = db.reference(f'/Horarios/-O0QT9g3RXHZASIMvyfw/{semana}/dia/{dia}')
        cant_users = 0
        horarios_diccionario = horario_ref.get()

        try:
            if horarios_diccionario is not None:
                if hora in horarios_diccionario:
                    lista_hora = horarios_diccionario[hora]
                    horarios_diccionario[hora] = [email for email in lista_hora if email is not None]
            for clave, valor in horarios_diccionario.items():
                if clave == hora:
                    cant_users = len(valor)
            return cant_users
        except:
            print("funcion cant users")
            print(horarios_diccionario)

            
                        

    def check_cant_users(self, semana, dia, hora):
        try:
            if self.cant_users(semana, dia, hora) < 4:
                return True
            else: return False
        except:
            print(self.cant_users(semana, dia, hora))

    def agregar_usuario_a_horario(self, semana, dia, hora):

        horario_ref = db.reference(f'/Horarios/-O0QT9g3RXHZASIMvyfw/{semana}/dia/{dia}')
        horarios_diccionario = horario_ref.get()
        
        try:

            usuarios = horarios_diccionario[hora]
            
            if cookie_state.cookie not in usuarios:
                if self.cant_users(semana, dia, hora) < 4 :
                    usuarios.append(cookie_state.cookie)
                print("la clase esta llena")
            
            horario_ref.update({hora: usuarios})
        except Exception as e:
            usuarios = list(horarios_diccionario[hora].values())
            if cookie_state.cookie not in usuarios:
                if self.cant_users(semana , dia, hora) < 4 :
                    usuarios.append(cookie_state.cookie)
                print("la clase esta llena")
            horario_ref.update({hora: usuarios})



    def eliminar_usuario_a_horario(self,semana, dia, hora, usuario):
        usuarios_ref = db.reference(f'/Horarios/-O0QT9g3RXHZASIMvyfw/{semana}/dia/{dia}')
        usuarios_diccionario = usuarios_ref.get()
        try:
            lista_usuarios = usuarios_ref.get()
            if usuario in lista_usuarios:
                lista_usuarios.remove(usuario)
                usuarios_ref.set(lista_usuarios)
            else:
                print("Este usuario no esta en la clase")
        except:
            # if usuario  in usuarios_diccionario:
            #     usuarios_diccionario.remove(usuario)
            #     usuarios_ref.set(usuarios_diccionario)
            # else:
                print("raro")
    

    def get_user_data(self, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            return uid, user.email
        except Exception as e:
            print('Error fetching user data:', e)
            return None, None
        

    def encontrar_usuario(self, user):
        fechas = self.obtener_fechas_proximas_semanas()
        try:
            horario_ref = db.reference(f'/Horarios/-O0QT9g3RXHZASIMvyfw')
            horarios_diccionario = horario_ref.get()
            index= 0
            horarios = []
            for semana, data_dias_usuarios in horarios_diccionario.items():
                for dias, dias_usuarios in data_dias_usuarios.items():
                    for  dia, hora_usuarios in  dias_usuarios.items():
                        for hora, usuarios in hora_usuarios.items():
                            if user in usuarios:
                                horarios.append(f'{semana},{dia},{fechas[index]},{hora}')
                        index += 1
            return horarios
        except:
            print(horarios_diccionario)
            print("funcion encontrar_usuario")
        

firebase = FireBase()

#firebase.ref.push({"semana1": {'dia': {'lunes': {'17:30': ['jul1inv@gmail.com', 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com', 'manumanu97@hotmail.com']}, 'martes': {'10:00': [None, None, None, 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '14:00': ['ju11linv@gmail.com', 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, 'reycamila04@gmail.com', None, 'ivannarisaro@hotmail.com']}, 'miercoles': {'14:00': ['manumanu97@gmail.com', None, 'asdfasdf', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, None, 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': ['juli1nv@gmail.com', 'manumanu97@hotmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com']}, 'tjueves': {'10:00': {'0': 'julinv@gmail.com', '5': 'skere@hotmail.com', '6': 'ivannarisaro@hotmail.com'}, '14:00': {'1': 'julinv@gmail.com', '3': 'reycamila04@gmail.com', '6': 'ivannarisaro@hotmail.com'}, '16:30': [None, 'jul111inv@gmail.com', None, 'reycamila04@gmail.com', 'skere@hotmail.com']}, 'viernes': {'16:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com'], '18:00': [None, None, 'skere@hotmail.com', 'manumanu97@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com']}}},"semana2": {'dia': {'lunes': {'17:30': ['jul1inv@gmail.com', 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com', 'manumanu97@hotmail.com']}, 'martes': {'10:00': [None, None, None, 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '14:00': ['ju11linv@gmail.com', 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, 'reycamila04@gmail.com', None, 'ivannarisaro@hotmail.com']}, 'miercoles': {'14:00': ['manumanu97@gmail.com', None, 'asdfasdf', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, None, 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': ['juli1nv@gmail.com', 'manumanu97@hotmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com']}, 'tjueves': {'10:00': {'0': 'julinv@gmail.com', '5': 'skere@hotmail.com', '6': 'ivannarisaro@hotmail.com'}, '14:00': {'1': 'julinv@gmail.com', '3': 'reycamila04@gmail.com', '6': 'ivannarisaro@hotmail.com'}, '16:30': [None, 'jul111inv@gmail.com', None, 'reycamila04@gmail.com', 'skere@hotmail.com']}, 'viernes': {'16:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com'], '18:00': [None, None, 'skere@hotmail.com', 'manumanu97@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com']}}}, "semana3" : {'dia': {'lunes': {'17:30': ['jul1inv@gmail.com', 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com', 'manumanu97@hotmail.com']}, 'martes': {'10:00': [None, None, None, 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '14:00': ['ju11linv@gmail.com', 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, 'reycamila04@gmail.com', None, 'ivannarisaro@hotmail.com']}, 'miercoles': {'14:00': ['manumanu97@gmail.com', None, 'asdfasdf', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, None, 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': ['juli1nv@gmail.com', 'manumanu97@hotmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com']}, 'tjueves': {'10:00': {'0': 'julinv@gmail.com', '5': 'skere@hotmail.com', '6': 'ivannarisaro@hotmail.com'}, '14:00': {'1': 'julinv@gmail.com', '3': 'reycamila04@gmail.com', '6': 'ivannarisaro@hotmail.com'}, '16:30': [None, 'jul111inv@gmail.com', None, 'reycamila04@gmail.com', 'skere@hotmail.com']}, 'viernes': {'16:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com'], '18:00': [None, None, 'skere@hotmail.com', 'manumanu97@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com']}}}, "semana4" : {'dia': {'lunes': {'17:30': ['jul1inv@gmail.com', 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com', 'manumanu97@hotmail.com']}, 'martes': {'10:00': [None, None, None, 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '14:00': ['ju11linv@gmail.com', 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, 'reycamila04@gmail.com', None, 'ivannarisaro@hotmail.com']}, 'miercoles': {'14:00': ['manumanu97@gmail.com', None, 'asdfasdf', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, None, 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': ['juli1nv@gmail.com', 'manumanu97@hotmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com']}, 'tjueves': {'10:00': {'0': 'julinv@gmail.com', '5': 'skere@hotmail.com', '6': 'ivannarisaro@hotmail.com'}, '14:00': {'1': 'julinv@gmail.com', '3': 'reycamila04@gmail.com', '6': 'ivannarisaro@hotmail.com'}, '16:30': [None, 'jul111inv@gmail.com', None, 'reycamila04@gmail.com', 'skere@hotmail.com']}, 'viernes': {'16:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com'], '18:00': [None, None, 'skere@hotmail.com', 'manumanu97@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com']}}}, "semana5" : {'dia': {'lunes': {'17:30': ['jul1inv@gmail.com', 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com', 'manumanu97@hotmail.com']}, 'martes': {'10:00': [None, None, None, 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '14:00': ['ju11linv@gmail.com', 'reycamila04@gmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, 'reycamila04@gmail.com', None, 'ivannarisaro@hotmail.com']}, 'miercoles': {'14:00': ['manumanu97@gmail.com', None, 'asdfasdf', 'ivannarisaro@hotmail.com'], '16:30': ['j1ulinv@gmail.com', None, None, None, 'skere@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': ['juli1nv@gmail.com', 'manumanu97@hotmail.com', 'skere@hotmail.com', 'ivannarisaro@hotmail.com']}, 'tjueves': {'10:00': {'0': 'julinv@gmail.com', '5': 'skere@hotmail.com', '6': 'ivannarisaro@hotmail.com'}, '14:00': {'1': 'julinv@gmail.com', '3': 'reycamila04@gmail.com', '6': 'ivannarisaro@hotmail.com'}, '16:30': [None, 'jul111inv@gmail.com', None, 'reycamila04@gmail.com', 'skere@hotmail.com']}, 'viernes': {'16:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com'], '18:00': [None, None, 'skere@hotmail.com', 'manumanu97@hotmail.com', 'ivannarisaro@hotmail.com'], '9:00': [None, 'skere@hotmail.com', None, 'reycamila04@gmail.com', 'ivannarisaro@hotmail.com']}}}})


class Login():
    def create_user(self, email, password):
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            link = auth.generate_email_verification_link(email)
            self.send_verification_email(email, link)
            print('User created successfully')
        except Exception as e:
            print('Error creating user:', e)

    def send_verification_email(self, email, link):


        load_dotenv()

        EMAIL = os.getenv('EMAIL')
        PASSWORD = os.getenv('PASSWORD')
        
        msg = MIMEText(f'Para entrar a la mejor clase de ceramica verifica tu usuario clickeando este link: {link}')
        msg['Subject'] = 'Email Verification'
        msg['From'] = EMAIL
        msg['To'] = email

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

    def sign_in_with_email_and_password(self, email, password):
        
        
        load_dotenv()
        
        API_KEY = os.getenv("API_KEY")
        
        api_key = API_KEY  # Obtén esto desde la configuración de tu proyecto en la consola de Firebase
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        response = rq.post(url, json=payload)
        data = response.json()

        if 'idToken' in data:
            print('Successfully signed in')
            return data['idToken']
        else:
            print('Error signing in:', data.get('error', {}).get('message'))
            return None

    def get_user_data(self, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            return user.email
        except Exception as e:
            print(e)

    

    def refresh_id_token(self, refresh_token):
        API_KEY = os.getenv("API_KEY")
        url = f'https://securetoken.googleapis.com/v1/token?key={API_KEY}'
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = rq.post(url, data=payload)
        data = response.json()

        if 'id_token' in data:
            return data['id_token'], data['refresh_token']
        else:
            print('Error refreshing token:', data.get('error', {}).get('message'))
            return None, None

    def get_user_data_with_refresh(self, cookies):
        cookie = http.cookies.SimpleCookie()
        cookie.load(cookies)
        id_token = cookie.get("id_token").value if "id_token" in cookie else None
        refresh_token = cookie.get("refresh_token").value if "refresh_token" in cookie else None

        if not id_token:
            return None, None

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            return uid, user.email
        except Exception as e:
            print('Token expired, refreshing token...')
            id_token, refresh_token = self.refresh_id_token(refresh_token)
            if id_token:
                # Aquí deberías establecer las cookies actualizadas
                # por ejemplo, rx.set_cookie("id_token", id_token)
                return self.get_user_data_with_refresh(cookies)
            else:
                print('Failed to refresh token')
                return None, None

    def reserve_turno(self, turno):
        user_id, email = self.get_user_data_with_refresh()
        if user_id:
            FireBase.store_turno(user_id, turno)
            print(f'Turno reservado para {email}')
        else:
            print('Error reservando turno, usuario no autenticado')

login = Login()
        

# print(CookieState.cookie)

# print(login.get_user_data(login.sign_in_with_email_and_password("manumanu97@hotmail.com", "123456789")))


class ReservaCancela(rx.State):
    
    
    async def printt(self):
        printt = printtt()
        return printt

    async def data(self):
        data = await data()
        print(data)
        return data
    
    async def eliminar_usuario(self, semana, dia, hora, usuario):
        eliminar = eliminar_usuarioo(semana, dia, hora, usuario)
        return eliminar

    async def agregar_usuario(self, semana, dia, hora):
        agregar = agregar_usuarioo(semana,dia, hora)
        return agregar
    
def eliminar_usuarioo(semana, dia, hora, usuario):
    firebase.eliminar_usuario_a_horario(semana, dia, hora, usuario)

def agregar_usuarioo(semana, dia, hora):
    firebase.agregar_usuario_a_horario(semana, dia, hora)

async def data():
    return firebase.data()

class Color():
    color_red: str = "red"
    color_green: str = "green"

color = Color()


class ButtonState(rx.State):
    show_text_lunes: bool = False
    show_text_martes: bool = False
    show_text_miercoles: bool = False
    show_text_jueves: bool = False
    show_text_viernes: bool = False

    def toggle_text(self, id):
        if id == 1:
            self.show_text_lunes = not self.show_text_lunes
        elif id == 2:
            self.show_text_martes = not self.show_text_martes
        elif id == 3:
            self.show_text_miercoles = not self.show_text_miercoles
        elif id == 4:
            self.show_text_jueves = not self.show_text_jueves
        elif id == 5:
            self.show_text_viernes = not self.show_text_viernes



@rx.page(
    title="turnos",
    description="Taller de cerámica",
    # on_load=ReservaCancela.data
)
def index() -> rx.Component:
    return rx.box(
        navbar(boton=True),
        
    )



    
@rx.page(
    route="/crear_usuario", 
    title="crear usuario",
    description="Taller de ceramica"
)
def crear_usuario() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            rx.heading("Crea tu usuario"),
            form_create_user(),
            rx.spacer(),
            rx.text("ya tenes un usuario?"),
            iniciar_sesion_button(),
            root_button(),
            width= "100%",
            align= "center"
        ),
    )


@rx.page(
    route="/ingreso", 
    title="ingreso",
    description="Taller de ceramica"
)
def ingreso() -> rx.Component:
    return rx.box(
        rx.center(
        rx.vstack(
            navbar(),
            rx.heading("Ingresa con tu usuario"),
            form_ingresar_user(),
            button_print_cookie(),
            root_button(),
            turnos_button(),
            width= "100%",
            align= "center"
        ),
    ),
    )

@rx.page(
        route="/turnos",
        title="turnos ",
        description="Taller de ceramica"
)
def turnos():
    return rx.box(
        rx.center(
            rx.vstack(
                navbar(),
                prueba(),
                width = "100%"
            )
        )
    )

@rx.page(
        route="/mis_horarios",
        title="mis horarios ",
        description="Taller de ceramica"
)
def mis_horarios():
    horarios = firebase.encontrar_usuario("asd")

    horarios_boxes = [
        rx.box(
            rx.hstack(
            text_box(f"Tienes turno el día {horario.split(',')[1], horario.split(',')[2]} a las {horario.split(',')[3]}"),
            eliminar_usuario_button(horario.split(',')[0], horario.split(',')[1], horario.split(',')[2], "asd")
            )
        )
        for horario in horarios
    ]

    return rx.box(
        rx.center(
            rx.vstack(
                navbar(),  
                rx.heading(rx.text("Tus horarios son :")),  
                rx.heading("Tus horarios son :"), 
                *horarios_boxes,
                width = "100%"  
            )
        )
    )

class PaginacionState(rx.State):
    indice: int = 0  

    def siguiente(self):
        self.indice = (self.indice + 1) % 5

    def anterior(self):
        self.indice = (self.indice - 1) % 5


def prueba():

    return rx.center(
        rx.vstack(
            rx.flex(
                rx.cond(
                PaginacionState.indice == 0,
                links_button1()
                ),
                align="start"
            ),
            rx.flex(
                rx.cond(
                PaginacionState.indice == 1,
                links_button2()
                ),
                align="start"
            ),
            rx.flex(
                rx.cond(
                PaginacionState.indice == 2,
                links_button3()
                ),
                align="start"
            ),
            rx.flex(
                rx.cond(
                PaginacionState.indice == 3,
                links_button4()
                ),
                align="start"
            ),
            rx.flex(
                rx.cond(
                PaginacionState.indice == 4,
                links_button5()
                ),
                align="start"
            ),
            rx.hstack(
                rx.button(rx.icon("arrow-left", color = "black"), on_click=PaginacionState.anterior, style= {"background_color": "#FFFDF4"}),
                rx.button(rx.icon("arrow-right", color = "black"), on_click=PaginacionState.siguiente, style= {"background_color": "#FFFDF4"}),
            ),
            width = "100%",
            # padding_left = "3em",
            # padding_top = "3em"
        ),
    )


class UserState(rx.State):
    email: str = "1"

    @classmethod
    def set_user_email(cls, email: str):
        cls.email = email


class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        username = form_data.get("username")
        password = form_data.get("password")
        login.create_user(username, password)

    def ingresar(self, form_data: dict):
        username = form_data.get("username")
        password = form_data.get("password")
        login.sign_in_with_email_and_password(username, password)
        print(login.sign_in_with_email_and_password(username, password))
        email = login.get_user_data(login.sign_in_with_email_and_password(username, password))
        print(email)
        print(cookie_state.cookie)
        cookie_state.change_cookie(email)
        print(cookie_state.cookie)
        # username = form_data.get("username")
        # password = form_data.get("password")
        # try:
        #     token = login.sign_in_with_email_and_password(username, password)
        #     email = login.get_user_data(token)
        #     UserState.set_user_email(username)  # Almacenar el email en el estado
        #     CookieState.change_cookie(username)
        #     print(UserState.email)
        #     print(CookieState.cookie) # Verificar si el correo se ha guardado correctamente
        # except Exception as e:
        #     print(f"Error al iniciar sesión: {e}")

def text_box(text: str):
    return rx.box(rx.text.strong(text))

    
def links_button1():
    return rx.vstack(
    day_button_lunes1(),
    day_button_martes1(),
    day_button_miercoles1(),
    day_button_jueves1(),
    day_button_viernes1(),
    spacing="2" 
    )

def links_button2():
    return rx.vstack(
    day_button_lunes2(),
    day_button_martes2(),
    day_button_miercoles2(),
    day_button_jueves2(),
    day_button_viernes2(),
    spacing="2" 
    )

def links_button3():
    return rx.vstack(
    day_button_lunes3(),
    day_button_martes3(),
    day_button_miercoles3(),
    day_button_jueves3(),
    day_button_viernes3(),
    spacing="2" 
    )

def links_button4():
    return rx.vstack(
    day_button_lunes4(),
    day_button_martes4(),
    day_button_miercoles4(),
    day_button_jueves4(),
    day_button_viernes4(),
    spacing="2" 
    )

def links_button5():
    return rx.vstack(
    day_button_lunes5(),
    day_button_martes5(),
    day_button_miercoles5(),
    day_button_jueves5(),
    day_button_viernes5(),
    spacing="2" 
    )

def button_print_cookie():
    return rx.center(
        rx.button(
            rx.text("print cookie"),
            width = "13em",
            style= {
                    "background_color": "#383956",
                    "_hover": {
                    "background_color": "#66A9ED"
                    }
                },
            on_click=ReservaCancela.printt
        )
    )

def button_agregar_clase(semana, dia, hora, fecha ):
    
    return rx.center(
        rx.cond(
            firebase.check_cant_users(semana, dia, hora),
            button_green(semana, dia, hora, fecha),
            button_disabled(hora),
        )
    )

def button_green(semana, dia, hora, fecha) -> rx.Component:
    return rx.button(
        rx.text(f"turno del {fecha} las {hora}"),
        on_click=ReservaCancela.agregar_usuario(semana, dia, hora),
        color_scheme=color.color_green,
        width="13em",
    )
    


def button_disabled( hora) -> rx.Component:
    return rx.center(
        rx.button(
            rx.text(f"turno de las {hora}"),
            disabled=True,
            width = "13em"
        )
    )

def eliminar_usuario_button(semana, dia, hora, usuario):
    return rx.button(
        rx.text("Cancelar turno"),
        on_click=ReservaCancela.eliminar_usuario(semana, dia, hora, usuario),
        color_scheme= color.color_red,
        width = "13em"
    )


def mis_horarios_button():
    return rx.center(
        rx.link(
            rx.button(
                rx.text("Mis horarios"),
                width = "13em",
                style= {
                    "background_color": "#383956",
                    "_hover": {
                    "background_color": "#66A9ED"
                    }
                }
            ),
            href="/mis_horarios"
    )   )

def printtt():
    print(cookie_state.cookie)
 

def root_button():
    return rx.center(
        rx.link(
            rx.button(
                rx.text("Pagina inicial"),
                width = "13em",
                style= {
                    "background_color": "#383956",
                    "_hover": {
                    "background_color": "#66A9ED"
                    }
                }
            ),
            href="/"
    )   )

def iniciar_sesion_button():
    return rx.center(
        rx.link(
            rx.button(
                rx.text("iniciar sesion"),
                width = "13em",
                style= {
                    "background_color": "#383956",
                    "_hover": {
                    "background_color": "#66A9ED"
                    }
                }
                ),
                href="/ingreso"
            ),
    )
    
def crear_usuario_button():
    return rx.center(
        rx.link(
                rx.button(
                rx.text("Crea tu propio usuario"),
                width = "13em",
                style= {
                    "background_color": "#383956",
                    "_hover": {
                    "background_color": "#66A9ED"
                    }
                }
                ),
                href="/crear_usuario"
            )
    )

def turnos_button():
    return rx.center(
        rx.link(
                rx.button(
                rx.text("Turnos"),
                width = "13em",
                style= {
                    "background_color": "#383956",
                    "_hover": {
                    "background_color": "#66A9ED"
                    }
                }
                ),
                href="/turnos"
            )
    )

def desplegable_button():
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon("chevron-down", color="white"),
                variant="ghost",
                size="2",
                width="6em",
                style={
                    "background_color": "#383956",
                    "_hover": {
                        "background_color": "#66A9ED"
                    }
                }
            ),
        ),
        rx.menu.content(
            rx.link(
                rx.button(
                    rx.text("turnos"),
                    width="13em",
                    style={
                        "background_color": "#383956",
                        "_hover": {
                            "background_color": "#66A9ED"
                        }
                    }
                ),
                href="/turnos",
                style={"margin_bottom": "0.5em"}  # Añade margen inferior aquí
            ),
            rx.link(
                rx.button(
                    rx.text("mis turnos"),
                    width="13em",
                    style={
                        "background_color": "#383956",
                        "_hover": {
                            "background_color": "#66A9ED"
                        }
                    }
                ),
                href="/mis_horarios",
                style={"margin_bottom": "1.5em",
                "background_color": "#FFFDF4"}  # Añade margen inferior aquí
            ),
        ),
        style={"margin_top": "5.5em",
               "background_color": "#FFFDF4"}  # Añade margen superior al menú desplegable completo
    )


def form_create_user():
    return rx.vstack(
        rx.form(
            rx.form.field(
                rx.form.label("Ingrese su usuario"),
                rx.input(placeholder="Usuario", name="username", color = "black"),
            ),
            rx.form.field(
                rx.form.label("Ingrese su contraseña"),
                rx.input(placeholder="Contraseña", type="password", name="password", color = "black"),
            ),
            rx.form.submit(
                rx.button("Crear usuario", type="submit",
                        style= {
                            "background_color": "#383956",
                            "_hover": {
                            "background_color": "#66A9ED"
                            }
                        }),
                as_child=True,
                on_click=rx.redirect("/"),
            ),
            on_submit=FormState.handle_submit(),
            reset_on_submit=True,
        )
    )

def form_ingresar_user():
    return rx.vstack(
        rx.form(
            rx.form.field(
                rx.form.label("Ingrese su usuario"),
                rx.input(placeholder="Usuario", name="username", color = "black"),
            ),
            rx.form.field(
                rx.form.label("Ingrese su contraseña"),
                rx.input(placeholder="Contraseña", type="password", name="password", color = "black"),
            ),
            rx.form.submit(
                    rx.button("Iniciar sesion", type="submit",
                        style= {
                            "background_color": "#383956",
                            "_hover": {
                            "background_color": "#66A9ED"
                            }
                        }
                ),
                as_child=True,
                on_click=rx.redirect("/"),
            ),
            on_submit=FormState.ingresar(),
            reset_on_submit=True,
        )
    )

def comprobar_usuario():
    return rx.center(
        rx.button(
            rx.text("Comprobar"),

        )
    )
    

def navbar(boton = False) -> rx.Component:
    return rx.box(
            rx.hstack(
                rx.link(
                    rx.text("Taller de ceramica",
                        padding_left="1em"
                    ),
                    href="/"
                ),
                # turnos_button(),
                desplegable_button(),
                rx.spacer(),
            rx.box(
                    rx.cond(
                    boton,
                    rx.hstack(
                    crear_usuario_button(),
                    iniciar_sesion_button(),
                    width = "100%",
                    align_items="end")
                ),
                )
            ),
            width = "100%",
        style=dict(
            font_family="Confortaa-Medium",
            font_size = "1.3em",
            position="sticky",
            bg="#383956",
            padding_y="0.5em",
            padding_x="0.5em",
            z_index="999",
            top="0"
        )
    )




# Modificar las funciones de los botones para incluir las fechas
def day_button_lunes1():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"lunes {fechas[0]}",
                  on_click=ButtonState.toggle_text(1),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_lunes,
            button_agregar_clase("semana1", "lunes", "17:30", fechas[0])
        ),
        spacing="1"
    )

def day_button_martes1():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"martes {fechas[1]}",
                  on_click=ButtonState.toggle_text(2),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_martes,
            rx.hstack(
                button_agregar_clase("semana1", "martes", "10:00", fechas[1]),
                button_agregar_clase("semana1", "martes", "14:00", fechas[1]),
                button_agregar_clase("semana1", "martes", "16:30", fechas[1]),
            )
        ),
        spacing="1"
    )

def day_button_miercoles1():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"miercoles {fechas[2]}",
                  on_click=ButtonState.toggle_text(3),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_miercoles,
            rx.hstack(
                button_agregar_clase("semana1", "miercoles", "9:00", fechas[2]),
                button_agregar_clase("semana1", "miercoles", "14:00", fechas[2]),
                button_agregar_clase("semana1", "miercoles", "16:30", fechas[2]),
            )
        ),
        spacing="1"
    )

def day_button_jueves1():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"jueves {fechas[3]}",
                  on_click=ButtonState.toggle_text(4),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_jueves,
            rx.hstack(
                button_agregar_clase("semana1", "tjueves", "10:00", fechas[3]),
                button_agregar_clase("semana1", "tjueves", "14:00", fechas[3]),
                button_agregar_clase("semana1", "tjueves", "16:30", fechas[3]),
            )
        ),
        spacing="1"
    )

def day_button_viernes1():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"viernes {fechas[4]}",
                  on_click=ButtonState.toggle_text(5),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_viernes,
            rx.hstack(
                button_agregar_clase("semana1", "viernes", "9:00", fechas[4]),
                button_agregar_clase("semana1", "viernes", "16:00", fechas[4]),
                button_agregar_clase("semana1", "viernes", "18:00", fechas[4]),
            )
        ),
        spacing="1"
    )

def day_button_lunes2():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"lunes {fechas[5]}",
                  on_click=ButtonState.toggle_text(1),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_lunes,
            button_agregar_clase("semana2", "lunes", "17:30", fechas[5])
        ),
        spacing="1"
    )

def day_button_martes2():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"martes {fechas[6]}",
                  on_click=ButtonState.toggle_text(2),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_martes,
            rx.hstack(
                button_agregar_clase("semana2", "martes", "10:00", fechas[6]),
                button_agregar_clase("semana2", "martes", "14:00", fechas[6]),
                button_agregar_clase("semana2", "martes", "16:30", fechas[6]),
            )
        ),
        spacing="1"
    )

def day_button_miercoles2():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"miercoles {fechas[7]}",
                  on_click=ButtonState.toggle_text(3),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_miercoles,
            rx.hstack(
                button_agregar_clase("semana2", "miercoles", "9:00", fechas[7]),
                button_agregar_clase("semana2", "miercoles", "14:00", fechas[7]),
                button_agregar_clase("semana2", "miercoles", "16:30", fechas[7]),
            )
        ),
        spacing="1"
    )

def day_button_jueves2():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"jueves {fechas[8]}",
                  on_click=ButtonState.toggle_text(4),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_jueves,
            rx.hstack(
                button_agregar_clase("semana2", "tjueves", "10:00", fechas[8]),
                button_agregar_clase("semana2", "tjueves", "14:00", fechas[8]),
                button_agregar_clase("semana2", "tjueves", "16:30", fechas[8]),
            )
        ),
        spacing="1"
    )

def day_button_viernes2():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"viernes {fechas[9]}",
                  on_click=ButtonState.toggle_text(5),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_viernes,
            rx.hstack(
                button_agregar_clase("semana2", "viernes", "9:00", fechas[9]),
                button_agregar_clase("semana2", "viernes", "16:00", fechas[9]),
                button_agregar_clase("semana2", "viernes", "18:00", fechas[9]),
            )
        ),
        spacing="1"
    )

def day_button_lunes3():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"lunes {fechas[10]}",
                  on_click=ButtonState.toggle_text(1),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_lunes,
            button_agregar_clase("semana3", "lunes", "17:30", fechas[10])
        ),
        spacing="1"
    )

def day_button_martes3():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"martes {fechas[11]}",
                  on_click=ButtonState.toggle_text(2),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_martes,
            rx.hstack(
                button_agregar_clase("semana3", "martes", "10:00", fechas[11]),
                button_agregar_clase("semana3", "martes", "14:00", fechas[11]),
                button_agregar_clase("semana3", "martes", "16:30", fechas[11]),
            )
        ),
        spacing="1"
    )

def day_button_miercoles3():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"miercoles {fechas[12]}",
                  on_click=ButtonState.toggle_text(3),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_miercoles,
            rx.hstack(
                button_agregar_clase("semana3", "miercoles", "9:00", fechas[12]),
                button_agregar_clase("semana3", "miercoles", "14:00", fechas[12]),
                button_agregar_clase("semana3", "miercoles", "16:30", fechas[12]),
            )
        ),
        spacing="1"
    )

def day_button_jueves3():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"jueves {fechas[13]}",
                  on_click=ButtonState.toggle_text(4),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_jueves,
            rx.hstack(
                button_agregar_clase("semana3", "tjueves", "10:00", fechas[13]),
                button_agregar_clase("semana3", "tjueves", "14:00", fechas[13]),
                button_agregar_clase("semana3", "tjueves", "16:30", fechas[13]),
            )
        ),
        spacing="1"
    )

def day_button_viernes3():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"viernes {fechas[14]}",
                  on_click=ButtonState.toggle_text(5),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_viernes,
            rx.hstack(
                button_agregar_clase("semana3", "viernes", "9:00", fechas[14]),
                button_agregar_clase("semana3", "viernes", "16:00", fechas[14]),
                button_agregar_clase("semana3", "viernes", "18:00", fechas[14]),
            )
        ),
        spacing="1"
    )

def day_button_lunes4():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"lunes {fechas[15]}",
                  on_click=ButtonState.toggle_text(1),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_lunes,
            button_agregar_clase("semana4", "lunes", "17:30", fechas[15])
        ),
        spacing="1"
    )

def day_button_martes4():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"martes {fechas[16]}",
                  on_click=ButtonState.toggle_text(2),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_martes,
            rx.hstack(
                button_agregar_clase("semana4", "martes", "10:00", fechas[16]),
                button_agregar_clase("semana4", "martes", "14:00", fechas[16]),
                button_agregar_clase("semana4", "martes", "16:30", fechas[16]),
            )
        ),
        spacing="1"
    )

def day_button_miercoles4():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"miercoles {fechas[17]}",
                  on_click=ButtonState.toggle_text(3),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_miercoles,
            rx.hstack(
                button_agregar_clase("semana4", "miercoles", "9:00", fechas[17]),
                button_agregar_clase("semana4", "miercoles", "14:00", fechas[17]),
                button_agregar_clase("semana4", "miercoles", "16:30", fechas[17]),
            )
        ),
        spacing="1"
    )

def day_button_jueves4():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"jueves {fechas[18]}",
                  on_click=ButtonState.toggle_text(4),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_jueves,
            rx.hstack(
                button_agregar_clase("semana4", "tjueves", "10:00", fechas[18]),
                button_agregar_clase("semana4", "tjueves", "14:00", fechas[18]),
                button_agregar_clase("semana4", "tjueves", "16:30", fechas[18]),
            )
        ),
        spacing="1"
    )

def day_button_viernes4():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"viernes {fechas[19]}",
                  on_click=ButtonState.toggle_text(5),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_viernes,
            rx.hstack(
                button_agregar_clase("semana4", "viernes", "9:00", fechas[19]),
                button_agregar_clase("semana4", "viernes", "16:00", fechas[19]),
                button_agregar_clase("semana4", "viernes", "18:00", fechas[19]),
            )
        ),
        spacing="1"
    )

def day_button_lunes5():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"lunes {fechas[20]}",
                  on_click=ButtonState.toggle_text(1),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_lunes,
            button_agregar_clase("semana5", "lunes", "17:30", fechas[20])
        ),
        spacing="1"
    )

def day_button_martes5():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"martes {fechas[21]}",
                  on_click=ButtonState.toggle_text(2),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_martes,
            rx.hstack(
                button_agregar_clase("semana5", "martes", "10:00", fechas[21]),
                button_agregar_clase("semana5", "martes", "14:00", fechas[21]),
                button_agregar_clase("semana5", "martes", "16:30", fechas[21]),
            )
        ),
        spacing="1"
    )

def day_button_miercoles5():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"miercoles {fechas[22]}",
                  on_click=ButtonState.toggle_text(3),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_miercoles,
            rx.hstack(
                button_agregar_clase("semana5", "miercoles", "9:00", fechas[22]),
                button_agregar_clase("semana5", "miercoles", "14:00", fechas[22]),
                button_agregar_clase("semana5", "miercoles", "16:30", fechas[22]),
            )
        ),
        spacing="1"
    )

def day_button_jueves5():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"jueves {fechas[23]}",
                  on_click=ButtonState.toggle_text(4),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_jueves,
            rx.hstack(
                button_agregar_clase("semana5", "tjueves", "10:00", fechas[23]),
                button_agregar_clase("semana5", "tjueves", "14:00", fechas[23]),
                button_agregar_clase("semana5", "tjueves", "16:30", fechas[23]),
            )
        ),
        spacing="1"
    )

def day_button_viernes5():
    fechas = firebase.obtener_fechas_proximas_semanas()
    return rx.hstack(
        rx.button(f"viernes {fechas[24]}",
                  on_click=ButtonState.toggle_text(5),
                  width="13em",
                  style={
                      "background_color": "#383956",
                      "_hover": {
                          "background_color": "#66A9ED"
                      }
                  }),
        rx.cond(
            ButtonState.show_text_viernes,
            rx.hstack(
                button_agregar_clase("semana5", "viernes", "9:00", fechas[24]),
                button_agregar_clase("semana5", "viernes", "16:00", fechas[24]),
                button_agregar_clase("semana5", "viernes", "18:00", fechas[24]),
            )
        ),
        spacing="1"
    )


BASE_STYLE = {
    "font_family": "1em",
    "font_weight": "300",
    "background_color": "#FFFDF4",
    rx.heading: {
        "color": "#FCFDFD",
        "font_family": "Poppins",
        "font_weight": "500"
    },
    rx.button: {
        "width": "100%",
        "height": "100%",
        "padding": "0.5em",
        "border_radius": "0.8em",
        "white_space": "normal",
        "text_align": "start",
        "--cursor-button": "pointer",
    },
    rx.link: {
        "color": "#FCFDFD",
        "text_decoration": "none",
        "_hover": {}
    }
}


app = rx.App(
    style=BASE_STYLE,
    )
app.add_page(index)
app.add_page(crear_usuario)
app.add_page(ingreso)
app.add_page(mis_horarios)
app.add_page(prueba)

# # app.add_page(user_info)
# # async def main():
# #     # Iniciar la tarea de verificación periódica de la base de datos
# #     asyncio.create_task(check_database_periodically())
# #     app._compile()

# # if name == "main":
# #     asyncio.run(main())
# #"52875400 lucas 12/6"