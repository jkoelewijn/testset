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
        self.tests_success = []
        self.tests_error = []
        self.tests_response_error = []
        self.tests_trip_not_possible = []
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('test-otp')


    def run_tests(self, run_test_id=None):
        infile = open(self.options.input,  'r') if self.options.input != '-' else sys.stdin
        expected_result_file = open(self.options.expected_result,  'r') if self.options.expected_result != '-' else None
        outfile = open(self.options.output, 'w', 1) if self.options.output != '-' else sys.stdout

        tests = json.load(infile)
        if expected_result_file:
            expected_results = json.load(expected_result_file)

        for i, test in enumerate(tests):
            if run_test_id and test['id'] != run_test_id:
                continue

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
                self.logger.info("Test %s: from stop id: %s to stop id: %s", test['id'], test.get('from', 'n/a'), test.get('to', 'n/a'))

            url = self.build_url(test)
            self.logger.debug("    Calling URL: %s", url)
            response = requests.get(url)
            if response:
                result = self.parse_result(test, response.json())
                if result.get('error', '').startswith('Trip is not possible'):
                    self.logger.error('    Test failed: Trip not possible')
                    self.tests_error.append(test['id'])
                    self.tests_trip_not_possible.append(test['id'])

                    json.dump(result, outfile, indent=2, sort_keys=True)
                    if self.stop_on_error:
                        return;

                elif expected_result_file:
                    expected_result = self.find_expected_result_for_test(result, expected_results)
                    if expected_result:
                        test_result = self.compare_result(result, expected_result)
                        if test_result:
                            self.logger.success('    Test success')
                            self.tests_success.append(test['id'])
                        else:
                            self.logger.error('    Test failed')
                            self.tests_error.append(test['id'])
    
                            json.dump(result, outfile, indent=2, sort_keys=True)
                            if self.stop_on_error:
                                return;
                    else:
                        self.logger.error('    Expeced result for test: %s not found' % result.get('id'))
                        self.tests_error.append(test['id'])

                        json.dump(result, outfile, indent=2, sort_keys=True)
                        if self.stop_on_error:
                            return;

                # json.dump(result, outfile, indent=2, sort_keys=True)
            else:
                self.logger.error('    Response for test %s failed' % str(test['id']))
                self.tests_error.append(test['id'])
                self.tests_response_error.append(test['id'])
                if self.stop_on_error:
                    return;

        # outfile.write('\n]\n')

        if infile  is not sys.stdin:  infile.close()
        if outfile is not sys.stdout: outfile.close()
        
        self.logger.info('\n\nCompleted %d tests' % (self.test_counter,))
        self.logger.success('    %2d tests succeeding  %s' % (len(self.tests_success), ' '.join(self.tests_success)))
        self.logger.error(  '    %2d tests in error    %s' % (len(self.tests_error),   ' '.join(self.tests_error)))
        self.logger.error(  '    of which:')
        self.logger.error(  '    %2d trip not possible %s' % (len(self.tests_trip_not_possible), ' '.join(self.tests_trip_not_possible)))
        self.logger.error(  '    %2d response errors   %s' % (len(self.tests_response_error),    ' '.join(self.tests_response_error)))

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
                        self.logger.error("    Values for key: %s are not equal.\n    expected: %s \n         got: %s" % (key, expected_value, result_legs[idx].get(key)))
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
                    print "Values for key: %s are not equal expected: %s got: %s" % (key, expected_value, result_value)
        return success
