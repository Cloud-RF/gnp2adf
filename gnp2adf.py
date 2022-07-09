import csv
import sys
import datetime

# Convert proprietary Google Network Planner Antenna files to an open NSMA / TIA-804-b standard

metadata = {}

# polar plots
az = []
el = []
headers = []

with open(sys.argv[1], 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar="'")
    r = 1
    metaheader = 0
    metaline = 0
    for row in reader:
        #print(r,row)
        if "SpecMetadata" in row[0]:
            metaheader = r+1
            metaline = r+2
        if r == metaheader:
            headers = row
        if r == metaline:
            i = 0
            for h in headers:
                metadata[h] = row[i]
                i+=1
        # Pattern data
        if r > 7:
            az.append(round(float(row[1]),3))
            el.append(round(float(row[2]),3))
        r+=1
    print(metadata)
    print(az)
    print(el)

with open(sys.argv[1]+".adf", 'w', newline='') as adf:
    x = datetime.datetime.now()
    adf.write("REVNUM:,TIA/EIA‐804‐B\r\n")
    adf.write("COMNT1:,Standard TIA/EIA Antenna Pattern Data\r\n")
    adf.write("ANTMAN:,%s\r\n" % metadata["Manufacturer"])
    adf.write("MODNUM:,%s\r\n" % metadata["Model Name"])
    adf.write("DESCR1:,%s\r\n" % metadata["Description"])
    adf.write("DESCR2:,Converted to a standard at CloudRF.com\r\n")
    adf.write("DTDATA:,%s\r\n" % x.strftime("%Y%m%d"))
    adf.write("LOWFRQ:,%s\r\n" % metadata["Frequency Start (MHz)"])
    adf.write("HGHFRQ:,%s\r\n" % metadata["Frequency End (MHz)"])
    adf.write("GUNITS:,DBI/DBR\r\n")
    adf.write("MDGAIN:,%s\r\n" % metadata["Nominal Gain (dBi)"])
    adf.write("AZWIDT:,%s\r\n" % metadata["Beamwidth (Degrees)"])
    adf.write("ELWIDT:,%s\r\n" % metadata["Beamwidth (Degrees)"])
    adf.write("FRTOBA:,10\r\n")
    adf.write("ELTILT:,%s\r\n" % metadata["Electrical Downtilt (Degrees)"])
    adf.write("MAXPOW:,0\r\n")
    adf.write("PATTYP:,Typical\r\n")
    adf.write("NOFREQ:,1\r\n")
    adf.write("PATFRE:,%s\r\n" % metadata["Acquisition Frequency (MHz)"])
    adf.write("NUMCUT:,2\r\n")
    adf.write("PATCUT:,H\r\n")
    adf.write("POLARI:,V/V\r\n")
    adf.write("NUPOIN:,360\r\n")
    adf.write("FSTLST:,‐179,180\r\n")

    deg = -179
    for a in az:
        adf.write("%d,%.03f\r\n" % (deg,a))
        deg+=1

    adf.write("PATCUT:,V\r\n")
    adf.write("POLARI:,V/V\r\n")
    adf.write("NUPOIN:,360\r\n")
    adf.write("FSTLST:,‐179,180\r\n")

    deg = -179
    for e in el:
        adf.write("%d,%.03f\r\n" % (deg,e))
        deg+=1
    adf.write("ENDFIL:,EOF\r\n")