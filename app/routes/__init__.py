# Endpoint de prueba
@router.get("/login-test")
async def login_test():
    return {"mensaje": "Endpoint de login funcionando"}
