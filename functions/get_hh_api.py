
import requests


def get_hh_employers_list():
    """
    Формирует список ID 100 работодателей отсортированных по колличеству открытых вакансий
    :return: список ID 100 работодателей отсортированных по колличеству открытых вакансий
    """
    list_id_employers = []
    params = {
        'only_with_vacancies': True,  # Наличие открытых вакансий
        'sort_by': 'by_vacancies_open',  # Сортировка по колличеству вакансий
        'per_page': 100,  # Кол-во вакансий на 1 странице
        'offset': 0,
        'limit': 1000,
    }
    try:
        req = requests.get('https://api.hh.ru/employers', params=params)
    except requests.ConnectionError as e:
        print("Ошибка подключения:", e)
    except requests.Timeout as e:
        print("Ошибка тайм-аута:", e)
    except requests.RequestException as e:
        print("Ошибка запроса:", e)
    else:
        data = req.json()
        list_id_employers = [i["id"] for i in data["items"]]

    return list_id_employers


def get_employers_info(employer_id):
    """
    Формирует словарь с информацией о работодателе по его ID
    :param employer_id: ID работодателя
    :return: словарь с информацией о работодателе
    """
    params = {
        'per_page': 100, # Кол-во на 1 странице
        'offset': 0,
        'limit': 1000,
    }
    try:
        req = requests.get(f'https://api.hh.ru/employers/{employer_id}', params=params)
    except requests.ConnectionError as e:
        print("Ошибка подключения:", e)
    except requests.Timeout as e:
        print("Ошибка тайм-аута:", e)
    except requests.RequestException as e:
        print("Ошибка запроса:", e)
    else:
        data = req.json()

    return data


def get_employer_vacancies(employer_id):
    """
    Формирует словарь с информацией о акансиях работодателя
    :param employer_id: ID работодателя
    :return: словарь с информацией о акансиях работодателя
    """
    data = []
    page = 0
    status = True
    while status:
        params = {
            'employer_id': employer_id,  # поиск по конкретному работодателю
            'order_by': 'salary_desc', # сортировка по убыванию зарплаты
            'vacancy_type': 'open', # только открытые вакансии
            'per_page': 100, # Кол-во вакансий на 1 странице
            'page': page,  # номер страницы
        }
        try:
            req = requests.get('https://api.hh.ru/vacancies', params=params)
        except requests.ConnectionError as e:
            print("Ошибка подключения:", e)
        except requests.Timeout as e:
            print("Ошибка тайм-аута:", e)
        except requests.RequestException as e:
            print("Ошибка запроса:", e)
        else:
            if req.status_code == 200:
                data.append(req.json())
                page += 1
            else:
                status = False

    return data
