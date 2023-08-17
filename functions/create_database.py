import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных PostgreSQL и таблиц employers и vacancies в базе данных
    :param database_name: название БД
    :param params: словарь с параметрами для подключения к БД
    :return: None
    """
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
    finally:
        conn.close()

    try:
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS employers")
                cur.execute("""CREATE TABLE IF NOT EXISTS employers (
                            employee_id int,
                            name VARCHAR(50),
                            type VARCHAR(50),
                            city VARCHAR(30),
                            site_url  VARCHAR(200),
                            alternate_url VARCHAR(100),
                            vacancies_url VARCHAR(100),
                            open_vacancies int,
                            description VARCHAR(10000),
                            CONSTRAINT pk_employers_id PRIMARY KEY (employee_id))""")

                cur.execute("DROP TABLE IF EXISTS vacancies")
                cur.execute("""CREATE TABLE IF NOT EXISTS vacancies (
                            vacancy_id int,
                            employee_id int,
                            name VARCHAR(200),
                            salary_from int,
                            salary_to int,
                            salary_currency VARCHAR(30),
                            city VARCHAR(100),
                            requirement VARCHAR(500),
                            responsibility VARCHAR(500),
                            experience VARCHAR(500),
                            employment VARCHAR(100),
                            vacancy_url VARCHAR(100),
                            CONSTRAINT pk_vacancies_id PRIMARY KEY (vacancy_id),
                            CONSTRAINT fk_vacancies_id_employers FOREIGN KEY (employee_id) REFERENCES 
                            employers(employee_id) ON DELETE CASCADE) """)
    finally:
        conn.commit()
        conn.close()
