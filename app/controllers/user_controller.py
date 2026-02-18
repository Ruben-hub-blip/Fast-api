import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.user_model import User
from fastapi.encoders import jsonable_encoder

class UserController:
        
    def create_user(self, user: User):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre,apellido,cedula,edad,usuario,contrasena) VALUES (%s, %s, %s, %s, %s ,%s)", (user.nombre, user.apellido, user.cedula, user.edad, user.usuario, user.contrasena))
            conn.commit()
            conn.close()
            return {"resultado": "Usuario creado"}
        except psycopg2.Error as err:
            conn.rollback()
        finally:
            conn.close()
        

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id':int(result[0]),
                    'nombre':result[1],
                    'apellido':result[2],
                    'cedula':result[3],
                    'edad':int(result[4]),
                    'usuario':result[5],
                    'contrasena':result[6]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            conn.rollback()
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id':data[0],
                    'nombre':data[1],
                    'cedula':data[2],
                    'edad':data[3],
                    'usuario':data[4],
                    'contrasena':data[5]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            conn.rollback()
        finally:
            conn.close()

    def update_user(self, user_id: int, user: User):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s,
                    apellido = %s,
                    cedula = %s,
                    edad = %s,
                    usuario = %s,
                    contrasena = %s
                WHERE id = %s
            """, (
                user.nombre,
                user.apellido,
                user.cedula,
                user.edad,
                user.usuario,
                user.contrasena,
                user_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

            return {"resultado": "Usuario actualizado correctamente"}

        except psycopg2.Error as err:
            conn.rollback()

        finally:
            conn.close()

    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

            return {"resultado": "Usuario eliminado correctamente"}

        except psycopg2.Error as err:
            conn.rollback()

        finally:
            conn.close()
    
##user_controller = UserController()