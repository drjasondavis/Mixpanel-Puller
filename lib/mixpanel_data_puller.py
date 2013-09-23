import sys
from datetime import datetime
import mixpanel_api

DATE_FORMAT = '%Y-%m-%d'

def extract_dates(start_date, end_date):
    def validate(date_str):
        try:
            return parse_date(date_str)
        except:
            print "Invalid date format: %s, valid date format should look like: %s" % (date_str, DATE_FORMAT)
            raise

    return [validate(d) for d in [start_date, end_date]]

def parse_date(d_str):
    return datetime.strptime(d_str, DATE_FORMAT).date()

def stringify_date(d):
    return d.strftime(DATE_FORMAT)

def pull(start_date, end_date, api_key, api_secret):
    api = mixpanel_api.Mixpanel(api_key, api_secret, data=True)
    data_iter = api.request(['export'], {
        'from_date': start_date,
        'to_date': end_date,
    })
    return data_iter

def run(argv):
    start_date = argv[0]

    i = 1
    if len(argv) == 3:
        end_date = start_date
    elif len(argv) == 4:
        end_date = sys.argv[i]
        i += 1
    else:
        raise Exception("Invalid input")

    api_key, api_secret = argv[i:i+2]

    for d in pull(start_date, end_date, api_key, api_secret):
        print d,

if __name__ == "__main__":
    run(sys.argv[1:])
