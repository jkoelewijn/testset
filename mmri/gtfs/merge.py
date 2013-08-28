#!/usr/bin/env python

"""
Merge multiple GTFS feeds.
"""

import argparse
from collections import namedtuple
import os
import sys

from mmri.util.csv_unicode import UnicodeDictReader, UnicodeDictWriter


Agency = namedtuple('Agency',
        'agency_id,agency_name,agency_url,agency_timezone,agency_lang')
CalendarDate = namedtuple('CalendarDate',
        'date,service_id,exception_type')
Route = namedtuple('Route',
        'agency_id,route_id,route_short_name,route_long_name,route_type')
Stop = namedtuple('Stop',
        'stop_id,stop_name,stop_lat,stop_lon,location_type,parent_station')
StopTime = namedtuple('StopTime',
        'trip_id,arrival_time,departure_time,stop_id,stop_sequence')
Transfer = namedtuple('Transfer',
        'from_stop_id,to_stop_id,transfer_type,min_transfer_time')
Trip = namedtuple('Trip',
        'route_id,service_id,trip_id,block_id,wheelchair_accessible')

gtfs_files = [
    ('agency.txt', Agency),
    ('calendar_dates.txt', CalendarDate),
    ('routes.txt', Route),
    ('stops.txt', Stop),
    ('stop_times.txt', StopTime),
    ('transfers.txt', Transfer),
    ('trips.txt', Trip),
]


def merge_gtfs(input_dirs, output_dir):
    """
    Merge GTFS feeds from `input_dirs` to `output_dir`. Duplicate
    rows will be discarded, but no attempt is made to match unique
    fields. For example, multiple row with the same `agency_id` can
    appear in the output.
    """

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for filename, cls in gtfs_files:
        merged = set()
        for input_dir in input_dirs:
            input_filename = os.path.join(input_dir, filename)
            if not os.path.exists(input_filename): continue
            with open(input_filename, 'rb') as csv_file:
                for row in UnicodeDictReader(csv_file, delimiter=','):
                    for f in cls._fields: row.setdefault(f, '')
                    merged.add(cls(**row))
        merged = sorted(merged)
        with open(os.path.join(output_dir, filename), 'wb') as csv_file:
            writer = UnicodeDictWriter(csv_file, cls._fields, delimiter=',')
            writer.writeheader()
            writer.writerows(row._asdict() for row in merged)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
            description='Merge GTFS feeds.')
    parser.add_argument('input_dirs', metavar='INPUT_FEED', nargs='+',
            help='input GTFS feed directory')
    parser.add_argument('output_dir', metavar='OUTPUT_FEED',
            help='output GTFS feed directory (will be overwritten)')
    return parser.parse_args(args)


def main():
    options = parse_args()
    merge_gtfs(options.input_dirs, options.output_dir)


if __name__ == '__main__':
    main()
