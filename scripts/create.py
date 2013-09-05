import json
import sys

infile = open('benchmark_points_with_stops.json','r')
outfile = open('benchmark_requests.json','w', 1)
outfile_otp = open('benchmark_requests_otp.json','w', 1)

tests = json.load(infile)
results = []
results_otp = []
for i, test in enumerate(tests):
	result = {
		'id': 'benchmarktest_%d' % i,
        'from': '%s' % test['start']['stop_id'],
        'to': '%s' % test['stop']['stop_id'],
        'time': '2013-05-15T12:00:00',
        'timeType': 'D',
	}
	result_otp = {
		'id': 'benchmarktest_%d' % i,
        'from': '%s_%s' % (test['start']['feed_id'], test['start']['stop_id']),
        'to': '%s_%s' % (test['stop']['feed_id'], test['stop']['stop_id']),
        'time': '2013-05-15T12:00:00',
        'timeType': 'D',
	}
	results.append(result)
	results_otp.append(result_otp)

json.dump(results, outfile, indent=4, sort_keys=True)
json.dump(results_otp, outfile_otp, indent=4, sort_keys=True)

infile.close()
outfile.close()
outfile_otp.close()
