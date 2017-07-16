import sim
import csv
import sys

TRIALS = 10000

def main(players=1):
    filename = 'not_alone_card_value_data_' + unicode(players)  + '.csv'
    with open(filename, 'w') as csvfile:
        fieldnames = [
            'players',
            'hunted', 
            'artemia', 
            'survival card value',
            'hunt card value',
            'rounds',
        ]

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
    hunt_val = 0
    data = []
    while hunt_val <= 1.0:

        survival_val = 0
        while survival_val <= 1.0:
            data.append(sim.sim(players, TRIALS, hunt_val, survival_val, False))
            print 'players ' + unicode(players)
            print 'hunt ' + unicode(hunt_val)
            print 'suvive' + unicode(survival_val)
            survival_val = round(survival_val + 0.05, 2)
        hunt_val = round(hunt_val + 0.05, 2)

    with open(filename, 'a') as csvfile:
        fieldnames = [
            'players',
            'hunted', 
            'artemia', 
            'survival card value',
            'hunt card value',
            'rounds',
        ]

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        for x in data:
            writer.writerow(x)
if __name__ == '__main__':
    players = 1
    if len(sys.argv) > 1:
        players = int(sys.argv[1])
    try:
        main(players)
    except:
        print 'probably invalid arguement'
