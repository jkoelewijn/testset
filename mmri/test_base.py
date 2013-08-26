import json
import logging
import requests
import sys

from datetime import datetime
from time import time

# The amount of times the script should run the tests.
# This is important to filter out outliers
RUN_TIMES = 1

MAX_DURATION = 5
WARNING_DURATION = 3

class TestBase(object):
    def __init__(self, args, logger=None):
        super(TestBase, self).__init__()
        self.DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
        self.options = args
        self.stop_on_error = args.stop_on_error
        self.benchmark = args.benchmark
        self.test_counter = 0
        self.tests_success = []
        self.tests_error = []
        self.tests_response_error = []
        self.tests_trip_not_possible = []
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('test-otp')

        if self.benchmark:
            self.benchmarker = { \
                    'total_time': 0, \
                    'number_requests': 0, \
                    'average': 0, \
                    'number_warning': 0, \
                    'number_max': 0, \
                    'maximum_time': 0, \
                    'maximum_id': '', \
                    'minimum_time': 1000000000, \
                    'minimum_id': '', \
                    'warning_duration': WARNING_DURATION, \
                    'max_duration': MAX_DURATION, \
                    'summary': [], \
            }

    def run_tests(self, run_test_id=None):
        infile = open(self.options.input,  'r') if self.options.input != '-' else sys.stdin
        if self.options.expected_result:
            expected_result_file = open(self.options.expected_result,  'r') if self.options.expected_result != '-' else None
        else:
            expected_result_file = None

        outfile = open(self.options.output, 'w', 1) if self.options.output != '-' else sys.stdout
        # Note that this file descriptor is on append mode, so it won't clear the
        # existing data from the file
        benchmark_outfile = open(self.options.benchmark_output, 'a', 1) if self.options.benchmark_output != '-' else sys.stdout

        tests = json.load(infile)
        if expected_result_file:
            expected_results = json.load(expected_result_file)

        for j in range(RUN_TIMES):
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
                if self.benchmark:
                    start_time = time()
                response = requests.get(url)
                if self.benchmark:
                    self.update_benchmarker(start_time, test['id'])
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

                    # If there is not expected result and otp didin't return 
                    # trip not possible, then it's considered as successful
                    else:
                        self.logger.success('    Test success')
                        self.tests_success.append(test['id'])

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
        self.logger.success('\t%2d tests succeeding  %s' % (len(self.tests_success), ' '.join(self.tests_success)))
        if expected_result_file is None:
            self.logger.warning('\tYou didn\'t provide a file of expected results!\n')
        self.logger.error(  '\t%2d tests in error    %s' % (len(self.tests_error),   ' '.join(self.tests_error)))
        self.logger.error(  '\tof which:')
        self.logger.error(  '\t%2d trip not possible %s' % (len(self.tests_trip_not_possible), ' '.join(self.tests_trip_not_possible)))
        self.logger.error(  '\t%2d response errors   %s' % (len(self.tests_response_error),    ' '.join(self.tests_response_error)))
        if self.benchmark:
            self.print_benchmarker(benchmark_outfile)

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
                    if expected_value == '*':
                        self.logger.warning("    Value for key: %s has been neglected as the expected result is declared with a *" % (key))
                    elif result_legs[idx].get(key) != expected_value:
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

    def print_benchmarker(self, benchmark_outfile):
        self.logger.info('\nStatistics: \
                \n\tAverage Response Time - %(average).2fs \
                \n\tSlowest Response:\n\t\tID - %(maximum_id)s\n\t\tDuration - (%(maximum_time).2fs) \
                \n\tFastest Response:\n\t\tID - %(minimum_id)s\n\t\tDuration - (%(minimum_time).2fs)' \
                % self.benchmarker)
        self.logger.warning('\tSlower than %(warning_duration).2fs - %(number_max)d requests' % self.benchmarker)
        self.logger.error('\tSlower than %(max_duration).2fs - %(number_warning)d requests\n' % self.benchmarker)

        if benchmark_outfile is not None:
            summary = "\n # TEST RUN AT %s \n" % str(datetime.now())
            for x in self.benchmarker['summary']:
                summary += "%s %s\n" % (x[0], x[1])
            benchmark_outfile.write(summary)
            benchmark_outfile.close()

    def update_benchmarker(self, start_time, request_id):
        if start_time is not None:
            duration = time() - start_time
            self.benchmarker['number_requests'] += 1
            self.benchmarker['total_time'] += duration
            self.benchmarker['average'] = ( self.benchmarker['number_requests'] * self.benchmarker['average'] + duration ) / ( self.benchmarker['number_requests'] + 1 )
            if duration > self.benchmarker['maximum_time']:
                self.benchmarker['maximum_time'] = duration
                self.benchmarker['maximum_id'] = request_id

            elif duration < self.benchmarker['minimum_time']:
                self.benchmarker['minimum_time'] = duration
                self.benchmarker['minimum_id'] = request_id

            if duration > self.benchmarker['max_duration']:
                self.benchmarker['number_warning'] += 1
                self.logger.error('\tRequest took %.2f seconds' % duration)

            elif duration > self.benchmarker['warning_duration']:
                self.benchmarker['number_max'] += 1
                self.logger.warning('\tRequest took %.2f seconds' % duration)

            else:
                self.logger.success('\t%.2f seconds' % duration)

            self.benchmarker['summary'].append((request_id, duration))
