from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import LoginRequest, TokenResponse, TokenData
from app.core.security import create_access_token, verify_password, hash_password
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Usuario mock de prueba para validar el flujo
USUARIO_TEST = {
    "email": "admin@techflow.com",
    "password_hash": hash_password("admin123"),
    "rol": "administrador"
}


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    """Endpoint para autenticarse y recibir un Bearer Token JWT."""
    if credentials.email != USUARIO_TEST["email"] or not verify_password(credentials.password, USUARIO_TEST["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (email o contraseña inválidos)."
        )
    
    token = create_access_token(subject=credentials.email)
    return TokenResponse(access_token=token)


@router.get("/me")
def get_perfil_autenticado(current_user: TokenData = Depends(get_current_user)):
    """Endpoint protegido: sólo accesible con Token JWT válido en Header."""
    return {
        "mensaje": "Acceso concedido",
        "usuario": current_user.email
    }