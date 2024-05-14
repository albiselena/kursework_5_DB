import os
from pprint import pprint

import requests
import json


class ParserHH():
    """Парсер данных с сайта hh.ru."""
    base_url = 'https://api.hh.ru/'

    def __init__(self, id_employers):
        self.id_employers = id_employers

    def get_employer_info(self, employer_id: int) -> dict:
        """Функция строит УРЛ, отправляет запрос, проверяет статус, разбирает ответ в виде json."""
        url = f'{self.base_url}employers/{employer_id}/'
        response = requests.get(url)
        response.raise_for_status()
        emp_info = response.json()
        return {
            'id': emp_info['id'],
            'name': emp_info['name'],
            'url': emp_info['alternate_url'],
            'vacancies': emp_info['open_vacancies']
        }

    def job_employers(self) -> list[dict]:
        """Получение информации о работодателях по их id."""
        return [
            self.get_employer_info(emp_id)
            for emp_id in self.id_employers
        ]

    def get_vacancy_info(self, employer_id: int) -> dict:
        url = f'{self.base_url}vacancies?employer_id={employer_id}'
        params = {'per_page': 10, 'employer_id': employer_id, 'area': 1}  # В данном запросе возвращается 10 вакансий
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancy = response.json()
        return {
            'employer_id': employer_id,
            'area': 'Москва',  # Вакансии только по Москве чтобы не делать много запросов
            'vacancies': [
                {
                    'name': v['name'],
                    'url': v['alternate_url'],
                    'salary_from': v['salary'].get('from', None) if v['salary'] else None,
                    'salary_to': v['salary'].get('to', None) if v['salary'] else None,
                    'experience': v['experience']['name'],
                    'employment': v['employment']['name'],
                }
                for v in vacancy['items']
            ]
        }

    def job_vacancies(self) -> list[dict]:
        """Получение информации о вакансиях по id работодателя."""
        return [
            self.get_vacancy_info(emp_id)
            for emp_id in self.id_employers
        ]

#emp_id = (4219, 80, 132654, 2987, 7172, 2596486, 1375441, 4207409, 105688, 1100167)
#api = ParserHH(emp_id)
#data = api.job_employers()
#vacancies = api.job_vacancies()
#pprint(vacancies)

# 80 - Альфа-Банк
# 4219 - Теле2
# 132654 - Нефте Транс Сервис
# 2987 - КРОК
# 7172 - Лента
# 2596486 - Основа
# 1375441 - Okko
# 4207409 - Комитет
# 105688 - Белая дача
# 1100167 - Казанский университет
