from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from datetime import date
from typing import Optional

# --- CONFIGURACIÓN COGNITO  ---
REGION = "us-east-1"
# Tu ID de cliente real
CLIENT_ID = "2u8r33sivddfsghmtlkdhlb2r6" 
# Tu Issuer URL real
COGNITO_ISSUER = "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_SrHVYqKXa"
COGNITO_URL = f"https://cognito-idp.{REGION}.amazonaws.com/"

# --- CONFIGURACIÓN RDS ---
DB_USER = "admin"
DB_PASS = "TuPassword123" 
DB_HOST = "examen-backend2.cg9wc2m6cqtf.us-east-1.rds.amazonaws.com" 
DB_NAME = "examen_backend"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELOS ---
class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    precio = Column(Float)
    fecha_creacion = Column(Date)

# Crear tablas en RDS
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Cursos - Fase 2 AWS Cognito")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- LOGIN REAL CON COGNITO ---
@app.post("/login", tags=["Auth"])
def login_with_cognito(username: str, password: str):
    """
    Este endpoint hace login directamente contra AWS Cognito.
    """
    payload = {
        "AuthParameters": {
            "USERNAME": username,
            "PASSWORD": password
        },
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": CLIENT_ID
    }
    headers = {
        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
        "Content-Type": "application/x-amz-json-1.1"
    }
    
    response = requests.post(COGNITO_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        error_detail = response.json().get("message", "Error de autenticación")
        raise HTTPException(status_code=401, detail=f"Cognito Error: {error_detail}")
    
    # Esto te devuelve el AccessToken, IdToken y RefreshToken
    return response.json().get("AuthenticationResult")

# --- ENDPOINTS DE NEGOCIO ---

@app.get("/courses", tags=["Cursos"])
def get_courses(
    categoria: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Curso)
    if categoria:
        query = query.filter(Curso.categoria_id == categoria)
    if fecha_inicio and fecha_fin:
        query = query.filter(Curso.fecha_creacion.between(fecha_inicio, fecha_fin))
    return query.all()

@app.post("/courses", status_code=201, tags=["Cursos"])
def create_course(nombre: str, desc: str, cat_id: int, precio: float, db: Session = Depends(get_db)):
    nuevo = Curso(nombre=nombre, descripcion=desc, categoria_id=cat_id, precio=precio, fecha_creacion=date.today())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"status": "success", "id": nuevo.id}

@app.post("/courses/categories", status_code=201, tags=["Categorías"])
def create_category(nombre: str, db: Session = Depends(get_db)):
    nueva = Categoria(nombre=nombre)
    db.add(nueva)
    db.commit()
    return {"message": "Categoría creada"}