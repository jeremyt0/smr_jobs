from models.company import Company

class DataStorage:

    def __init__(self):
        self.companies = []
        self.jobs = []
        self.job_tags = []  # List of tuples (job_tag, id)

    def add_job_tag(self, j):
        if j not in self.job_tags:
            self.job_tags.append(j)
            return True
        return False

    def add_job_to_company(self, job):
        self.get_company(job['company_id']).jobs.append(job)


    def add_jobtag_to_company(self, job_tag, company_id):
        self.get_company(company_id).job_tags.append(job_tag)


    def add_company(self, company):
        if company.id not in [company.id for company in self.companies]:
            self.companies.append(company)
            return True
        return False

    def get_company(self, companyid):
        for co in self.companies:
            if companyid == co.id:
                return co
        return None

    def check_company_exists(self, companyid):
        return companyid in [co.id for co in self.companies]


    def save_available_jobs_CSV(self):
        # Create CSV output
        try:
            string = ''
            for company in self.companies:
                for job in company.jobs:
                    string += f'{company.name},{job.title}\n'
                    # print(f'{company.name}, {job.title}')
        except Exception as e:
            print(e)
            return False
        return Utils.save_to_txt(f'open_positions.csv', string)

    # TODO: Save data into a json template
    def save_data_json(self):
        #Save all relevant information to a json file

        data = [company.get_Company_dict() for company in self.companies]
        return Utils.save_to_json(f'alldata.json', data)