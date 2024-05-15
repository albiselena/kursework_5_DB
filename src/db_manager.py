from pprint import pprint, pformat

import psycopg2
from config import config

params = config()


class DBManager:
    """Класс для работы с базой данных."""
    def __init__(self, params):
        self.params = params
        self.conn = psycopg2.connect(dbname='hh_database', **params)
        self.cur = self.conn.cursor()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.cur.close()
        self.conn.close()

    @property
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute("""
            SELECT employers.name_company, COUNT(vacancies.company_id) AS count_vacancies
            FROM employers
            LEFT JOIN vacancies ON employers.company_id = vacancies.company_id
            GROUP BY employers.name_company;
        """)
        rows = self.cur.fetchall()
        result = [{"name_company": row[0], "count_vacancies": row[1]} for row in rows]
        return pformat(result)

    @property
    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию."""
        self.cur.execute("""
            SELECT employers.name_company, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN employers ON employers.company_id = vacancies.company_id;
        """)
        rows = self.cur.fetchall()
        result = [{"name_company": row[0], "title": row[1], "salary_from": row[2], "salary_to": row[3], "url": row[4]}
                  for row in rows]
        return pformat(result)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.cur.execute("""
            SELECT AVG(salary_from) FROM vacancies;
            """)
        avg_salary = self.cur.fetchone()[0]
        return round(avg_salary)

    def get_vacancies_with_higher_salary(self):
        """Получает список вакансий с зарплатой выше средней."""
        self.cur.execute("""
            SELECT vacancies.title FROM vacancies
            WHERE vacancies.salary_from > (SELECT AVG(salary_from) FROM vacancies);
        """)
        result = self.cur.fetchall()
        return pformat(result)

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список вакансий с ключевым словом в названии."""
        self.cur.execute(f"""
            SELECT * FROM vacancies
            WHERE LOWER(vacancies.title) ILIKE '%{keyword}%';
        """)
        rows = self.cur.fetchall()
        result = [{"title": row[2], "salary_from": row[3], "salary_to": row[4], "url": row[5]}
                  for row in rows]
        return pformat(result)



