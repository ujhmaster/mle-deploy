from catboost import CatBoostClassifier

def load_churn_model(model_path: str):
    """Загружаем обученную модель оттока.
    Args:
        model_path (str): Путь до модели.
    """
    try:
        model = CatBoostClassifier()
        model.load_model(model_path)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Failed to load model: {e}")
    return model

if __name__ == "__main__":
    # вызовите функцию load_churn_model с нужным путём
    model = load_churn_model(model_path='models/catboost_churn_model.bin')
    # выведите параметры модели через print(f"Model parameter names: {}") 
    print(f"Model parameter names: {model.feature_names_}") 