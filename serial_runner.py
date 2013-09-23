import argparse
import sys
from runner import Runner
import lib.mixpanel_data_puller as puller

class SerialRunner(Runner):

    def create_parser(self):
        parser = argparse.ArgumentParser(description='Serial Runner for mixpanel data pull.')
        return parser

    def pull_data(self, date):
        if self.args.dry:
            return "DRY_MODE"
        return puller.pull(date, date, self.args.apikey, self.args.apisecret)

    def pull_data_for_date_range(self):
        start_date, end_date = self.args.startdate, self.args.enddate
        for date in self.date_iter(start_date, end_date):
            date = puller.stringify_date(date)
            print "Pulling data for %s" % date
            data_iter = self.pull_data(date)
            s3_output_file = "%s%s" % (self.output_bucket, date)
            self.put_s3_string_iter(data_iter, s3_output_file, zip=True)

def run(argv):
    runner = SerialRunner()
    runner.parse_args(argv)
    runner.pull_data_for_date_range()

if __name__ == '__main__':
    run(sys.argv)
