#!/usr/bin/env python
#
# Test a trip planner

import sys
import argparse
from importlib import import_module
import logging
from color_logging import ColoredFormatter


PROVIDER_CHOICES = ['otp', 'hpjp']


logger = logging.getLogger(__name__)


def setup_logging(options):
    SUCCESS_LEVEL_NUM = 9
    logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

    def success(self, message, *args, **kws):
        # Yes, logger takes its '*args' as 'args'.
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)
    logging.Logger.success = success

    logger.setLevel(logging.DEBUG if options.debug else logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(ColoredFormatter('%(message)s'))
    # console.setFormatter(ColoredFormatter('%(name)s: %(message)s (%(filename)s:%(lineno)d)'))
    logger.addHandler(console)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
            description='Test a trip planner and time requests.')
    parser.add_argument('-t', '--test', metavar='TEST',
            help='id of the test to run (default: all tests)')
    parser.add_argument('-p', '--provider', metavar='PROVIDER',
            choices=PROVIDER_CHOICES, default='otp',
            help='provider to run the tests for (default: otp)')
    parser.add_argument('input', metavar='INPUT',
            help='file to read test input from')
    parser.add_argument('expected_output', metavar='EXPECTED',
            help='file to read expected output from')
    parser.add_argument('output', metavar='OUTPUT',
            help='file to write actual output to')
    parser.add_argument('benchmark_output', metavar='TIMING_OUTPUT',
            help='file to write timing data to')
    parser.add_argument('-u', '--url', metavar='URL',
            help='planner URL (optional based on planner)')
    parser.add_argument('-d', '--debug', action='store_true',
            help='show debugging output')
    parser.add_argument('-s', '--stop_on_error', action='store_true',
            help='stop on first test error')

    return parser.parse_args(args)


def main():
    options = parse_args()
    setup_logging(options)

    try:
        provider = __import__("test_%s" % options.provider)
    except ImportError:
        provider = import_module("mmri.test_%s" % options.provider)

    test_class = provider.TestClass(options, logger=logger)
    test_class.run_tests(run_test_id=options.test)


if __name__ == '__main__':
    main()
