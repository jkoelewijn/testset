# # Test OpenTripPlanner
import requests
import urllib

from datetime import datetime
from test_base import TestBase


class TestClass(TestBase):

    def __init__(self, *args, **kwargs):
        super(TestClass, self).__init__(*args, **kwargs)

        if not self.options.url:
            self.options.url = 'http://localhost:8080/otp-rest-servlet/ws/plan'

    def plan_trip(self, test):
        url = self.build_url(test)
        self.logger.debug("calling url: %s" % url)
        response = requests.get(url)
        if response:
            return self.parse_result(test, response.json())
        else:
            return None

    def build_url(self, test):
        time = datetime.strptime(test['time'], self.DATE_TIME_FORMAT)
        coords = lambda c: '%f,%f' % (c['latitude'], c['longitude'])

        params = {
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M:%S'),
            'arriveBy': (test['timeType'] == 'A'),
            'optimize': 'QUICK',
            'mode': 'WALK,TRANSIT',
            'walkSpeed': 1.389,
            'numItineraries': 1,
            'disableRemainingWeightHeuristic': True,
            'nonpreferredTransferPenalty': 30,
            'otherThanPreferredRoutesPenalty': 0,
            'walkBoardCost': 0,
            'bikeBoardCost': 0,
        }

        # If lat/lon use lat,lon otherwise use the provided stopid (rewritten format from given 1a1 to expected MMRI_1a1)
        if type(test['to']) is dict:
            params['fromPlace'] = coords(test['from'])
            params['toPlace'] = coords(test['to'])
        else:
            prefix = ''
            if test.get('agencyId'):
                prefix = test['agencyId'] + '_'
            if test.get('from'):
                params['fromPlace'] = '%s%s' % (prefix, test['from'])
            if test.get('to'):
                params['toPlace'] = '%s%s' % (prefix, test['to'])

        # if wheelchairAccessible is set, set the wheelchairAccessible param (true or false)
        if not test.get('wheelchairAccessible') is None:
            params['wheelchair'] = test['wheelchairAccessible']

        # if startTransitTripId is set, set the startTransitTripId param for onboard planning (rewritten format from given 2f|intercity to expected MMRI_2f|intercity)
        # NB: This is untested, not sure wether this is the correct way to pass along on-board planning or that other params should be changed as well
        if not test.get('startTransitTripId') is None:
            params['startTransitTripId'] = '%s_%s' % (test['agencyId'], test['startTransitTripId'])

        # If preferLeastTransfers is set to true, set the transferPenalty param to a value that makes sense
        # NB: This transferPenalty is just picked at random, no idea wether it will actually make the accompanying test pass
        if not test.get('preferLeastTransfers') is None:
            params['transferPenalty'] = 180

        # If preferredTravelTypes is set, add it as the only mode next to walk in the mode param
        # NB: Is this actually complying to the test? As we're just removing the ability to go by train, instead of increasing a preference. Any better API param we can set?
        if not test.get('preferredTravelType') is None:
            params['mode'] = 'WALK,%s' % test['preferredTravelType'].upper()

        # If a bannedRoute is set, add it to the bannedRoutes param (rewritten format from given 3d|1 to expected MMRI_3d|1)
        # NB: Perhaps we should use unpreferredRoutes here?
        if not test.get('bannedRoute') is None:
            params['bannedRoutes'] = '%s_%s' % (test['agencyId'], test['bannedRoute'])

        # If a bannedStop is set, add it to the bannedStopsHard param (rewritten format from given 3f2 to expected MMRI_3f2)
        if not test.get('bannedStop') is None:
            params['bannedStopsHard'] = '%s_%s' % (test['agencyId'], test['bannedStop'])

        url = self.options.url + '?%s' % urllib.urlencode(params)
        return url

    def parse_result(self, test, result):
        if result['error'] is None:
            return self.parse_itinerary(test, result)
        else:
            return self.parse_error(test, result)

    def parse_itinerary(self, test, result):
        itinerary = result['plan']['itineraries'][0]
        return {
            'id': test['id'],
            'legs': [self.parse_leg(leg) for leg in itinerary['legs'] if leg['mode'] != 'WALK'],
        }

    def get_stop_id(self, direction, leg):
        if leg and leg[direction] and leg[direction]['stopId'] and leg[direction]['stopId']['id']:
            return leg[direction]['stopId']['id']
        return None

    def parse_leg(self, leg):
        result = {
            'departureTime': self.jsonDateTime(leg['startTime']),
            'arrivalTime': self.jsonDateTime(leg['endTime']),
            'departureStopId': self.get_stop_id('from', leg),
            'arrivalStopId': self.get_stop_id('to', leg),
            'line': '%(route)s (%(headsign)s)' % leg,
        }

        if leg.get('alerts') is not None and leg.get('alerts', [{}])[0].get('alertHeaderText', {}).get('someTranslation', {}) is not None:
            result['alert'] = leg['alerts'][0]['alertHeaderText']['translsomeTranslationations']
        return result

    def parse_error(self, test, result):
        return {
            'id': test['id'],
            'error': result['error']['msg'],
        }
