from src.db_manager import DBManager
from src.creator_db import create_database, create_tables, loading_data_into_tables
from src.config import config

params = config()


def main():
    print('Делаем запросы к API hh.ru и загружаем данные в базу данных.')
    employer_id = [2768743, 72404, 1758479, 3208395, 7788, 3089, 589513, 851138, 95255, 1100167]
    create_database(params)
    create_tables(params)
    loading_data_into_tables(params, employer_id)
    db = DBManager(params)
    print('База данных создана и заполнена данными.')
    print('Выберете действие:')
    print('1 - Получить список всех компаний и количество вакансий у каждой компании')
    print('2 - Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию')
    print('3 - Получить среднюю зарплату по вакансиям')
    print('4 - Получить список вакансий с зарплатой выше средней')
    print('5 - Получить список вакансий по ключевому слову')
    print('0 - Выход')
    while True:
        try:
            user_request = int(input())
            if user_request == 1:
                print(db.get_companies_and_vacancies_count)
            elif user_request == 2:
                print(db.get_all_vacancies)
            elif user_request == 3:
                print(db.get_avg_salary())
            elif user_request == 4:
                print(db.get_vacancies_with_higher_salary())
            elif user_request == 5:
                print('Введите ключевое слово:')
                keyword = input()
                print(db.get_vacancies_with_keyword(keyword))
            elif user_request == 0:
                break
            else:
                print("Неверный ввод. Пожалуйста, введите число от 0 до 5.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число от 0 до 5.")
    db.close()


if __name__ == '__main__':
    main()

