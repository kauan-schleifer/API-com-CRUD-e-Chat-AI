from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import google.generativeai as genai

# ========== CONFIG GERAL ==========
DATABASE_URL = "sqlite:///./usuarios.db"

# ========== CONFIG DB ==========
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ========== MODELO DB ==========
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    idade = Column(Integer)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# ========== SCHEMAS ==========
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    idade: int

class UsuarioOut(UsuarioCreate):
    id: int

# ========== APP ==========
app = FastAPI(title="API com CRUD e Chat AI")

# Página inicial com HTML básico
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>FastAPI + Gemini</title>
        </head>
        <body style='font-family: sans-serif; text-align: center; margin-top: 50px;'>
            <h1>API com CRUD</h1>
            <p>Acesse a documentação interativa em:</p>
            <a href='/docs' style='font-size: 20px;'>/docs</a>
        </body>
    </html>
    """

# ========== DEPENDÊNCIA ==========
# Função para obter a sessão do banco de dados

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== CRUD ==========
# Criar usuário
@app.post("/usuarios", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Ler usuário por ID
@app.get("/usuarios/{usuario_id}", response_model=UsuarioOut)
def ler_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# Atualizar usuário
@app.put("/usuarios/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario(usuario_id: int, dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario

# Deletar usuário
@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return {"ok": True}

# ========== CHAT COM GEMINI ==========
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    prompt = request.prompt.lower()

    # INTEGRAÇÃO DO CHAT COM O CRUD
    if "quantos usuários" in prompt:
        total = db.query(Usuario).count()
        return {"resposta": f"Há {total} usuários cadastrados."}

    elif "listar usuários" in prompt:
        usuarios = db.query(Usuario).all()
        return {"resposta": [u.nome for u in usuarios]}

    elif "apagar usuário" in prompt:
        try:
            partes = prompt.split("usuário")[-1].strip()
            id_ = int(partes)
            usuario = db.query(Usuario).filter(Usuario.id == id_).first()
            if not usuario:
                return {"resposta": f"Usuário com ID {id_} não encontrado."}
            db.delete(usuario)
            db.commit()
            return {"resposta": f"Usuário com ID {id_} apagado com sucesso."}
        except:
            return {"resposta": "Erro ao interpretar ID para apagar usuário."}

    # Criar usuario pelo Chat
    elif "criar usuário" in prompt:
        try:
            import re
            match = re.search(r"criar usuário (.+?) com email (.+?) e idade (\d+)", prompt)
            if match:
                nome, email, idade = match.groups()
                novo_usuario = Usuario(nome=nome.strip(), email=email.strip(), idade=int(idade))
                db.add(novo_usuario)
                db.commit()
                db.refresh(novo_usuario)
                return {"resposta": f"Usuário {nome} criado com sucesso com ID {novo_usuario.id}."}
            else:
                return {"resposta": "Formato inválido. Use: criar usuário NOME com email EMAIL e idade IDADE"}
        except Exception as e:
            return {"resposta": f"Erro ao criar usuário: {e}"}

    # Resposta genérica da IA
    try:
        resposta = model.generate_content(request.prompt)
        print("Resposta da IA:")
        print(resposta.text)
    except Exception as e:
        print("Erro ao chamar a IA:")
        print(e)
