import os
import math
import random
import argparse

def poisson_arrival(flow: float, period: float):
    t = 0
    arrival_list = []
    while(t < period):
        u = random.random()
        x = -math.log(1-u) / flow
        arrival_list.append(t)
        t = t + x
    return arrival_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--flow', type=float, help='Traffic Flow (veh/s)')
    parser.add_argument('--period', type=float, help='Period (s)')
    parser.add_argument('--output_path', type=str, help='The path of output file.')
    args = parser.parse_args()

    dir = [0, 2]
    route = [0, 1, 2, 3, 4, 5]
    
    random.seed(0)
    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)

    output = [''] * len(dir)
    arrival_list = poisson_arrival(args.flow, args.period)

    for veh in range(len(arrival_list)):
        dir_idx = random.randint(0, len(dir) - 1)
        route_idx = random.randint(0, len(route) - 1)
        time = round(arrival_list[veh] * 100)

        output[dir_idx] += '1`({}, {})@{}++\n'.format(dir[dir_idx], route[route_idx], time)

    for i in range(len(output)):
        output[i] = output[i].rstrip('++\n')
    
    file_name = 'flow_{}_period_{}.txt'.format(args.flow, args.period)
    fp = open(os.path.join(args.output_path, file_name), 'w')
    
    for i in range(len(output)):
        fp.write(output[i])
        if i != (len(output) - 1):
            fp.write('\n\n')