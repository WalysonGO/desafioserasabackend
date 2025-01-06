from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.user_controller import user_router
from app.controllers.debt_controller import debt_router
from app.database import Base, engine, get_db
from app.services.user_service import update_overdue_debts
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.env_loader import load_env

# Carregando as variáveis de ambiente
load_env()

# Inicializando o banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inicializa o agendador
scheduler = BackgroundScheduler()

# Função que será chamada pelo agendador
def scheduled_task():
    db = next(get_db())
    update_overdue_debts(db)

# Adiciona a tarefa ao agendador para ser executada a cada minuto
scheduler.add_job(scheduled_task, 'interval', hours=1)
scheduler.start()

# Certifique-se de que o agendador é parado corretamente ao encerrar a aplicação
import atexit
atexit.register(lambda: scheduler.shutdown())

# Configurando CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=dict)
def hello_world():
    return {"message": "Hello, World! 👋 Desafio Técnico SERASA."}

# Rotas da API
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(debt_router, prefix="/debts", tags=["Debts"])
