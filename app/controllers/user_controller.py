import psycopg
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.user_model import User
from fastapi.encoders import jsonable_encoder


class UserController:

    def create_user(self, user: User):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO usuarios
                (nombre, apellido, cedula, edad, email, contrasena)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user.nombre,
                user.apellido,
                user.cedula,
                user.edad,
                user.email,
                user.contrasena
            ))

            conn.commit()
            return {"resultado": "Usuario creado"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_user(self, user_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="User not found")

            content = {
                "id": result[0],
                "nombre": result[1],
                "apellido": result[2],
                "cedula": result[3],
                "edad": result[4],
                "email": result[5],
                "contrasena": result[6]
            }

            return jsonable_encoder(content)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_users(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios")
            results = cursor.fetchall()

            payload = []

            for row in results:
                payload.append({
                    "id": row[0],
                    "nombre": row[1],
                    "apellido": row[2],
                    "cedula": row[3],
                    "edad": row[4],
                    "email": row[5],
                    "contrasena": row[6]
                })

            return {"resultado": jsonable_encoder(payload)}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def update_user(self, user_id: int, user: User):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s,
                    apellido = %s,
                    cedula = %s,
                    edad = %s,
                    email = %s,
                    contrasena = %s
                WHERE id = %s
            """, (
                user.nombre,
                user.apellido,
                user.cedula,
                user.edad,
                user.email,
                user.contrasena,
                user_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

            return {"resultado": "Usuario actualizado"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def delete_user(self, user_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

            return {"resultado": "Usuario eliminado"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

