import csv
import requests
import sys

#initialize API URL target
URL = "https://api.syf.com/--/---------/--------/--------*-------"

# Initialize Auth header
HEAD = {'*-***-******-**':'*******************************'}

#input data ************************************************************************
sp_data = '**_***_*.csv'

# declare resources
firstlineswitch = 0
output = []
counter204 = 0
total = 0
tracker204 = []
errors = []

# index of Phone Cleared parameter ************************************************************************
idxphone = 6

with open(sp_data) as csvfile:
    CSV = csv.reader(csvfile, delimiter=',')

    for row in CSV:

        #ignore CSV header
        if firstlineswitch == 0:
            firstlineswitch = 1
            continue

        #catch blank rows
        if not row[idxphone]:
            continue

        #initialize API Parameters
        PARAM = {'phone':row[idxphone]}

        #send GET request
        r = requests.get(url=URL, params = PARAM, headers = HEAD)

        #catch 204 response, increase counter, and log phone number that triggered 204
        if r.status_code == 204:
            tracker204.append(row[idxphone])
            counter204 += 1

        #assume 200 OK response from API
        elif r.status_code == 200:
            data = r.json()

            # try to pull MID and PCGC from API response and append to output list************************************************************************
            try:
                qa = data['results'][0]
                output.append((row[idxphone], qa['********ID'], qa['****'], row[1]))
            #sometimes request fails, if request fails then log phone in errors
            except:
                errors.append(((row[idxphone])))

        # if we don't recieve a 200 or a 204, break
        else:
            print(str(row[idxphone]) + ' recieved a ' + str(r.status_code) + ', script will now exit -- godspeed!')
            sys.exit()

        total+=1

        print('status code=' + str(r.status_code))
        print('incidences of 204='+ str(counter204))
        print('total='+ str(total))
        print('_________')

# ~ANALYTICS~!************************************************************************
print('total ratio of 204/completed requests: '+ str(counter204) + '/' + str(total))
print(tracker204) # list of phone numbers that triggered 204 response
# print(errors) # list of phone numbers for which the request failed
# print(len(errors)) # number of failed requests

#write output to csv file
with open('ur file.csv','w') as out:
    csv_out=csv.writer(out)
    for row in output:
        csv_out.writerow(row)
