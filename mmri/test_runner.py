#!/usr/bin/env python
#
# Test OpenTripPlanner

import argparse
import logging

logger = logging.getLogger('test-otp')


# Command line handling
def parse_args(args=None):
    parser = argparse.ArgumentParser(
            description='Test OpenTripPlanner using planning data from a test file.')
    parser.add_argument('-p', '--provider', metavar='PROVIDER', default='otp', choices=['otp'],
            help='the provider to run the tests for (default: otp)')
    parser.add_argument('input', metavar='INPUT', nargs='?', default='-',
            help='the test input file (default: stdin)')
    parser.add_argument('output', metavar='OUTPUT', nargs='?', default='-',
            help='the test output file (default: stdout')
    parser.add_argument('-u', '--url', metavar='URL',
            help='the OpenTripPlanner URL')
    parser.add_argument('-d', '--debug', action='store_true',
            help='show debugging output')
    return parser.parse_args(args)


def main():
    args = parse_args()

    logging.basicConfig(format='%(message)s', level=logging.WARN)
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    provider = __import__("test_%s" % args.provider)
    test_class = provider.TestClass(args)
    test_class.run_tests()


if __name__ == '__main__':
    main()
