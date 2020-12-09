from models.job import Job
import requests
from bs4 import BeautifulSoup


def getSoupContent(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

class Company:

    def __init__(self, name, slug, id, description):
        self.name = name
        self.slug = slug
        self.id = id
        self.description = description
        self.jobs = []
        self.job_tags = []
        self.size = None
        self.date_established = None

    def get_Company_dict(self):
        return {'name': self.name, 'slug': self.slug, 'companyid': self.id, 'description': self.description, 'jobcount': self.get_num_jobs(), 'jobtitles': [job.get_Job_dict() for job in self.jobs], 'jobtags': self.job_tags, 'size': self.size, 'date_established': self.date_established}

    def get_num_jobs(self):
        return len(self.jobs)

    # Updates company 'date_established' and 'team_members'
    def update_company_info_date_size(self):
        print(f"Getting date and size of {self.slug}")
        url = f'https://www.siliconmilkroundabout.com/company/{self.slug}'
        soup = getSoupContent(url)

        keys = [key.text.replace(' ','_') for key in soup.find_all('dt')]
        values = [value.text for value in soup.find_all('dd')]

        dict1 = dict(zip(keys, values))
        if 'date_established' in dict1:
            self.date_established = dict1['date_established']
        if 'team_members' in dict1:
            self.size = dict1['team_members']

        return len(dict1) == 2

    def __str__(self):
        return 'Company: {self.name}'.format(self=self)