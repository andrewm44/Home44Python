#!/usr/bin/env python3
import argparse
import base64
import codecs
import time
from . import gendevice


TICK = 32.84
TIMEOUT = 30
IR_TOKEN = 0x26


def auto_int(x):
    return int(x, 0)


def to_microseconds(bytes):
    result = []
    #  print bytes[0] # 0x26 = 38for IR
    index = 4
    while index < len(bytes):
        chunk = bytes[index]
        index += 1
        if chunk == 0:
            chunk = bytes[index]
            chunk = 256 * chunk + bytes[index + 1]
            index += 2
        result.append(int(round(chunk * TICK)))
        if chunk == 0x0d05:
            break
    return result


def durations_to_broadlink(durations):
    result = bytearray()
    result.append(IR_TOKEN)
    result.append(0)
    result.append(len(durations) % 256)
    result.append(len(durations) / 256)
    for dur in durations:
        num = int(round(dur / TICK))
        if num > 255:
            result.append(0)
            result.append(num / 256)
        result.append(num % 256)
    return result


def format_durations(data):
    result = ''
    for i in range(0, len(data)):
        if len(result) > 0:
            result += ' '
        result += ('+' if i % 2 == 0 else '-') + str(data[i])
    return result


def parse_durations(str):
    result = []
    for s in str.split():
        result.append(abs(int(s)))
    return result

def testsend():
    devtype = 0x649b
    host = "192.168.1.88"
    mac = bytearray.fromhex("ec0bae3df6e0")

    dev = gendevice(devtype, (host, 80), mac)
    dev.auth()

    testdata = "b1c09401ce9e06000d160d0a18160d150d160d150d0b170c170b170c17160c0c160c17170b170c170b170c0c160001fb0a160d0b17160c170c160c170c0b170c170b170c16170c0c160c17170b170c170b170c0c160001f90c160d0b17160c170c160c170c0b170c170c160c17160c0c170c16170b180b170b180b0c160001f80d170b0c17160c170c160c170c0c160c170c160c17170b0c170c16170b170c170b180b0c170001f80c160d0b17170b170c170b170c0c160c170c160c17170b0c170c16170c170b170c170b0c170001f80c170c0b17160d160c170b170c0c160c170c160c17170b0c170c16170c170b170c170b0c170001f80c170c0b17170c160c170c160c0c160c170c160c17170b0d160c16170c170b170c170c0c160001f80c170c0c16170c160c170c160c0c170b170c170c16170b0d160c16180b170b180b170c0c160001f80c170c0c16170c170c160c170c0b170c160c170c16170c0c160d16170b170c170b170c0c160001f90b170c0c17160c170c160c170c0c160c170c160c17170b0c170c16170c170b170b180b0c170005dc"

    data = bytearray.fromhex(''.join(testdata))

    dev.send_data(data)

def sendcmd(senddcmd):
    devtype = 0x649b
    host = "192.168.1.88"
    mac = bytearray.fromhex("ec0bae3df6e0")

    dev = gendevice(devtype, (host, 80), mac)
    dev.auth()

    match senddcmd:
        case "extractorlight":
            print("sending extractor light")
            senddata = "b1c09401ce9e06000d160d0a18160d150d160d150d0b170c170b170c17160c0c160c17170b170c170b170c0c160001fb0a160d0b17160c170c160c170c0b170c170b170c16170c0c160c17170b170c170b170c0c160001f90c160d0b17160c170c160c170c0b170c170c160c17160c0c170c16170b180b170b180b0c160001f80d170b0c17160c170c160c170c0c160c170c160c17170b0c170c16170b170c170b180b0c170001f80c160d0b17170b170c170b170c0c160c170c160c17170b0c170c16170c170b170c170b0c170001f80c170c0b17160d160c170b170c0c160c170c160c17170b0c170c16170c170b170c170b0c170001f80c170c0b17170c160c170c160c0c160c170c160c17170b0d160c16170c170b170c170c0c160001f80c170c0c16170c160c170c160c0c170b170c170c16170b0d160c16180b170b180b170c0c160001f80c170c0c16170c170c160c170c0b170c160c170c16170c0c160d16170b170c170b170c0c160001f90b170c0c17160c170c160c170c0c160c170c160c17170b0c170c16170c170b170b180b0c170005dc"
        case _:
            senddata = ""
            print("unhandled command")

    data = bytearray.fromhex(''.join(senddata))

    dev.send_data(data)
