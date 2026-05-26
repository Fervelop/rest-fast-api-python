import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Cargar las variables del archivo .env para que esten disponibles en os.getenv.
load_dotenv()

# 2. Obtener las credenciales y datos de conexion desde el entorno.
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 3. Construir la URL de conexion en el formato que entiende SQLAlchemy.
#    mysql+pymysql indica el dialecto MySQL y el driver PyMySQL.
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Crear el engine, que centraliza la comunicacion con la base de datos.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 5. Configurar el generador de sesiones. Cada instancia de SessionLocal
#    representa una sesion de trabajo independiente sobre la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. Base sera la clase padre de los modelos declarativos de SQLAlchemy.
Base = declarative_base()

def get_db():
    """Provee una sesion de base de datos y garantiza su cierre.

    Esta funcion se usa normalmente como dependencia en FastAPI. Abre una
    sesion al inicio de la solicitud, la entrega al endpoint con yield y la
    cierra siempre al finalizar, incluso si ocurre un error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()