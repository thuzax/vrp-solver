class RequestsStorage:
    instance = None
    def __new__(cls, *args, **kwargs):
        if (cls.instance is None):
            cls.instance = super(RequestsStorage, cls).__new__(
                cls, *args, **kwargs
            )
            cls.instance.initialize_attrs()
        
        return cls.instance

    def initialize_attrs(self):
        self.all_requests = {}
        self.new_requests = {}

    def store_new_request(self, pair, request):
        self.new_requests[pair] = request
        self.all_requests[pair] = request


    def get_all_requests(self):
        return self.all_requests

    
    def get_new_requests(self):
        return self.new_requests


    def reset_new_requests(self):
        self.new_requests = {}