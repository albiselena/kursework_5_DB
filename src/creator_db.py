import psycopg2
from config import config

from connection_hh import ParserHH

params = config()


def create_database(params: dict) -> None:
    """Создание базы данных. Eсли база данных с таким именем уже существует, она удаляется."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""DROP DATABASE IF EXISTS hh_database""")
    cur.execute("""CREATE DATABASE hh_database""")
    print("""База данных hh_database создана.""")

    cur.close()
    conn.close()


def create_tables(params: dict) -> None:
    """Создание таблиц для сохранения данных о работодателях и вакансиях."""
    conn = psycopg2.connect(dbname='hh_database', **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                company_id SERIAL PRIMARY KEY,
                name_company VARCHAR(250) NOT NULL,
                url TEXT NOT NULL,
                vacancies INTEGER
            )"""
                    )
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INTEGER NOT NULL,
                title VARCHAR(250) NOT NULL,
                area VARCHAR(50),
                salary_from INTEGER,
                salary_to INTEGER,
                url TEXT,
                experience VARCHAR(50),
                FOREIGN KEY (company_id) REFERENCES employers (company_id)
            )"""
                    )
        print('Таблицы с работодателями и вакансиями созданы.')

    conn.commit()
    conn.close()


def loading_data_into_tables(params: dict, employer_id) -> None:
    """Загрузка данных в таблицы."""
    hh = ParserHH(employer_id)
    employers = hh.job_employers()
    vacancies = hh.job_vacancies()
    conn = psycopg2.connect(dbname='hh_database', **params)
    with conn.cursor() as cur:
        for employer, vacancy in zip(employers, vacancies):
            cur.execute("""
                INSERT INTO employers (name_company, url, vacancies)
                VALUES (%s, %s, %s)
                RETURNING company_id
            """, (employer['name'], employer['url'], employer['vacancies']))
            company_id = cur.fetchone()[0]  # Получаем новый company_id из новой созданной таблицы с работодателями
            for v in vacancy['vacancies']:
                cur.execute("""
                    INSERT INTO vacancies (company_id, title, area, salary_from, salary_to, url, experience)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (company_id, v['name'], vacancy['area'], v['salary_from'], v['salary_to'], v['url'],
                      v['experience']))
        print('Данные загружены в таблицы.')

    conn.commit()
    conn.close()



#create_database(params)
#create_tables(params)
#loading_data_into_tables(params, (80, 2987))
