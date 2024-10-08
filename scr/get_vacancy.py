import requests


class HH_api_db:
    """Класс для работы с API HH.ru и заполнение таблиц в BD"""
    employers_dict = {
        "Яндекс": 1740,
        "Авито": 84585,
        "Ozon": 2180,
        "Тинькофф": 78638,
        "VK": 15478,
        "Банк ВТБ": 4181,
        "Билайн": 4934,
        "СБЕР": 3529,
        "МТС": 3776,
        "2ГИС": 64174
    }

    @staticmethod
    def get_request(employer_id) -> dict:
        """Запрос списка работодателей, при наличии вакансий и заработной платы"""
        params = {
            "page": 1,
            "per_page": 100,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']

    def get_vacancies(self):
        """Получение списка работодателей"""
        vacancies_list = []
        for employer in self.employers_dict:
            emp_vacancies = self.get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list