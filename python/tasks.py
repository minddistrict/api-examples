class Task(object):

    def __init__(self, task_result):
        # task_result contains what the API returns
        self.api_url = task_result['@url']
        self.modification_time = task_result['@changes']['modification_time']
        self.creation_time = task_result['@changes']['creation_time']
        self.title = task_result['title']
        self.url = task_result['url']
        self.title = task_result['title']
        self.message = task_result['message']
