"""Класс FastApiHandler, который обрабатывает запросы API."""

from catboost import CatBoostClassifier

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "user_id": int,
            "model_params": dict
        }
        self.err = []

        self.model_path = "../models/catboost_churn_model.bin"
        self.load_churn_model(model_path=self.model_path)
        
        # необходимые параметры для предсказаний модели оттока
        self.required_model_params = [
                'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Type', 'PaperlessBilling', 'PaymentMethod', 
                'MonthlyCharges', 'TotalCharges', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'days', 'services'
            ]
        
    def load_churn_model(self, model_path: str):
        """Загружаем обученную модель оттока.
            Args:
                model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostClassifier()
            self.model.load_model(model_path)
            print('model loaded')
            print("model fetures list:", self.model.feature_names_)
        except Exception as e:
            self.err.append(f"Failed to load model: {e}")

    def churn_predict(self, model_params: dict) -> float:
        """Предсказываем вероятность оттока.

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            float - вероятность оттока от 0 до 1
        """
        param_values_list = list(model_params.values())
        return self.model.predict_proba(param_values_list)[1]
        
    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора параметров.
            Args:
                query_params (dict): Параметры запроса.
                
            Returns:
                bool: True - если есть нужные параметры, False - иначе
        """
        if "user_id" not in query_params or "model_params" not in query_params:
            self.err.append('unset user_id or model_params dict keys')
            return False
        
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            self.err.append('bad type of user_id')
            return False
        
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            self.err.append('bad type of model_params')
            return False
        
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.
        
            Args:
                model_params (dict): Параметры пользователя для предсказания.
        
            Returns:
                bool: True - если есть нужные параметры, False - иначе
        """
        
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        else:
            self.err.append('incorrect model param set')

        return False
    
    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.
        
            Args:
                params (dict): Словарь параметров запроса.
        
            Returns:
                - **dict**: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        
        return True
        
    def handle(self, params):
        """Функция для обработки запросов API параметров входящего запроса.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            if not self.validate_params(params):
                response = {"Error": "validate_params_errors", "details": self.err}
            else:
                model_params = params["model_params"]
                user_id = params["user_id"]
                predicted_churn = self.churn_predict(model_params)
                response = {
                        "user_id": user_id,
                        "probability": predicted_churn,
                        "is_churn": int(predicted_churn > 0.5)
                    }

        except Exception as e:
            return {"Error": f"Error while handling request: {e}", "details": self.err}
        else:
            return response

if __name__ == "__main__":

    # создаём тестовый запрос
    test_params = {
        "user_id": "123",
        "model_params": {
            "gender": 1,
            "SeniorCitizen": 0,
            "Partner": 0,
            "Dependents": 0,
            "Type": 0.5501916796819537,
            "PaperlessBilling": 1,
            "PaymentMethod": 0.2192247621752094,
            "MonthlyCharges": 50.8,
            "TotalCharges": 288.05,
            "MultipleLines": 0,
            "InternetService": 0.3437455629703251,
            "OnlineSecurity": 0,
            "OnlineBackup": 0,
            "DeviceProtection": 0,
            "TechSupport": 1,
            "StreamingTV": 0,
            "StreamingMovies": 0,
            "days": 245,
            "services": 2
        }
    }

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")        