# импорт библиотеки для работы со случайными числами
import random

# импорт класса для создания экземпляра FastAPI приложения
from fastapi import FastAPI

# создание экземпляра FastAPI приложения
app = FastAPI()

# обработка запросов к корню приложения
@app.get("/")
def read_root():
    return {"Hello": "World"}

# обработка запросов к специальному пути для получения предсказания модели
# предсказание пока что в виде заглушки со случайной генерацией score
@app.get("/api/public/v1/churn/{user_id}")
def get_prediction_for_item(user_id: str):
    return {"user_id": user_id, "score": random.random()}