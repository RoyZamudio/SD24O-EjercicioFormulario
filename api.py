from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os #Para acceder a la ruta del home
import uuid #generar un nombre aleatorio, unico

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    edad:int
    domicilio:str    
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]

@app.post("/fotos")
async def guarda_foto(nombre: str = Form(None),direccion: str = Form(...),foto: UploadFile = File(...),vip: str = Form(None)):
    es_vip = vip == "1"
    print("Nombre:", nombre)
    print("Dirección:", direccion)
    print("VIP:", "Sí" if es_vip else "No")
    
    home_usuario = os.path.expanduser("~")
    ruta_base = f"{home_usuario}/fotos-usuarios-vip" if es_vip else f"{home_usuario}/fotos-usuarios"
    
    os.makedirs(ruta_base, exist_ok=True)

    nombre_archivo = f"{uuid.uuid4()}{os.path.splitext(foto.filename)[1]}"
    ruta_imagen = os.path.join(ruta_base, nombre_archivo)
    
    with open(ruta_imagen, "wb") as archivo_foto:
        contenido = await foto.read()
        archivo_foto.write(contenido)

    print("Guardando la foto en:", ruta_imagen)
    
    respuesta = {
        "Nombre": nombre,
        "Dirección": direccion,
        "VIP": es_vip,
        "Ruta": ruta_imagen
    }
    return respuesta


# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


@app.get("/usuarios/{id}")
def usuario_por_id(id: int):
    print("buscando usuario por id:", id)
    # simulamos consulta a la base:
    return usuarios[id]


@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }

    return compra

@app.get("/usuarios")
def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
    print("lote:",lote, " pag:", pag, " orden:", orden)
    #simulamos la consulta
    return usuarios

@app.post("/usuarios")
def guardar_usuario(usuario:UsuarioBase, parametro1:str):
    print("usuario a guardar:", usuario, ", parametro1:", parametro1)
    #simulamos guardado en la base.
    
    usr_nuevo = {}
    usr_nuevo["id"] = len(usuarios)
    usr_nuevo["nombre"] = usuario.nombre
    usr_nuevo["edad"] = usuario.edad
    usr_nuevo["domicilio"] = usuario.domicilio

    usuarios.append(usuario)

    return usr_nuevo

@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int):
    #simulamos una consulta
    if id>=0 and id< len(usuarios):
        usuario = usuarios[id]
    else:
        usuario = None
    
    if usuario is not None:
        usuarios.remove(usuario)
    
    return {"status_borrado", "ok"}
