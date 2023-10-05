import os
import math
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--non_delay', default='./non_delay', help='The directory of non_delay files.')
    parser.add_argument('--delay', required=True, help='The directory of delay files.')
    args = parser.parse_args()

    files = sorted(os.listdir(args.non_delay))

    for idx in range(len(files)):
        print('====== {} ======'.format(files[idx]))
        nbr_veh, nbr_mor = 0, 0
        delay_veh, delay_mor = 0, 0
        non_delay_veh, non_delay_mor = 0, 0

        fp_non_delay = open(os.path.join(args.non_delay, files[idx]), 'r')
        ln_non_delay = fp_non_delay.readlines()
        fp_delay = open(os.path.join(args.delay, files[idx]), 'r')
        ln_delay = fp_delay.readlines()

        if ln_delay[0].find('deadlock') != -1:
            print('adt_veh:', math.inf)
            print('adt_mor:', math.inf)
            print('adt_tot:', math.inf)
            continue

        for ln_idx in range(len(ln_non_delay)):
            ln_nd = ln_non_delay[ln_idx].split('@')
            nbr_nd = int(ln_nd[0].split('`')[0])
            type_nd = int(ln_nd[0][-2])
            time_nd = float(ln_nd[1].split('+')[0])

            if type_nd < 3:
                nbr_mor += nbr_nd
                non_delay_mor += nbr_nd * time_nd
            else:
                nbr_veh += nbr_nd
                non_delay_veh += nbr_nd * time_nd

        for ln_idx in range(len(ln_delay)):
            ln_d = ln_delay[ln_idx].split('@')
            nbr_d = int(ln_d[0].split('`')[0])
            type_d = int(ln_d[0][-2])
            time_d = float(ln_d[1].split('+')[0])

            if type_d < 3:
                delay_mor += nbr_d * time_d
            else:
                delay_veh += nbr_d * time_d

        adt_veh = (delay_veh - non_delay_veh) / nbr_veh / 100
        adt_mor = (delay_mor - non_delay_mor) / nbr_mor / 100
        adt_total = (delay_veh - non_delay_veh + delay_mor - non_delay_mor) / (nbr_veh + nbr_mor) / 100
        print('adt_veh: {:.2f}'.format(adt_veh))
        print('adt_mor: {:.2f}'.format(adt_mor))
        print('adt_tot: {:.2f}'.format(adt_total))