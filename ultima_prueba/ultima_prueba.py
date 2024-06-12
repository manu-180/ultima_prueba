import reflex as rx
import firebase_admin
import os
import asyncio
import requests as rq
import re
import smtplib
import http.cookies
from firebase_admin import auth, db, credentials
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import time


async def check_database_periodically():
    while True:
        firebase = FireBase()
        data = firebase.data()
        rx.State.update_forward_refs()  
        await asyncio.sleep(10)  

class Horarios(rx.Base):
    id: int
    horario: str
    usuarios: list

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

firebase_sdk = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(firebase_sdk, {"databaseURL": DATABASE_URL})

# ref = db.reference("/Horarios")
# ref.push({"id": 1, "horario":"12:00", "usuarios": ["julinv@hotmail.com"]})
# ref.push({"id": 2, "horario":"14:00", "usuarios": ["julinv@hotmail.com"]})
# ref.push({"id": 3, "horario":"16:00", "usuarios": ["julinv@hotmail.com"]})
# ref.push({"id": 4, "horario":"18:00", "usuarios": ["julinv@hotmail.com"]})
# ref.push({"id": 5, "horario":"20:00", "usuarios": ["julinv@hotmail.com"]})

class CookieState(rx.State):
    cookie: str = rx.Cookie("")

class FireBase():
    ref = db.reference("/Horarios")

    def data(self):
        data = self.ref.get("-NzBFPwsONhMP5SKqs9u")
        dict_data = data[0]
        class_data = []

        for clave, valor in dict_data.items():
            class_data.append(Horarios(
                id=valor["id"],
                horario=valor["horario"],
                usuarios=valor["usuarios"]
            ))
        return class_data

    def horarios(self):
        horarios = []
        for i in self.data():
            horarios.append(i.horario)
        return horarios

    def unico_horario(self, id):
        for i in self.data():
            if i.id == id:
                return i.horario

    def cant_users(self, id) -> int:
        for i in self.data():
            if i.id == id:
                lista_filtrada = []
                lista_usuarios = i.usuarios
                for usuario in lista_usuarios:
                    if usuario != None:
                        lista_filtrada.append(usuario)
        return len(lista_filtrada)
                        

    def check_cant_users(self, id):
        if self.cant_users(id) < 4:
            return True
        else: return False

    def agregar_usuario_a_horario(self, id, nuevo_usuario):
        usuarios_ref = db.reference(f'/Horarios/{self.buscar_horario(id)}/usuarios')
        try:
            usuarios_diccionario = usuarios_ref.get()
            lista_usuarios = list(usuarios_diccionario.values())
            if nuevo_usuario not in lista_usuarios:
                lista_usuarios.append(nuevo_usuario)
                usuarios_ref.set(lista_usuarios)
            else:
                print("Este usuario ya esta en la clase")
        except:
            if nuevo_usuario not in usuarios_diccionario:
                usuarios_diccionario.append(nuevo_usuario)
                if self.cant_users(id) < 4:
                    usuarios_ref.set(usuarios_diccionario)
                else:
                    print("La clase está llena")

    def buscar_horario(self, id):
        data = self.ref.get("-NzBFPwsONhMP5SKqs9u")
        dict_data = data[0]
        list_keys = list(dict_data.keys())
        for index, i in enumerate(list_keys):
            if index + 1 == id :
                return i
        

    def reservar(self, id, new_user):
        data = self.ref.get("-NzBFPwsONhMP5SKqs9u")
        dict_data = data[0]
        for clave, valor in dict_data.items():
            if valor["id"] == id:
                usuarios = self.ref.child(clave)
                dict_users = valor["usuarios"]
                dict_values = dict_users.values()
                list_users = []
                for i in dict_values:
                    list_users.append(i)
                if self.cant_users(id) < 4:
                    list_users.append(new_user)
                    usuarios.update({"usuarios": list_users})
                else:
                    print("La clase está llena")

    def cancelar(self, id):
        data = self.ref.get("-NzBFPwsONhMP5SKqs9u")
        dict_data = data[0]
        for clave, valor in dict_data.items():
            if valor["id"] == id:
                usuarios = self.ref.child(clave)
                contador = valor["cant_users"]
                if contador > 0:
                    usuarios.update({"cant_users": contador - 1})
    
    def store_turno(user_id, turno):
        ref = db.reference(f'Horarios/{user_id}')
        ref.push(turno)

    def get_turnos(user_id):
        ref = db.reference(f'Horarios/{user_id}')
        return ref.get()

    def get_user_data(id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            return uid, user.email
        except Exception as e:
            print('Error fetching user data:', e)
            return None, None

firebase = FireBase()


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
            print('Error fetching user data:', e)

    

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
    
    async def reservar_turno(self, id: int) -> list:
        reservar_la_clase = firebase.reservar(id)
        return reservar_la_clase


    async def cancelar_turno(id: int):
        cancelar_la_clase = firebase.cancelar(id)
        return cancelar_la_clase
    
    async def printt(self):
        printt = printtt()
        return printt

    async def data(self):
        data = await data()
        print(data)
        return data
    
    async def agregar_usuario(self, id):
        agregar = agregar_usuarioo(id)
        return agregar
    
def agregar_usuarioo(id):
    user = login.get_user_data(CookieState.cookie)
    firebase.agregar_usuario_a_horario(id, user)

async def data():
    return firebase.data()

class Color():
    color_red: str = "red"
    color_green: str = "green"

color = Color()

@rx.page(
    title="turnos",
    description="Taller de cerámica",
    # on_load=ReservaCancela.data
)
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            crear_usuario_button(),
            rx.divider(),
            button_agregar_clase(1),
            button_agregar_clase(2),
            button_agregar_clase(3),
            button_agregar_clase(4),
            button_agregar_clase(5)
        )
    )



    
@rx.page(
    route="/crear_usuario", 
    title="crear usuario",
    description="Taller de ceramica"
)
def crear_usuario() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Crea tu usuario"),
            form_create_user(),
            iniciar_sesion_button(),
            root_button()
        )
    )

@rx.page(
    route="/ingreso", 
    title="ingreso",
    description="Taller de ceramica"
)
def ingreso() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Ingresa con tu usuario"),
            form_ingresar_user(),
            button_print_cookie(),
            root_button()
        )
    )



class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        """Manejar la sumisión del formulario."""
        self.form_data = form_data
        username = form_data.get("username")
        password = form_data.get("password")
        login.create_user(username,password)

    def ingresar(self, form_data: dict):
        username = form_data.get("username")
        password = form_data.get("password")
        login.sign_in_with_email_and_password(username, password)
        CookieState.cookie = login.sign_in_with_email_and_password(username, password)
        print(CookieState.cookie)

def button_print_cookie():
    return rx.center(
        rx.button(
            rx.text("print cookie"),
            on_click=ReservaCancela.printt
        )
    )

def button_agregar_clase(id):
    return rx.center(
        rx.button(
            rx.text(f"clase de las {firebase.unico_horario(id)}"),
            on_click=ReservaCancela.agregar_usuario(id)
        )
    )

def printtt():
    print(login.get_user_data(CookieState.cookie))

def root_button():
    return rx.center(
        rx.link(
            rx.button(
                rx.text("Horarios")
            ),
            href="/"
    )   )

def iniciar_sesion_button():
    return rx.center(
        rx.link(
            rx.button(
                rx.text("iniciar sesion")
                ),
                href="/ingreso"
            ),
    )
    
def crear_usuario_button():
    return rx.center(
        rx.link(
                rx.button(
                rx.text(
                    "Crea tu propio usuario"
                    )
                ),
                href="/crear_usuario"
            )
    )


def form_create_user():
    return rx.vstack(
        rx.form(
            rx.form.field(
                rx.form.label("Ingrese su usuario"),
                rx.input(placeholder="Usuario", name="username"),
            ),
            rx.form.field(
                rx.form.label("Ingrese su contraseña"),
                rx.input(placeholder="Contraseña", type="password", name="password"),
            ),
            rx.form.submit(
                rx.button("Crear usuario", type="submit"),
                as_child=True,
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
                rx.input(placeholder="Usuario", name="username"),
            ),
            rx.form.field(
                rx.form.label("Ingrese su contraseña"),
                rx.input(placeholder="Contraseña", type="password", name="password"),
            ),
            rx.form.submit(
                rx.button("Iniciar sesion", type="submit"),
                as_child=True,
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
    

def button_green(text, id) -> rx.Component:
    return rx.button(
        rx.text(text),
        on_click=ReservaCancela.reservar_turno(id),
        color_scheme=color.color_green
    )

def button_red(text, id) -> rx.Component:
    return rx.center(
        rx.button(
            rx.text(text),
            disabled=True,
        ),
        rx.button(
            rx.text("¿Cancelar esta clase?"),
            on_click=ReservaCancela.cancelar_turno(id)
        ),
        rx.vstack(
            rx.text("(Si no cancelas con un día de anticipación",
                    size="1",
                    spacing="0px",
                    padding="0px",
                    margin="0px"),
            rx.text("no podrás recuperar la clase)",
                    size="1",
                    spacing="0px",
                    padding="0px",
                    margin="0px"
            )
        )
    )

def button(id):
    return rx.cond(
        firebase.check_cant_users(id),
        button_green(f"Turno de las {firebase.unico_horario(id)}", id),
        button_red(f"Turno de las {firebase.unico_horario(id)}", id)
    )

app = rx.App()
app.add_page(index)
app.add_page(crear_usuario)
app.add_page(ingreso)
# app.add_page(user_info)
# async def main():
#     # Iniciar la tarea de verificación periódica de la base de datos
#     asyncio.create_task(check_database_periodically())
#     app._compile()

# if name == "main":
#     asyncio.run(main())