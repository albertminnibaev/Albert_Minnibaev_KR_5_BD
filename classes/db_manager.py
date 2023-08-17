import psycopg2


class DBManager:
    """
    Класс для работы с базой данных работодателей и их вакансий вакансий
    """

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании
        :return: список всех компаний и количество вакансий у каждой компании
        """
        data = {}
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT name, open_vacancies FROM employers")
                    rows = cur.fetchall()
                    for row in rows:
                        data[row[0]] = row[1]
        finally:
            conn.commit()
            conn.close()
        return data

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return: список словарей всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию.
        """
        data = []
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT employers.name, vacancies.name, salary_from, salary_to, 
                               salary_currency, vacancy_url FROM vacancies
                               INNER JOIN employers USING(employee_id)""")
                    rows = cur.fetchall()
                    for row in rows:
                        data.append({'employee_name': row[0],
                                     'vacancy_name': row[1],
                                     'salary_from': f'{row[2]} {row[4]}',
                                     'salary_to': f'{row[3]} {row[4]}',
                                     'vacancy_url': row[5]})
        finally:
            conn.commit()
            conn.close()
        return data

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        :return: среднюю зарплату по вакансиям
        """
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT AVG(salary_from) FROM vacancies")
                    avg_salary = round(cur.fetchall()[0][0])
        finally:
            conn.commit()
            conn.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT * FROM vacancies WHERE salary_from > {self.get_avg_salary()}")
                    vacancies_with_higher_salary = cur.fetchall()
        finally:
            conn.commit()
            conn.close()
        return vacancies_with_higher_salary

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        :param name: ключевое слово
        :return: список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT * FROM vacancies WHERE name LIKE '%{keyword}%'")
                    vacancies_with_keyword = cur.fetchall()
        finally:
            conn.commit()
            conn.close()
        return vacancies_with_keyword
