import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from Utils.utils import Utils
# from database.database import Database
from models.datastorage import DataStorage
from models.company import Company
from models.job import Job

## Note: I should split each class to separate files but current file is not that large.
## TODO: add comments

def getSoupContent(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

def getJson(url):
    r = requests.get(url)
    return json.loads(r.text)


class Processor(object):
    instance = None

    @staticmethod
    def getInstance():
        if Processor.instance is None:
            Processor.instance = Processor()
        return Processor.instance

    def __init__(self):
        super(Processor, self).__init__()

        self.beginning_year = 16
        self.current_year = 21
        self.data = ''
        self.data_storage = DataStorage()


    def start(self, file=False):
        print("Start to process data.")
        if file:
            if self.load_data_from_json('alldata.json') != True:
                print("Cannot read json")
                return False
            print("Updating companies...")
            self.update_company_data(api=False)
            print("Updating jobs...")
            self.update_jobs()
        else:
            self.update_data()

        return True


    def load_data_from_json(self, filename):
        try:
            with open(filename, 'r') as json_file:
                self.data = json.load(json_file)
                return True
        except Exception as e:
            print(e)
            return None

    def save_list_companies(self):
        list_companies = sorted([company.name for company in self.data_storage.companies])
        Utils.save_to_CSV('all_companies.csv', list_companies)
        print("Saved list of companies")



    def get_data_from_api(self, year):
        print("Getting data from API...")
        # year = '21'
        url = f'https://www.siliconmilkroundabout.com/api/companies-attending?event_id={year}'
        try:
            companies_json = getJson(url)

            # Save retrieved data to file
            Utils.save_to_json(f'hiringcompanies20{year}.json', companies_json) 
        except Exception as e:
            print(e)

        return companies_json
    
    def update_jobs(self):
        for c_data in self.data:
            # If company has jobs
            if c_data['jobtitles']:
                jobs = c_data['jobtitles'].split('|JOB|')
                for job in [json.loads(j) for j in jobs]:
                    job = Job(job['title'], job['role_type_id'], c_data['companyid'])
                    self.data_storage.jobs.append(job)
                    self.data_storage.add_job_to_company(job)

            # If company has job tags
            if c_data['jobtags']:
                job_tags = c_data['jobtags'].split('|TAG|')
                for job_tag in [json.loads(j) for j in job_tags]:
                    job_tag = (job_tag['name'], job_tag['id'])
                    self.data_storage.add_job_tag(job_tag)
                    self.data_storage.add_jobtag_to_company(job_tag, c_data['companyid'])

    def update_company_data(self, api=True):
        ## Create Companies
        for c_data in self.data:
            if self.data_storage.check_company_exists(c_data['companyid']) == False:
                company = Company(c_data['name'], c_data['slug'], c_data['companyid'], c_data['description'])
                self.data_storage.add_company(company)
                if api:
                    company.update_company_info_date_size()
            
    def update_data(self):
        for year in range(self.beginning_year,self.current_year+1):
            print(year)
            self.data = self.get_data_from_api(year)
            self.update_company_data()

            if year == self.current_year+1:
                self.update_jobs()

    def save_data(self):
        self.data_storage.save_data_json()



def main():
    print("Starting")

    processor = Processor.getInstance()

    # If file=True: read from 'alldata.json'; if False then retrieves data from API
    processor.start(file=True) 
    processor.save_list_companies()


    # TODO use api to get more job data
    # specific_job_url = f'https://www.siliconmilkroundabout.com/api/get/jobs?id={company_id}'

    print("End of Main.")





if __name__ == "__main__":
    main()