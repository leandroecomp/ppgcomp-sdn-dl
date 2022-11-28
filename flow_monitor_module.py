#!/usr/bin/python
# -*- coding: utf-8 -*-
# flow_monitor_module.py
import time
import hashlib
import csv
from collections import defaultdict
import requests
import config

d = {}
d = defaultdict(dict)

def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

def hash_MD5(match):
    string = "".join(match)
    result = hashlib.md5(str(string).encode("utf-8")).hexdigest()
    return result

def get_flows(url):
    return requests.get(url)

def parse_flows(response):
    return response.json()

INPUT_FILE = "datasets/input.csv"

URL = "http://192.168.255.254:8080/stats/flow/1"

f = open(INPUT_FILE, "w", newline="")
f.truncate()
write_flows = csv.writer(f, delimiter=";")

header = [
    "sample",
    "id_flow",
    "OVS_start_flow",
    "OVS_duration_flow",
    "OVS_packet_count",
    "OVS_byte_count",
    "nw_src",
    "tp_src",
    "nw_dst",
    "tp_dst",
    "nw_proto",
]

writer.writerow(header)
f.close()
sample = 1
while True:

    response = get_flows(URL)
    now_time = float(time.time())
    data = parse_flows(response)
    elements = data["1"]
    print("Snapshot #%3d" % sample)
    f = open(INPUT_FILE, "a", newline="")
    writer = csv.writer(f, delimiter=";")

    for x in elements:
        if x["priority"] == 100:

            OVS_duration_sec = float(x["duration_sec"])
            OVS_duration_nsec = float(x["duration_nsec"] / 10**9)
            OVS_duration_flow = OVS_duration_sec + OVS_duration_nsec
            OVS_packet_count = x["packet_count"]
            OVS_byte_count = x["byte_count"]

            priority = x["priority"]
            dl_type = x["match"]["dl_type"]
            nw_proto = x["match"]["nw_proto"]
            nw_src = x["match"]["nw_src"]
            nw_dst = x["match"]["nw_dst"]
            if nw_proto == 1:
                tp_src = 0
                tp_dst = 0
            else:
                tp_src = x["match"]["tp_src"]
                tp_dst = x["match"]["tp_dst"]

            id_flow = hash_MD5(
                [nw_src, str(tp_src), nw_dst, str(tp_dst), str(nw_proto)]
            )

            OVS_start_flow = now_time - OVS_duration_flow

            print(  # OVS_start_flow,
                # OVS_duration_flow,
                sample,
                id_flow,
                OVS_packet_count,
                OVS_byte_count,
                nw_src,
                tp_src,
                nw_dst,
                tp_dst,
                nw_proto,
            )

            write_flows.writerow(
                [
                    sample,
                    id_flow,
                    OVS_start_flow,
                    OVS_duration_flow,
                    OVS_packet_count,
                    OVS_byte_count,
                    nw_src,
                    tp_src,
                    nw_dst,
                    tp_dst,
                    nw_proto,
                ]
            )

    f.close()
    sample += 1

    for i in range(config.REQUEST_TIME):
        time.sleep(1)

f.close()
