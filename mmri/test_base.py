import json
import logging
import requests
import sys

from datetime import datetime


class TestBase(object):
    def __init__(self, args, logger=None):
        super(TestBase, self).__init__()
        self.DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
        self.options = args
        self.stop_on_error = args.stop_on_error
        self.test_counter = 0
        self.success_counter = 0
        self.error_counter = 0
        self.response_error_counter = 0
        self.trip_not_possible_counter = 0
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('test-otp')


    def run_tests(self):
        infile = open(self.options.input,  'r') if self.options.input != '-' else sys.stdin
        expected_result_file = open(self.options.expected_result,  'r') if self.options.expected_result != '-' else None
        outfile = open(self.options.output, 'w', 1) if self.options.output != '-' else sys.stdout

        tests = json.load(infile)
        if expected_result_file:
            expected_results = json.load(expected_result_file)

        for i, test in enumerate(tests):
            if i > 0:
                self.logger.info('\n')
                self.logger.info('--------------------------------------------------------')
                self.logger.info('\n')

            self.test_counter += 1
            # outfile.write(',\n' if i > 0 else '[\n')
            if type(test['to']) is dict:
                self.logger.info("Test %s: from %s (%f, %f) to %s (%f, %f)", test['id'],
                            test['from']['description'], test['from']['latitude'], test['from']['longitude'],
                            test['to']['description'], test['to']['latitude'], test['to']['longitude'])
            else:
                self.logger.info("Test %s: from stop id: %s to stop id: %s", test['id'], test['from'], test['to'])

            url = self.build_url(test)
            self.logger.debug("    Calling URL: %s", url)
            response = requests.get(url)
            if response:
                result = self.parse_result(test, response.json())
                if result.get('error', '').startswith('Trip is not possible'):
                    self.logger.error('    Test failed: Trip not possible')
                    self.error_counter += 1
                    self.trip_not_possible_counter += 1

                    json.dump(result, outfile, indent=2, sort_keys=True)
                    if self.stop_on_error:
                        return;

                elif expected_result_file:
                    expected_result = self.find_expected_result_for_test(result, expected_results)
                    if expected_result:
                        test_result = self.compare_result(result, expected_result)
                        if test_result:
                            self.logger.success('    Test success')
                            self.success_counter += 1
                        else:
                            self.logger.error('    Test failed')
                            self.error_counter += 1
    
                            json.dump(result, outfile, indent=2, sort_keys=True)
                            if self.stop_on_error:
                                return;
                    else:
                        self.logger.error('    Expeced result for test: %s not found' % result.get('id'))
                        self.error_counter += 1

                        json.dump(result, outfile, indent=2, sort_keys=True)
                        if self.stop_on_error:
                            return;

                # json.dump(result, outfile, indent=2, sort_keys=True)
            else:
                self.logger.error('    Response for test %s failed' % str(test['id']))
                self.error_counter += 1
                self.response_error_counter += 1
                if self.stop_on_error:
                    return;

        # outfile.write('\n]\n')

        if infile  is not sys.stdin:  infile.close()
        if outfile is not sys.stdout: outfile.close()
        
        self.logger.info('\n\nCompleted %d tests' % (self.test_counter,))
        self.logger.success('    Success: %d' % (self.success_counter,))
        self.logger.error('    Error: %d' % (self.error_counter,))
        self.logger.error('    Trip not possible Error: %d' % (self.trip_not_possible_counter,))
        self.logger.error('    Response Error: %d' % (self.response_error_counter,))

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
            if result_legs and len(result_legs) > idx:
                for key in leg:
                    expected_value = leg.get(key)
                    if result_legs[idx].get(key) != expected_value:
                        success = False
                        self.logger.error("    Values for key: %s are not equal: %s : %s" % (key, expected_value, result_legs[idx].get(key)))
            else:
                success = False
                self.logger.error("    Leg not found in result: %s" % (json.dumps(leg),))
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
                    print "Values for key: %s are not equal: %s : %s" % (key, expected_value, result_value)
        return success
