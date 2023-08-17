
from functions.get_hh_api import get_hh_employers_list, get_employers_info, get_employer_vacancies
from functions.save_data_to_database import save_data_to_database
from functions.create_database import create_database
from functions.config import config
from classes.db_manager import DBManager


def main():

    params = config()
    create_database('test', params)
    list_id_employers = get_hh_employers_list()

    for item in list_id_employers[:10]:
        data_employers = get_employers_info(item)
        data_vacancies = get_employer_vacancies(item)
        save_data_to_database(data_employers, data_vacancies, 'test', params)

    dbm = DBManager('test', params)
    dbm.get_companies_and_vacancies_count()
    dbm.get_all_vacancies()
    dbm.get_avg_salary()
    dbm.get_vacancies_with_higher_salary()
    dbm.get_vacancies_with_keyword("Менеджер по организации и запуску маркетинговых акций")

if __name__ == '__main__':
    main()
