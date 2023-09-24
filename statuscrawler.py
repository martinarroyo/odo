# https://github.com/giampaolo/psutil/blob/master/psutil/_pslinux.py
# https://github.com/qrees/tornado-chat/tree/master/common
import os
import subprocess
import time

import tornado
from time import localtime, mktime

import conf

SUBPROCESS_OPTS = {'shell': False, 'stdout': tornado.process.Subprocess.STREAM}

def extract_cpu_info(cpu_info):
    result = []
    for cpu in cpu_info:
        cpu = cpu.split()
        cpu = cpu[-11:]
        result.append({
            "cpu": cpu[0],
            "usr": float(cpu[1].replace(',', '.')),
            "nice": float(cpu[2].replace(',', '.')),
            "sys": float(cpu[3].replace(',', '.')),
            "iowait": float(cpu[4].replace(',', '.')),
            "irq": float(cpu[5].replace(',', '.')),
            "soft": float(cpu[6].replace(',', '.')),
            "steal": float(cpu[7].replace(',', '.')),
            "guest": float(cpu[8].replace(',', '.')),
            "gnice": float(cpu[9].replace(',', '.')),
            "idle": float(cpu[10].replace(',', '.')),
        })
    return result

async def get_network_info():
    p1 = tornado.process.Subprocess(["netstat", "-i"], stdout=subprocess.PIPE)
    p2 = tornado.process.Subprocess(["tail", "-n", "+2"], stdin=p1.stdout, **SUBPROCESS_OPTS)
    network_result = await p2.stdout.read_until_close()
    network_result = network_result.decode('utf-8').strip()
    network_result = network_result.split("\n")
    header = network_result[0].split()
    interfaces = network_result[1:]
    result = []
    for iface in interfaces:
        result.append({key: value for key, value in zip(header, iface.split())})
    return result

async def get_uptime():
    p1 = tornado.process.Subprocess("uptime", stdout=subprocess.PIPE)
    p2 = tornado.process.Subprocess(["tail", "-n", "1"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = tornado.process.Subprocess(["awk", "{print $3 $4 $5}"], stdin=p2.stdout, **SUBPROCESS_OPTS)

    uptime_result = await p3.stdout.read_until_close()
    return uptime_result.decode('utf-8').strip()

async def get_memory_data():
    memory = {}

    egrep1 = tornado.process.Subprocess(["egrep", "--color", "^(MemTotal|MemFree|Buffers|Cached|SwapTotal|SwapFree)", "/proc/meminfo"], stdout=subprocess.PIPE)
    memory_data_process = tornado.process.Subprocess(["egrep", "[a-zA-Z]+:( )+[0-9.]+", "-o"], stdin=egrep1.stdout, **SUBPROCESS_OPTS)
    memory_data = (await memory_data_process.stdout.read_until_close()).decode('utf-8').strip()

    memory_data = [e.split(":") for e in memory_data.split("\n")]

    for entry in memory_data:
        memory[entry[0]] = int(entry[1].strip())

    return memory

async def get_load_data():
    # https://raymii.org/s/snippets/Get_uptime_load_and_users_with_grep_sed_and_awk.html
    p1 = tornado.process.Subprocess("uptime", stdout=subprocess.PIPE)
    p2 = tornado.process.Subprocess(["grep", "-ohe", "load average[s:][: ].*"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = tornado.process.Subprocess(["awk", "{ print $3\" \"$4\" \"$5 }"], stdin=p2.stdout, **SUBPROCESS_OPTS)
    load_data = (await p3.stdout.read_until_close()).decode('utf-8').strip().split(', ') 
    load_average = {'1min': float(load_data[0].replace(',', '.')), '5min': float(load_data[1].replace(',', '.')), '15min': float(load_data[2].replace(',', '.'))}
    return load_average

async def get_rx():
    # TODO: Replace with /proc/net/dev: https://serverfault.com/a/533523/284322
    return int((await tornado.process.Subprocess("/sbin/ifconfig eth0 | grep \"RX bytes\" | awk '{ print $2 }' | cut -d\":\" -f2", **SUBPROCESS_OPTS).stdout.read_until_close()).decode('utf-8').strip())

async def get_tx():
     return int((await tornado.process.Subprocess("/sbin/ifconfig eth0 | grep \"TX bytes\" | awk '{ print $2 }' | cut -d\":\" -f2", **SUBPROCESS_OPTS).stdout.read_until_close()).decode('utf-8').strip())

async def get_cpu_info():
    p1 = tornado.process.Subprocess([os.path.join(conf.BASE_DIR, "./mpstat/mpstat"), "-P", "ALL", "1", "1"], stdout=subprocess.PIPE)
    p2 = tornado.process.Subprocess(["tail", "-n", "+4"], stdin=p1.stdout, **SUBPROCESS_OPTS)
    cpu_info = (await p2.stdout.read_until_close()).decode('utf-8').strip().split('\n')
    return extract_cpu_info(cpu_info)

async def get_data():
    """
    Reads data sources and outputs a dictionary containing the results
    """
    response_dict = {}
    response_dict["time"] = mktime(localtime())*1000.0
    fd_uname = tornado.process.Subprocess(["uname", "-r"], **SUBPROCESS_OPTS).stdout

    uname_result = await fd_uname.read_until_close()
    uname_result = uname_result.decode('utf-8').strip()
    response_dict["uname"] = uname_result
    response_dict["uptime"] = await get_uptime()
    response_dict["memory"] = await get_memory_data()

    response_dict["load_average"] = await get_load_data()

    response_dict["cpu"] = await get_cpu_info()

    response_dict["network"] = await get_network_info()
    response_dict["timestamp"] = time.time()

    return response_dict
