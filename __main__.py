from bitdeli import profile_events
from bitdeli.protocol import params, done
from bitdeli.chunkedlist import ChunkedList
from datetime import datetime, timedelta
import json

PARAMS = params()
PROFILE_RETENTION = 365
TFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

for profile, events in profile_events():
    for event in events:
        name = json.loads(event.object.data)['$event_name']
        key = name if name[0] == '$' else 'events'
        c = profile.get(key)
        if c == None:
            c = profile[key] = ChunkedList()
        c.push([(event.timestamp, event.groupkey, event.ip, event.object)])
    too_old = datetime.strftime(datetime.strptime(event.timestamp, TFORMAT) -\
                                timedelta(days=PROFILE_RETENTION), TFORMAT)
    for key, lst in profile.iteritems():
        if key[0] != '!':
            lst.drop_chunks(lambda x: x[0] > too_old)
    #profile.set_expire(PROFILE_RETENTION)

done()
