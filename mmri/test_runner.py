#!/usr/bin/env python
#
# Test OpenTripPlanner

import argparse
import logging
from color_logging import ColoredFormatter

logger = logging.getLogger(__name__)


# Command line handling
def parse_args(args=None):
    parser = argparse.ArgumentParser(
            description='Test OpenTripPlanner using planning data from a test file.')
    parser.add_argument('-p', '--provider', metavar='PROVIDER', default='otp', choices=['otp'],
            help='the provider to run the tests for (default: otp)')
    parser.add_argument('input', metavar='INPUT', nargs='?', default='-',
            help='the test input file (default: stdin)')
    parser.add_argument('expected_result', metavar='EXPECTED_RESULT', nargs='?', default='-',
            help='the test expected output file (default: stdin)')
    parser.add_argument('output', metavar='OUTPUT', nargs='?', default='-',
            help='the test output file (default: stdout')
    parser.add_argument('-u', '--url', metavar='URL',
            help='the OpenTripPlanner URL')
    parser.add_argument('-d', '--debug', action='store_true',
            help='show debugging output')
    parser.add_argument('-s', '--stop_on_error', action='store_true',
            help='stop when test errors')

    return parser.parse_args(args)


def main():
    args = parse_args()


    SUCCESS_LEVEL_NUM = 9 
    logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")
    def success(self, message, *args, **kws):
        # Yes, logger takes its '*args' as 'args'.
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws) 
    logging.Logger.success = success


    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(ColoredFormatter('%(message)s'))
    # console.setFormatter(ColoredFormatter('%(name)s: %(message)s (%(filename)s:%(lineno)d)'))
    logger.addHandler(console)

    provider = __import__("test_%s" % args.provider)
    test_class = provider.TestClass(args, logger=logger)
    test_class.run_tests()


if __name__ == '__main__':
    main()
