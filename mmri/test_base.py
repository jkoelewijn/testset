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
        self.test_counter = 0
        self.success_counter = 0
        self.error_counter = 0

    def run_tests(self):
        infile = open(self.options.input,  'r') if self.options.input != '-' else sys.stdin
        expected_result_file = open(self.options.expected_result,  'r') if self.options.expected_result != '-' else None
        outfile = open(self.options.output, 'w', 1) if self.options.output != '-' else sys.stdout

        tests = json.load(infile)
        if expected_result_file:
            expected_results = json.load(expected_result_file)

        for i, test in enumerate(tests):
            self.test_counter += 1
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

            if expected_result_file:
                expected_result = self.find_expected_result_for_test(result, expected_results)
                if expected_result:
                    test_result = self.compare_result(result, expected_result)
                    if test_result:
                        logger.info('Test success')
                        self.success_counter += 1
                    else:
                        logger.info('Test failed')
                        self.error_counter += 1
                else:
                    logger.info('Expeced result for test: %s not found' % result.get('id'))
                    self.error_counter += 1

            json.dump(result, outfile, indent=2, sort_keys=True)
        outfile.write('\n]\n')

        if infile  is not sys.stdin:  infile.close()
        if outfile is not sys.stdout: outfile.close()
        
        logger.info('Completed %d tests \n    Success: %d\n    Error: %d' % (self.test_counter, self.success_counter, self.error_counter))

    def jsonDateTime(self, timestamp):
        time = datetime.fromtimestamp(timestamp / 1000)  # milliseconds to seconds
        return datetime.strftime(time, self.DATE_TIME_FORMAT)

    def build_url(self, test):
        # Implement in extended class
        pass

    def parse_result(self, test):
        # Implement in extended class
        pass

    def find_expected_result_for_test(self, test_result, expected_results):
        for result in expected_results:
            if result.get('id') == test_result.get('id'):
                return result
        return None

    def compare_legs(self, expected_legs, result_legs):
        success = True
        for idx, leg in enumerate(expected_legs):
            if len(result_legs) > idx:
                for key in leg:
                    expected_value = leg.get(key)
                    if result_legs[idx].get(key) != expected_value:
                        success = False
                        logger.info("    Values for key: %s are not equeal: %s : %s" % (key, expected_value, result_legs[idx].get(key)))
            else:
                success = False
                logger.info("    Leg not found in result: %s" % (json.dumps(leg),))
        return success

    def compare_result(self, test_result, expected_result):
        success = True

        for key in expected_result:
            expected_value = expected_result.get(key)
            result_value = test_result.get(key)
            if key == 'legs':
                if self.compare_legs(expected_value, result_value) is False:
                    success = False
            else:
                if expected_value != result_value:
                    success = False
                    print "Values for key: %s are not equeal: %s : %s" % (key, expected_value, result_value)
        return success
