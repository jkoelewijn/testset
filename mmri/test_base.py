import json
import logging
import requests
import sys

from datetime import datetime

logger = logging.getLogger('test-otp')


class TestBase(object):
    def __init__(self, args):
        super(TestBase, self).__init__()
        self.DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
        self.options = args

    def run_tests(self):
        infile  = open(self.options.input,  'r')    if self.options.input  != '-' else sys.stdin
        outfile = open(self.options.output, 'w', 1) if self.options.output != '-' else sys.stdout

        tests = json.load(infile)
        for i, test in enumerate(tests):
            outfile.write(',\n' if i > 0 else '[\n')
            if type(test['to']) is dict:
                logger.info("Test %s: from %s (%f, %f) to %s (%f, %f)", test['id'],
                        test['from']['description'], test['from']['latitude'], test['from']['longitude'],
                        test['to']['description'], test['to']['latitude'], test['to']['longitude'])
            else:
                logger.info("Test %s: from stop id: %s to stop id: %s", test['id'], test['from'], test['to'])

            url = self.build_url(test)
            logger.debug("Calling URL: %s", url)
            response = requests.get(url)
            result = self.parse_result(test, response.json())
            json.dump(result, outfile, indent=2, sort_keys=True)
        outfile.write('\n]\n')

        if infile  is not sys.stdin:  infile.close()
        if outfile is not sys.stdout: outfile.close()

    def jsonDateTime(self, timestamp):
        time = datetime.fromtimestamp(timestamp / 1000)  # milliseconds to seconds
        return datetime.strftime(time, self.DATE_TIME_FORMAT)

    def build_url(self, test):
        # Implement in extended class
        pass

    def parse_result(self, test):
        # Implement in extended class
        pass

    def compare_result(self, test):
        pass
