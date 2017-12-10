import predictionio
import argparse
import random
import datetime
import pytz

def import_data(client,file):
    count=0
    now_date = datetime.datetime.now(pytz.utc)  # - datetime.timedelta(days=2.7)
    current_date = now_date
    f=open(file,'r')
    #next(f)
    print('Importing data...')
    for line in f:
        data=line.rstrip('\r\n').split(',')
        client.create_event(
            event=data[3],
            entity_type="user",
            entity_id=data[0],
            target_entity_type="item",
            target_entity_id=data[1],
            #event_time=current_date
        )
        print("Event: " + data[3] + " entity_id: " + data[0] + " target_entity_id: " + data[1])
        count=count+1
    f.close()
    print("%s events are imported") % count

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="Import sample data for recommendation engine")
  parser.add_argument('--access_key', default='invald_access_key')
  parser.add_argument('--url', default="http://localhost:7070")
  parser.add_argument('--file', default="forks_stars_sample_prepared_train.csv")

  args = parser.parse_args()
  print(args)
  client = predictionio.EventClient(
    access_key=args.access_key,
    url=args.url,
    threads=5,
    qsize=500)
  import_data(client, args.file)
