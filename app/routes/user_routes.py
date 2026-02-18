@router.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, email FROM usuarios WHERE email = %s AND contrasena = %s",
            (user.usuario, user.contrasena)
        )

        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        token = create_access_token({"sub": result[1]})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        cursor.close()
        conn.close()





