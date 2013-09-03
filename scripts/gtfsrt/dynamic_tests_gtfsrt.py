from gtfs_realtime_pb2 import FeedMessage, FeedHeader, TripUpdate, TripDescriptor

feedmessage = FeedMessage()
feedmessage.header.gtfs_realtime_version = "1.0"
feedmessage.header.incrementality = FeedHeader.FULL_DATASET

feedmessage.header.timestamp = 1388530800 # 2014-01-01

feedentity = feedmessage.entity.add()
feedentity.id = '3b'
feedentity.trip_update.trip.start_date = '20140101'
feedentity.trip_update.trip.trip_id = '3b|1'
update = feedentity.trip_update.stop_time_update.add()
update.stop_sequence = 0
update.stop_id = '3b1'
update.departure.delay = 600

feedentity = feedmessage.entity.add()
feedentity.id = '3b|2'
feedentity.trip_update.trip.start_date = '20140101'
feedentity.trip_update.trip.trip_id = '3b|2'
update = feedentity.trip_update.stop_time_update.add()
update.stop_sequence = 1
update.stop_id = '3b1'
update.departure.delay = 60

f = open("/tmp/3b.pb", "wb")
f.write(feedmessage.SerializeToString())
f.close()

feedmessage = FeedMessage()
feedmessage.header.gtfs_realtime_version = "1.0"
feedmessage.header.incrementality = FeedHeader.FULL_DATASET

feedmessage.header.timestamp = 1388531040 # 2014-01-01 00:04

feedentity = feedmessage.entity.add()
feedentity.id = '3c'
feedentity.trip_update.trip.start_date = '20140101'
feedentity.trip_update.trip.trip_id = '3c|1'
update = feedentity.trip_update.stop_time_update.add()
update.stop_sequence = 2
update.stop_id = '3c2'
update.arrival.delay = 120

f = open("/tmp/3c.pb", "wb")
f.write(feedmessage.SerializeToString())
f.close()

feedmessage = FeedMessage()
feedmessage.header.gtfs_realtime_version = "1.0"
feedmessage.header.incrementality = FeedHeader.FULL_DATASET

feedmessage.header.timestamp = 1388531040 # 2014-01-01 00:04

feedentity = feedmessage.entity.add()
feedentity.id = '3e'
feedentity.trip_update.trip.start_date = '20140101'
feedentity.trip_update.trip.trip_id = '3e|1'
feedentity.trip_update.trip.schedule_relationship = TripDescriptor.CANCELED

f = open("/tmp/3e.pb", "wb")
f.write(feedmessage.SerializeToString())
f.close()


feedmessage = FeedMessage()
feedmessage.header.gtfs_realtime_version = "1.0"
feedmessage.header.incrementality = FeedHeader.FULL_DATASET

feedmessage.header.timestamp = 1388530800 # 2014-01-01

feedentity = feedmessage.entity.add()
feedentity.id = '3i'
translation = feedentity.alert.header_text.translation.add()
translation.text = 'Unknown effect'
entityselector =  feedentity.alert.informed_entity.add()
entityselector.route_id = '3i|1'

f = open("/tmp/3i.pb", "wb")
f.write(feedmessage.SerializeToString())
f.close()


feedmessage = FeedMessage()
feedmessage.header.gtfs_realtime_version = "1.0"
feedmessage.header.incrementality = FeedHeader.FULL_DATASET

feedmessage.header.timestamp = 1388530800 # 2014-01-01

feedentity = feedmessage.entity.add()
feedentity.id = 'plannerstack_scenario'
feedentity.trip_update.trip.start_date = '20140101'
feedentity.trip_update.trip.trip_id = 'plannerstack_scenario|intercity'
update = feedentity.trip_update.stop_time_update.add()
update.stop_sequence = 1
update.stop_id = 'plannerstack_scenario1'
update.departure.delay = 600

f = open("/tmp/plannerstack_scenario1.pb", "wb")
f.write(feedmessage.SerializeToString())
f.close()
