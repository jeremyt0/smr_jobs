

class Job:
    
    def __init__(self, title, role_type, company_id):
        self.title = title
        self.role_type = role_type
        self.company_id = company_id

    def get_Job_dict(self):
        return {'title': self.title, 'role_type': self.role_type, 'company_id': self.company_id}

    def __str__(self):
        return 'Job: {self.title}'.format(self=self)