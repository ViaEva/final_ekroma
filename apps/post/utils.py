from datetime import datetime

def get_time():
    format = '%Y%m%d%M%s'
    return datetime.now().strftime(format)