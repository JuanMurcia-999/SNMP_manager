from fastapi import FastAPI, Request
from Servicio.Utils.Register import Writer,Read
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from datetime import datetime
import time
import logging



from Servicio.function import create_instance_startup, Exit_service

from Servicio.router.agents_router import router as agents_router
from Servicio.router.features_router import router as features_router
from Servicio.router.aditionals_router import router as aditional_router
from Servicio.router.history_router import router as history_router
from Servicio.router.manageables_router import router as manageable_router
from Servicio.router.alarms_router import router as alarms_router
from Servicio.router.traps_router import router as traps_router
from Servicio.router.Login import router as Login
from Servicio.router.user import router as user

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan function started")
    await create_instance_startup()
    # asyncio.create_task(Ping().Exectping())
    print("Lifespan function finished")
    await Read()
    try:
        Writer(f"\ndatestartup = : {datetime.now()}\n")
        start_time = time.time()
        yield
    finally:
        end_time = time.time()
        Writer(f"datestop = : {datetime.now()}\n")
        Writer(f"totaltime = {end_time - start_time}\n\n")
        await Exit_service()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(lifespan=lifespan)



# "http://192.168.20.9:8080"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log detalles de la solicitud
    logger.info(f"URL: {request.url}")
    logger.info(f"Método: {request.method}")
    logger.info(f"Encabezados: {dict(request.headers)}")
    
    # Leer el cuerpo de la solicitud (si existe)
    body = await request.body()
    logger.info(f"Cuerpo: {body.decode('utf-8')}")

    # Pasar la solicitud al siguiente middleware/controlador
    response = await call_next(request)

    # Log detalles de la respuesta
    logger.info(f"Estado de la respuesta: {response.status_code}")
    return response


app.include_router(agents_router)
app.include_router(features_router)
app.include_router(aditional_router)
app.include_router(history_router)
app.include_router(manageable_router)
app.include_router(alarms_router)
app.include_router(traps_router)
app.include_router(Login)
app.include_router(user)

