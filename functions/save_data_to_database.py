import psycopg2


def save_data_to_database(data_e, data_v, database_name, params) -> None:
    """
    Сохранение данных о аботодателях и их вакансиях в базу данных.
    :param data_e: словарь с данными о работодателях
    :param data_v: словарь с данными о вакансиях по конкретному работодателю
    :param database_name: название ДБ
    :param params: словарь с параметрами для подключения к БД
    :return: None
    """
    try:
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO employers (employee_id, name, type, city, site_url, alternate_url, vacancies_url, 
                    open_vacancies, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING employee_id
                    """,
                    (data_e['id'], data_e['name'], data_e['type'], data_e['area']['name'], data_e['site_url'],
                     data_e['alternate_url'], data_e['vacancies_url'], data_e['open_vacancies'], data_e['description'])
                )
                employee_id = cur.fetchone()[0]

                for items in data_v:
                    for item in items['items']:
                        with conn.cursor() as cur:
                            cur.execute(
                                """
                                INSERT INTO vacancies (vacancy_id, employee_id, name, salary_from, salary_to, 
                                salary_currency, city, requirement, responsibility, experience, employment, vacancy_url)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                (item['id'], employee_id, item['name'], item['salary']['from'], item['salary']['to'],
                                 item['salary']['currency'], item['area']['name'], item['snippet']['requirement'],
                                 item['snippet']['responsibility'], item['experience']['name'],
                                 item['employment']['name'], item['alternate_url'])
                            )
    finally:
        conn.commit()
        conn.close()
