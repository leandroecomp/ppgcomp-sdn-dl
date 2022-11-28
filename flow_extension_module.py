#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from collections import defaultdict
import hashlib
import csv
import config
from lib.flow import Flow
from lib.traffic import Traffic

INPUT_FILE = 'datasets/input - facebook-audio.csv'
OUTPUT_FILE = 'datasets/output - facebook-audio.csv'

def hash_MD5(match):
    string = ''.join(match)
    result = hashlib.md5(str(string).encode('utf-8')).hexdigest()
    return result

f = open(OUTPUT_FILE, 'w', newline='')
f.truncate()
writer = csv.writer(f, delimiter=';')

header = [
    'id_flow','nw_src','tp_src',
    'nw_dst','tp_dst','nw_proto',
    'request_pc','request_bc','request_pl','request_piat','request_pps','request_bps',
    'request_pl_mean','request_piat_mean','request_pps_mean','request_bps_mean',
    'request_pl_var','request_piat_var','request_pps_var','request_bps_var',
    'request_pl_q1','request_pl_q3','request_piat_q1','request_piat_q3','request_pl_max',
    'request_pl_min','request_piat_max','request_piat_min','request_pps_max','request_pps_min',
    'request_bps_max','request_bps_min',
    'replay_pc','replay_bc','replay_pl','replay_piat','replay_pps','replay_bps',
    'replay_pl_mean','replay_piat_mean','replay_pps_mean','replay_bps_mean',
    'replay_pl_var','replay_piat_var','replay_pps_var','replay_bps_var',
    'replay_pl_q1','replay_pl_q3','replay_piat_q1','replay_piat_q3',
    'replay_pl_max','replay_pl_min','replay_piat_max','replay_piat_min',
    'replay_pps_max','replay_pps_min','replay_bps_max','replay_bps_min',
    'category',
]
writer.writerow(header)

d = {}
d = defaultdict(dict)
active_flows = []
active_snapshot = 0

base = pd.read_csv(INPUT_FILE, sep=';')

for (index, row) in base.iterrows():
    OVS_start_flow = float(row['OVS_start_flow'])
    OVS_duration_flow = float(row['OVS_duration_flow'])
    OVS_packet_count = float(row['OVS_packet_count'])
    OVS_byte_count = float(row['OVS_byte_count'])

    sample = str(row['sample'])
    nw_src = str(row['nw_src'])
    tp_src = int(row['tp_src'])
    nw_dst = str(row['nw_dst'])
    tp_dst = int(row['tp_dst'])
    nw_proto = int(row['nw_proto'])

    request_id_flow = hash_MD5([nw_src, str(tp_src), nw_dst,str(tp_dst), str(nw_proto)])
    replay_id_flow = hash_MD5([nw_dst, str(tp_dst), nw_src,str(tp_src), str(nw_proto)])

    if int(sample) != active_snapshot:

        # grava em arquivo os arivos

        print('grava no arquivos os fluxos ativos')
        for x in range(len(active_flows)):
            if d[active_flows[x]].request is not None \
                    and d[active_flows[x]].replay is not None:
                if d[active_flows[x]].request.next_sample >= 1:

                    if d[active_flows[x]].request.pc != 0 \
                            and d[active_flows[x]].replay.pc != 0:

                        writer.writerow([
                            active_flows[x],
                            d[active_flows[x]].request.nw_src,
                            d[active_flows[x]].request.tp_src,
                            d[active_flows[x]].request.nw_dst,
                            d[active_flows[x]].request.tp_dst,
                            d[active_flows[x]].request.nw_proto,
                            '%.15f' % d[active_flows[x]].request.pc,
                            '%.15f' % d[active_flows[x]].request.bc,
                            '%.15f' % d[active_flows[x]].request.pl[-1],
                            '%.15f' % d[active_flows[x]].request.piat[-1],
                            '%.15f' % d[active_flows[x]].request.pps,
                            '%.15f' % d[active_flows[x]].request.bps,
                            '%.15f' % d[active_flows[x]].request.pl_mean,
                            '%.15f' % d[active_flows[x]].request.piat_mean,
                            '%.15f' % d[active_flows[x]].request.pps_mean,
                            '%.15f' % d[active_flows[x]].request.bps_mean,
                            '%.15f' % d[active_flows[x]].request.pl_var,
                            '%.15f' % d[active_flows[x]].request.piat_var,
                            '%.15f' % d[active_flows[x]].request.pps_var,
                            '%.15f' % d[active_flows[x]].request.bps_var,
                            '%.15f' % d[active_flows[x]].request.pl_q1,
                            '%.15f' % d[active_flows[x]].request.pl_q3,
                            '%.15f' % d[active_flows[x]].request.piat_q1,
                            '%.15f' % d[active_flows[x]].request.piat_q3,
                            '%.15f' % d[active_flows[x]].request.pl_max,
                            '%.15f' % d[active_flows[x]].request.pl_min,
                            '%.15f' % d[active_flows[x]].request.piat_max,
                            '%.15f' % d[active_flows[x]].request.piat_min,
                            '%.15f' % d[active_flows[x]].request.pps_max,
                            '%.15f' % d[active_flows[x]].request.pps_min,
                            '%.15f' % d[active_flows[x]].request.bps_max,
                            '%.15f' % d[active_flows[x]].request.bps_min,
                            '%.15f' % d[active_flows[x]].replay.pc,
                            '%.15f' % d[active_flows[x]].replay.bc,
                            '%.15f' % d[active_flows[x]].replay.pl[-1],
                            '%.15f' % d[active_flows[x]].replay.piat[-1],
                            '%.15f' % d[active_flows[x]].replay.pps,
                            '%.15f' % d[active_flows[x]].replay.bps,
                            '%.15f' % d[active_flows[x]].replay.pl_mean,
                            '%.15f' % d[active_flows[x]].replay.piat_mean,
                            '%.15f' % d[active_flows[x]].replay.pps_mean,
                            '%.15f' % d[active_flows[x]].replay.bps_mean,
                            '%.15f' % d[active_flows[x]].replay.pl_var,
                            '%.15f' % d[active_flows[x]].replay.piat_var,
                            '%.15f' % d[active_flows[x]].replay.pps_var,
                            '%.15f' % d[active_flows[x]].replay.bps_var,
                            '%.15f' % d[active_flows[x]].replay.pl_q1,
                            '%.15f' % d[active_flows[x]].replay.pl_q3,
                            '%.15f' % d[active_flows[x]].replay.piat_q1,
                            '%.15f' % d[active_flows[x]].replay.piat_q3,
                            '%.15f' % d[active_flows[x]].replay.pl_max,
                            '%.15f' % d[active_flows[x]].replay.pl_min,
                            '%.15f' % d[active_flows[x]].replay.piat_max,
                            '%.15f' % d[active_flows[x]].replay.piat_min,
                            '%.15f' % d[active_flows[x]].replay.pps_max,
                            '%.15f' % d[active_flows[x]].replay.pps_min,
                            '%.15f' % d[active_flows[x]].replay.bps_max,
                            '%.15f' % d[active_flows[x]].replay.bps_min,
                            d[active_flows[x]].category,
                        ])

                print(active_flows[x])
                print(d[active_flows[x]].request.pc)

        active_flows = []
        active_snapshot = int(sample)
        print('Snap atual %d' % active_snapshot)

    if request_id_flow in d:

        if not d[request_id_flow].request:
            d[request_id_flow].request = Flow(
                nw_src,
                tp_src,
                nw_dst,
                tp_dst,
                nw_proto,
                config.REQUEST_TIME,
            )

        d[request_id_flow].request.update(OVS_duration_flow,
                                          OVS_packet_count, OVS_byte_count)
        if request_id_flow not in active_flows:
            active_flows.append(request_id_flow)
    elif replay_id_flow in d:

        if not d[replay_id_flow].replay:

            d[replay_id_flow].replay = Flow(
                nw_src,
                tp_src,
                nw_dst,
                tp_dst,
                nw_proto,
                config.REQUEST_TIME,
            )

        d[replay_id_flow].replay.update(OVS_duration_flow,
                                          OVS_packet_count, OVS_byte_count)
        if replay_id_flow not in active_flows:
            active_flows.append(replay_id_flow)
    else:

        tf = Traffic()

        if config.PORTDICT[nw_proto][tp_dst]:  # existe uma porta cadastrada
            tf.category = config.PORTDICT[nw_proto][tp_dst]

            # print("Code 6  : porta de destino %s" % nw_src )

            d[request_id_flow] = tf
            d[request_id_flow].request = Flow(
                nw_src,
                tp_src,
                nw_dst,
                tp_dst,
                nw_proto,
                config.REQUEST_TIME,
            )
            d[request_id_flow].request.update(OVS_duration_flow,
                                              OVS_packet_count, OVS_byte_count)
            if request_id_flow not in active_flows:
                active_flows.append(request_id_flow)
        elif config.PORTDICT[nw_proto][tp_src]:

            tf.category = config.PORTDICT[nw_proto][tp_src]

            d[replay_id_flow] = tf
            d[replay_id_flow].replay = Flow(
                nw_src,
                tp_src,
                nw_dst,
                tp_dst,
                nw_proto,
                config.REQUEST_TIME,
            )
            d[replay_id_flow].replay.update(OVS_duration_flow,
                                              OVS_packet_count, OVS_byte_count)
            if replay_id_flow not in active_flows:
                active_flows.append(replay_id_flow)
        else:
            tf.category = '--UNKNOWN--'

            d[request_id_flow] = tf
            d[request_id_flow].request = Flow(
                nw_src,
                tp_src,
                nw_dst,
                tp_dst,
                nw_proto,
                config.REQUEST_TIME,
            )
            d[request_id_flow].request.update(OVS_duration_flow,
                                              OVS_packet_count, OVS_byte_count)

f.close()

base_final = pd.read_csv(OUTPUT_FILE, sep=';')
