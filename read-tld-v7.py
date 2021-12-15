#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
from ipaddress import IPv4Address
import sys
import sqlite3

# sys.argv is a list, which contains the command-line arguments passed to the script.
# The first item of this list contains the name of the script itself.
filename = sys.argv[1]

# Satellite control system time started from January 1, 2014 00:00:00 (UTC + 8)
beijing_time = timezone(timedelta(hours=8))
scs_epoch = datetime(2014, 1, 1, tzinfo=beijing_time).timestamp()

# Number of packets
count = 0

LTU_ips = {
    IPv4Address("172.16.1.11"): "LTU1_1",
    IPv4Address("172.16.1.21"): "LTU2.1",
    IPv4Address("172.16.1.31"): "LTU3.1",
    IPv4Address("172.16.1.12"): "LTU1.2",
    IPv4Address("172.16.1.22"): "LTU2.2",
    IPv4Address("172.16.1.32"): "LTU3.2",
}
# All parameters sizes are in bytes
# MAC header
MAC_SZ = 14

# IP header
IPv4_SZ = 20

# Source IP address
IP_SA = 4

# Destination IP address
IP_DA = 4

# UDP header
UDP_SZ = 8

# Sequence ID
PNin = 4

# To find out where source IP address is started, calculate its start position
IP_OFF = MAC_SZ + IPv4_SZ - IP_SA - IP_DA

# To find out where DATA is started, calculate its start position
DATA_OFF = MAC_SZ + IPv4_SZ + UDP_SZ + PNin

# Telemetry fields offsets
CUTIME_OFF = DATA_OFF + 44

BRD_LT1_OFF = DATA_OFF + 72
BRD_LT2_OFF = DATA_OFF + 74
BRD_LT3_OFF = DATA_OFF + 76
BRD_LT4_OFF = DATA_OFF + 78

CHG_VTCUR1_OFF = DATA_OFF + 80
CHG_VSCUR_OFF = DATA_OFF + 84
CHG_VSDIV_OFF = DATA_OFF + 86
CHG_VTDIV1_OFF = DATA_OFF + 88

LDD_HV1_OFF = DATA_OFF + 116
LDD_LDOUT1_OFF = DATA_OFF + 120

LDD_LT1_OFF = DATA_OFF + 126
LDD_LT2_OFF = DATA_OFF + 128
LDD_LT3_OFF = DATA_OFF + 130

LDD_RT1_OFF = DATA_OFF + 132
LDD_RT2_OFF = DATA_OFF + 136
LDD_RT3_OFF = DATA_OFF + 140

PLS_HVR1_OFF = DATA_OFF + 144
PLS_LDR1_OFF = DATA_OFF + 146
PLS_LDR2_OFF = DATA_OFF + 148
PLS_HVR2_OFF = DATA_OFF + 150
PLS_I1_OFF = DATA_OFF + 152
PLS_LD1_OFF = DATA_OFF + 154
PLS_LD2_OFF = DATA_OFF + 156
PLS_I2_OFF = DATA_OFF + 158
PLS_I3_OFF = DATA_OFF + 160
PLS_LD3_OFF = DATA_OFF + 162
PLS_LD4_OFF = DATA_OFF + 164
PLS_I4_OFF = DATA_OFF + 166
PLS_HVF1_OFF = DATA_OFF + 168
PLS_LDF1_OFF = DATA_OFF + 170
PLS_LDF2_OFF = DATA_OFF + 172
PLS_HVF2_OFF = DATA_OFF + 174

# Parameters sizes
CUTIME_W = 8

#Data width
DW = 2

# Adjustments to temperature sensors values
RT1_Adds = {
    "LTU1.1": 1.6,
    "LTU2.1": 2.6,
    "LTU3.1": -1.5,
}

RT2_Adds = {
    "LTU1.1": 1.5,
    "LTU2.1": 2.4,
    "LTU3.1": -2.2,
}

RT3_Adds = {
    "LTU1.1": 1.5,
    "LTU2.1": 2.4,
    "LTU3.1": -3.2,
}

# To use sqlite3 module create an object that represents the database.
# The data will be stored in the ltu-tel-temp.sqlite file
conn = sqlite3.connect("ltu-tel2.sqlite")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS temps_ltu11")

# Create table
cur.execute('''CREATE TABLE temps_ltu11(
        id integer PRIMARY KEY,
        /* cutime is timestamp, \
        since there is no timestamp datatype in sqlite,\
        define as real datatype. Then will be used datetime() function */
        cutime real,
        brd_lt1 real, brd_lt2 real, brd_lt3 real, brd_lt4 real, 
        ldd_lt1 real, ldd_lt2 real, ldd_lt3 real, 
        ldd_rt1 real, ldd_rt2 real, ldd_rt3 real)
        ''')

cur.execute("DROP TABLE IF EXISTS vltcur_ltu11")

cur.execute('''CREATE TABLE vltcur_ltu11(
        id integer PRIMARY KEY,
        /* cutime is timestamp, \
        since there is no timestamp datatype in sqlite,\
        define as real datatype. Then will be used datetime() function */
        cutime real, chg_vtcur1 real,chg_vtdiv1 real, chg_vscur real,
        chg_vsdiv real, ldd_hv1 real, ldd_ldout1 real)
        ''')

cur.execute("DROP TABLE IF EXISTS pls_ltu11")

cur.execute('''CREATE TABLE pls_ltu11(
        id integer PRIMARY KEY, cutime real,
        pls_hvr1 real, pls_ldr1 real, pls_ldr2 real, pls_hvr2 real,  
        pls_i1 real, pls_ld1 real, pls_ld2 real, pls_i2 real, pls_i3 real, 
        pls_ld3 real, pls_ld4 real, pls_i4 real, pls_hvf1 real, 
        pls_ldf1 real, pls_ldf2 real, pls_hvf2 real)
        ''')
class Packet:
    def __init__(self, bytes):
        self.bytes = 

    def get_bytes(self):
        x_cutime = packet[CUTIME_OFF : CUTIME_OFF + CUTIME_W]
        x_brd_lt1 = packet[BRD_LT1_OFF : BRD_LT1_OFF + DW]
        x_brd_lt2 = packet[BRD_LT2_OFF : BRD_LT2_OFF + DW]
        x_brd_lt3 = packet[BRD_LT3_OFF : BRD_LT3_OFF + DW]
        x_brd_lt4 = packet[BRD_LT4_OFF : BRD_LT4_OFF + DW]

        x_ldd_lt1 = packet[LDD_LT1_OFF : LDD_LT1_OFF + DW]
        x_ldd_lt2 = packet[LDD_LT2_OFF : LDD_LT2_OFF + DW]
        x_ldd_lt3 = packet[LDD_LT3_OFF : LDD_LT3_OFF + DW]

        x_rt1 = packet[LDD_RT1_OFF : LDD_RT1_OFF + DW]
        x_rt2 = packet[LDD_RT2_OFF : LDD_RT2_OFF + DW]
        x_rt3 = packet[LDD_RT3_OFF : LDD_RT3_OFF + DW]

        x_chg_vtcur1 = packet[CHG_VTCUR1_OFF : CHG_VTCUR1_OFF + DW]
        x_chg_vtdiv1 = packet[CHG_VTDIV1_OFF : CHG_VTDIV1_OFF + DW]
        x_chg_vscur = packet[CHG_VSCUR_OFF : CHG_VSCUR_OFF + DW]
        x_chg_vsdiv = packet[CHG_VSDIV_OFF : CHG_VSDIV_OFF + DW]

        x_ldd_hv1 = packet[LDD_HV1_OFF : LDD_HV1_OFF + DW]
        x_ldd_ldout1 = packet[LDD_LDOUT1_OFF : LDD_LDOUT1_OFF + DW]

        x_pls_hvr1 = packet[PLS_HVR1_OFF : PLS_HVR1_OFF + DW]
        x_pls_ldr1 = packet[PLS_LDR1_OFF : PLS_LDR1_OFF + DW]
        x_pls_ldr2 = packet[PLS_LDR2_OFF : PLS_LDR2_OFF + DW]
        x_pls_hvr2 = packet[PLS_HVR2_OFF : PLS_HVR2_OFF + DW]
        x_pls_i1 = packet[PLS_I1_OFF : PLS_I1_OFF + DW]
        x_pls_ld1 = packet[PLS_LD1_OFF : PLS_LD1_OFF + DW]
        x_pls_ld2 = packet[PLS_LD2_OFF : PLS_LD2_OFF + DW]
        x_pls_i2 = packet[PLS_I2_OFF : PLS_I2_OFF + DW]
        x_pls_i3 = packet[PLS_I3_OFF : PLS_I3_OFF + DW]
        x_pls_ld3 = packet[PLS_LD3_OFF : PLS_LD3_OFF + DW]
        x_pls_ld4 = packet[PLS_LD4_OFF : PLS_LD4_OFF + DW]
        x_pls_i4 = packet[PLS_I4_OFF : PLS_I4_OFF + DW]
        x_pls_hvf1 = packet[PLS_HVF1_OFF : PLS_HVF1_OFF + DW]
        x_pls_ldf1 = packet[PLS_LDF1_OFF : PLS_LDF1_OFF + DW]
        x_pls_ldf2 = packet[PLS_LDF2_OFF : PLS_LDF2_OFF + DW]
        x_pls_hvf2 = packet[PLS_HVF2_OFF : PLS_HVF2_OFF + DW]

        def convert_bytes(self):
            # Create an int from bytes. Default is unsigned.
            i_cutime =  int.from_bytes(x_cutime, byteorder="little")

            i_brd_lt1 = int.from_bytes(x_brd_lt1, byteorder="little")
            i_brd_lt2 = int.from_bytes(x_brd_lt2, byteorder="little")
            i_brd_lt3 = int.from_bytes(x_brd_lt3, byteorder="little")
            i_brd_lt4 = int.from_bytes(x_brd_lt4, byteorder="little")

            i_ldd_lt1 = int.from_bytes(x_ldd_lt1, byteorder="little")
            i_ldd_lt2 = int.from_bytes(x_ldd_lt2, byteorder="little")
            i_ldd_lt3 = int.from_bytes(x_ldd_lt3, byteorder="little")

            i_rt1 = int.from_bytes(x_rt1, byteorder="little")
            i_rt2 = int.from_bytes(x_rt2, byteorder="little")
            i_rt3 = int.from_bytes(x_rt3, byteorder="little")

            i_chg_vtcur1 = int.from_bytes(x_chg_vtcur1, byteorder="little")
            i_chg_vtdiv1 = int.from_bytes(x_chg_vtdiv1, byteorder="little")
            i_chg_vscur = int.from_bytes(x_chg_vscur, byteorder="little")
            i_chg_vsdiv = int.from_bytes(x_chg_vsdiv, byteorder="little")

            i_ldd_hv1  = int.from_bytes(x_ldd_hv1, byteorder="little")
            i_ldd_ldout1  = int.from_bytes(x_ldd_ldout1, byteorder="little")

            i_pls_hvr1  = int.from_bytes(x_pls_hvr1, byteorder="little")
            i_pls_ldr1  = int.from_bytes(x_pls_ldr1, byteorder="little")
            i_pls_ldr2  = int.from_bytes(x_pls_ldr2, byteorder="little")
            i_pls_hvr2  = int.from_bytes(x_pls_hvr2, byteorder="little")
            i_pls_i1  = int.from_bytes(x_pls_i1, byteorder="little")
            i_pls_ld1  = int.from_bytes(x_pls_ld1, byteorder="little")
            i_pls_ld2  = int.from_bytes(x_pls_ld2, byteorder="little")
            i_pls_i2  = int.from_bytes(x_pls_i2, byteorder="little")
            i_pls_i3  = int.from_bytes(x_pls_i3, byteorder="little")
            i_pls_ld3  = int.from_bytes(x_pls_ld3, byteorder="little")
            i_pls_ld4  = int.from_bytes(x_pls_ld4, byteorder="little")
            i_pls_i4  = int.from_bytes(x_pls_i4, byteorder="little")
            i_pls_hvf1  = int.from_bytes(x_pls_hvf1, byteorder="little")
            i_pls_ldf1  = int.from_bytes(x_pls_ldf1, byteorder="little")
            i_pls_ldf2  = int.from_bytes(x_pls_ldf2, byteorder="little")
            i_pls_hvf2  = int.from_bytes(x_pls_hvf2, byteorder="little")

            # Receive CU timestamp and convert it to UNIX time 
            cutime_timestamp = 8e-9 * int.from_bytes(x_cutime, byteorder="little") + scs_epoch


with open(filename, "rb") as binary_file:
    # Read binary file by packets, sized 1092 bytes

    while packet := binary_file.read(1092):
        # Calculate number of packets
        count += 1
        print(count)
        # Look for the source LTU IP address sized 4 bytes
        saddr = packet[IP_OFF : IP_OFF + 4]
        saddr_ip = IPv4Address(saddr)

        if saddr_ip in LTU_ips:
            # The channel is defined by dictionary key
            ch = LTU_ips[saddr_ip]

            

            

            
            if i_rt1 != 0 or i_rt2 != 0 or i_rt3 != 0:

                # Calculate LTU temperatures

                brd_lt1 = 0.488 * i_brd_lt1 - 273
                brd_lt2 = 0.488 * i_brd_lt2 - 273
                brd_lt3 = 0.488 * i_brd_lt3 - 273
                brd_lt4 = 0.488 * i_brd_lt4 - 273
                brd_lt_sample = (brd_lt1, brd_lt2, brd_lt3, brd_lt4)

                chg_vtcur1 = 0.244e-3 * i_chg_vtcur1
                chg_vtdiv1 = 20.1e-3 * i_chg_vtdiv1
                chg_vscur = 0.244e-3 * i_chg_vscur
                chg_vsdiv = 5.37e-3 * i_chg_vsdiv
                chg_sample = (chg_vtcur1, chg_vtdiv1, chg_vscur, chg_vsdiv)
                
                ldd_hv1 = 108e-3 * i_ldd_hv1
                ldd_ldout1 = 108e-3 * i_ldd_ldout1
                ldd_sample = (ldd_hv1, ldd_ldout1) 

                ldd_lt1 = 0.0957 * i_ldd_lt1 - 273
                ldd_lt2 = 0.0957 * i_ldd_lt2 - 273
                ldd_lt3 = 0.0957 * i_ldd_lt3 - 273
                ldd_lt_sample = (ldd_lt1, ldd_lt2, ldd_lt3)

                ldd_rt1 = 0.0957 * i_rt1 - 273 + RT1_Adds[ch]
                ldd_rt2 = 0.0957 * i_rt2 - 273 + RT2_Adds[ch]
                ldd_rt3 = 0.0957 * i_rt3 - 273 + RT3_Adds[ch]
                ldd_rt_sample = (ldd_rt1, ldd_rt2, ldd_rt3)

                pls_hvr1 = 108e-3 * i_pls_hvr1
                pls_ldr1 = 108e-3 * i_pls_ldr1
                pls_ldr2 = 108e-3 * i_pls_ldr2
                pls_hvr2 = 108e-3 * i_pls_hvr2
                pls_i1 = 31.74e-3 * i_pls_i1
                pls_ld1 = 108e-3 * i_pls_ld1
                pls_ld2 = 108e-3 * i_pls_ld2
                pls_i2 = 31.74e-3 * i_pls_i2
                pls_i3 = 31.74e-3 * i_pls_i3
                pls_ld3 = 108e-3 * i_pls_ld3
                pls_ld4 = 108e-3 * i_pls_ld4
                pls_i4 = 31.74e-3 * i_pls_i4
                pls_hvf1 = 108e-3 * i_pls_hvf1
                pls_ldf1 = 108e-3 * i_pls_ldf1
                pls_ldf2 = 108e-3 * i_pls_ldf2
                pls_hvf2 = 108e-3 * i_pls_hvf2
                pls_sample = (pls_hvr1 + pls_ldr1 + pls_ldr2 + pls_hvr2 + \
                    pls_i1 + pls_ld1 + pls_ld2 + pls_i2 + pls_i3 + pls_ld3 + \
                    pls_ld4 + pls_i4 + pls_hvf1 + pls_ldf1 + pls_ldf2 + pls_hvf2)

for row in tlm["LTU1.1"]:
    cur.execute('''INSERT INTO telemetry_ltu11(
        brd_lt1, brd_lt2, brd_lt3, brd_lt4, 
        chg_vtcur1, chg_vtdiv1, chg_vscur, chg_vsdiv, 
        ldd_hv1, ldd_ldout1, ldd_lt1, ldd_lt2, ldd_lt3,
        ldd_rt1, ldd_rt2, ldd_rt3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

# Save (commit) the changes
conn.commit()

# Changes have been committed, so close the connection
conn.close()
