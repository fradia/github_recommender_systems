import json
import requests
import argparse

def export_predictions(file_i, file_o):
    i=open(file_i,'r')
    next(i)
    users=[line.rstrip('\r\n').split(',')[0] for line in i]
    i.close()
    o=open(file_o,'a')
    for user in set(users):
        l=dict()
        d={'user':user}
        h = {'Content-type': 'application/json'}
        r=requests.post('http://localhost:8000/queries.json',data=json.dumps(d),headers=h)
        #extract text:
        extr=r.text
        if len(extr)<2:
            continue
        else:
            #get the list of the scores as string:
            scores=extr[0:len(extr)-1].split('{"itemScores":')[1]
            l='{"user_id":'+'"'+user+'"'+',"rec":'+scores+'}'
            o.write(l+'\n')
    o.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="Export recommendations")
  parser.add_argument('--file_i', default="./data/forks_stars_sample_train.csv")
  parser.add_argument('--file_o',default="./data/forks_stars_sample_ur_predictions_train.json")
  
  args = parser.parse_args()
  export_predictions(args.file_i,args.file_o)
