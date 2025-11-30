
# # backend/app.py
# from fastapi import FastAPI, BackgroundTasks, HTTPException
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# import os
# import joblib

# # -----------------------------
# # INTERNAL IMPORTS
# # -----------------------------
# from src.data_ingestion.fetch_news import fetch_news_for_country
# from src.ml_models.risk_predictor import compute_risk_from_news
# from src.utils.store_history import store_risk, init_db
# from src.utils.scheduler import start_scheduler, stop_scheduler

# # Routers
# from app.routes.history import router as history_router
# from app.routes.global_summary import router as global_summary_router

# # ML training + predictor functions
# from ml.train import train as train_model
# from deployed_model import predict_text, predict_from_features

# # -----------------------------
# # ENV + APP INIT
# # -----------------------------
# load_dotenv()
# app = FastAPI()
# from app.routes.orders import router as orders_router
# from app.routes.shipments import router as shipments_router
# from app.routes.inventory import router as inventory_router
# from app.routes.auth import router as auth_router

# app.include_router(orders_router, prefix="/api")
# app.include_router(shipments_router, prefix="/api")
# app.include_router(inventory_router, prefix="/api")
# app.include_router(auth_router, prefix="")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(history_router, prefix="/api")
# app.include_router(global_summary_router, prefix="/api")


# # -----------------------------
# # MODEL LOADING
# # -----------------------------
# MODEL_PATH = "backend/ml/model.pkl"
# VECTORIZER_PATH = "backend/ml/vectorizer.pkl"

# try:
#     model = joblib.load(MODEL_PATH)
#     vectorizer = joblib.load(VECTORIZER_PATH)
#     HAS_DEPLOYED_MODEL = True
#     print("✅ ML model loaded successfully.")
# except:
#     model = None
#     vectorizer = None
#     HAS_DEPLOYED_MODEL = False
#     print("⚠ No trained ML model found. Using heuristic only.")


# # -----------------------------
# # BASIC TEST ROUTE
# # -----------------------------
# @app.get("/api/hello")
# def root():
#     return {"message": "Backend connected successfully 🚀"}


# # -----------------------------
# # ANALYZE ROUTE
# # -----------------------------
# class CountryData(BaseModel):
#     country: str

# @app.post("/api/analyze")
# def analyze_data(data: CountryData):
#     country = data.country
#     articles = fetch_news_for_country(country, page_size=12)

#     combined = "\n".join(
#         (a.get("title") or "") + " " + (a.get("description") or "")
#         for a in articles
#     )

#     # -----------------------------
#     # AI MODEL PREDICTION
#     # -----------------------------
#     if HAS_DEPLOYED_MODEL:
#         try:
#             X = vectorizer.transform([combined])
#             risk_score = float(model.predict(X)[0])

#             heuristic = compute_risk_from_news(articles)

#             response = {
#                 "country": country,
#                 "risk_score": round(risk_score, 2),
#                 "status": "AI Model",
#                 "risk_label": heuristic.get("status"),
#                 "explanation": heuristic.get("explanation", ""),
#                 "top_risk_factors": heuristic.get("top_risk_factors", []),
#                 "top_articles": heuristic.get("top_articles", []),
#             }

#             store_risk(country, response["risk_score"])
#             return response

#         except Exception as e:
#             print("⚠ ML model error:", e)

#     # -----------------------------
#     # FALLBACK HEURISTIC
#     # -----------------------------
#     risk = compute_risk_from_news(articles)

#     try:
#         store_risk(country, risk["risk_score"])
#     except:
#         pass

#     return {
#         "country": country,
#         "risk_score": risk["risk_score"],
#         "status": risk["status"],
#         "risk_label": risk["status"],
#         "explanation": "Heuristic-based explanation.",
#         "top_risk_factors": risk["top_risk_factors"],
#         "top_articles": risk["top_articles"],
#     }


# # -----------------------------
# # RISK SCORE (simple)
# # -----------------------------
# @app.get("/api/risk_score/{country}")
# def get_risk_score(country: str):
#     articles = fetch_news_for_country(country, page_size=5)
#     risk = compute_risk_from_news(articles)
#     return {
#         "country": country,
#         "risk_score": risk.get("risk_score"),
#         "status": risk.get("status"),
#     }


# # -----------------------------
# # STARTUP / SHUTDOWN TASKS
# # -----------------------------
# @app.on_event("startup")
# def on_startup():
#     init_db()
#     try:
#         start_scheduler(interval_minutes=360)
#     except Exception as e:
#         print("Scheduler error:", e)

# @app.on_event("shutdown")
# def _on_shutdown():
#     try:
#         stop_scheduler()
#     except:
#         pass


# # -----------------------------
# # TRAIN MODEL
# # -----------------------------
# @app.post("/api/train")
# def api_train(background: bool = True, background_tasks: BackgroundTasks = None):
#     if background and background_tasks:
#         background_tasks.add_task(train_model, True)
#         return {"status": "training_started_background"}

#     model, metrics = train_model(save_model=True)
#     return {"status": "trained", "metrics": metrics}


# # -----------------------------
# # PREDICT ENDPOINT
# # -----------------------------
# class PredictRequest(BaseModel):
#     country: str | None = None
#     text: str | None = None
#     features: dict | None = None

# @app.post("/api/predict")
# def api_predict(req: PredictRequest):
#     try:
#         if req.features:
#             out = predict_from_features(req.features)
#         else:
#             combined = (req.text or "") + (" " + req.country if req.country else "")
#             out = predict_text(combined, extras={})

#         try:
#             store_risk(req.country or "UNKNOWN", out["risk_score"])
#         except:
#             pass

#         return out

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()    

# class User(BaseModel):
#     email: str
#     password: str

# @app.post("/login")
# def login(user: User):
#     return {"message": "Login successful", "email": user.email}

# @app.post("/register")
# def register(user: User):
#     return {"message": "User registered", "email": user.email}


# class RegisterModel(BaseModel):
#     name: str
#     email: str
#     password: str

# @app.post("/register")
# async def register_user(user: RegisterModel):
#     return {"message": "User registered successfully"}

# from fastapi import FastAPI
# from auth import router as auth_router

# app = FastAPI()

# # include auth routes
# app.include_router(auth_router)


# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class RegisterModel(BaseModel):
#     name: str
#     email: str
#     password: str

# @app.post("/register")
# def register_user(user: RegisterModel):
#     return {"message": "ok"}


# backend/app.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import joblib

# -----------------------------
# INTERNAL IMPORTS
# -----------------------------
from src.data_ingestion.fetch_news import fetch_news_for_country
from src.ml_models.risk_predictor import compute_risk_from_news
from src.utils.store_history import store_risk, init_db
from src.utils.scheduler import start_scheduler, stop_scheduler

# Routers
from app.routes.history import router as history_router
from app.routes.global_summary import router as global_summary_router
from app.routes.orders import router as orders_router
from app.routes.shipments import router as shipments_router
from app.routes.inventory import router as inventory_router
from app.routes.auth import router as auth_router

# ML training + predictor functions
from ml.train import train as train_model
from deployed_model import predict_text, predict_from_features

# -----------------------------
# ENV + APP INIT
# -----------------------------
load_dotenv()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders_router, prefix="/api")
app.include_router(shipments_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(global_summary_router, prefix="/api")
import os

# -----------------------------
# MODEL LOADING
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = "backend/ml/model.pkl"
VECTORIZER_PATH = "backend/ml/vectorizer.pkl"

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    HAS_DEPLOYED_MODEL = True
    print("✅ ML model loaded successfully.")
except:
    model = None
    vectorizer = None
    HAS_DEPLOYED_MODEL = False
    print("⚠ No trained ML model found. Using heuristic only.")

# -----------------------------
# BASIC TEST ROUTE
# -----------------------------
@app.get("/api/hello")
def root():
    return {"message": "Backend connected successfully 🚀"}

# -----------------------------
# ANALYZE ROUTE
# -----------------------------
class CountryData(BaseModel):
    country: str

@app.post("/api/analyze")
def analyze_data(data: CountryData):
    country = data.country
    articles = fetch_news_for_country(country, page_size=12)

    combined = "\n".join(
        (a.get("title") or "") + " " + (a.get("description") or "")
        for a in articles
    )

    # AI MODEL PREDICTION
    if HAS_DEPLOYED_MODEL:
        try:
            X = vectorizer.transform([combined])
            risk_score = float(model.predict(X)[0])
            heuristic = compute_risk_from_news(articles)

            response = {
                "country": country,
                "risk_score": round(risk_score, 2),
                "status": "AI Model",
                "risk_label": heuristic.get("status"),
                "explanation": heuristic.get("explanation", ""),
                "top_risk_factors": heuristic.get("top_risk_factors", []),
                "top_articles": heuristic.get("top_articles", []),
            }

            store_risk(country, response["risk_score"])
            return response

        except Exception as e:
            print("⚠ ML model error:", e)

    # FALLBACK HEURISTIC
    risk = compute_risk_from_news(articles)
    try:
        store_risk(country, risk["risk_score"])
    except:
        pass

    return {
        "country": country,
        "risk_score": risk["risk_score"],
        "status": risk["status"],
        "risk_label": risk["status"],
        "explanation": "Heuristic-based explanation.",
        "top_risk_factors": risk["top_risk_factors"],
        "top_articles": risk["top_articles"],
    }

# -----------------------------
# RISK SCORE (simple)
# -----------------------------
@app.get("/api/risk_score/{country}")
def get_risk_score(country: str):
    articles = fetch_news_for_country(country, page_size=5)
    risk = compute_risk_from_news(articles)
    return {
        "country": country,
        "risk_score": risk.get("risk_score"),
        "status": risk.get("status"),
    }

# -----------------------------
# STARTUP / SHUTDOWN TASKS
# -----------------------------
@app.on_event("startup")
def on_startup():
    init_db()
    try:
        start_scheduler(interval_minutes=360)
    except Exception as e:
        print("Scheduler error:", e)

@app.on_event("shutdown")
def on_shutdown():
    try:
        stop_scheduler()
    except:
        pass

# -----------------------------
# TRAIN MODEL
# -----------------------------
@app.post("/api/train")
def api_train(background: bool = True, background_tasks: BackgroundTasks = None):
    if background and background_tasks:
        background_tasks.add_task(train_model, True)
        return {"status": "training_started_background"}

    model, metrics = train_model(save_model=True)
    return {"status": "trained", "metrics": metrics}

# -----------------------------
# PREDICT ENDPOINT
# -----------------------------
class PredictRequest(BaseModel):
    country: str | None = None
    text: str | None = None
    features: dict | None = None

@app.post("/api/predict")
def api_predict(req: PredictRequest):
    try:
        if req.features:
            out = predict_from_features(req.features)
        else:
            combined = (req.text or "") + (" " + req.country if req.country else "")
            out = predict_text(combined, extras={})

        try:
            store_risk(req.country or "UNKNOWN", out["risk_score"])
        except:
            pass

        return out

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# USER AUTH ROUTES
# -----------------------------
class RegisterModel(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


@app.post("/login")
def login_user(user: UserLogin):
    # Here you can add DB/auth logic
    return {"message": "Login successful", "email": user.email}

@app.get("/test")
def test():
    return {"message": "Backend connected successfully!"}


# # main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ------------------- CORS -------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # frontend dev URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # -------------------------------------------

# # Example route
# @app.get("/hello")
# async def hello():
#     return {"message": "Hello from FastAPI!"}
