# ChrisMiuchiz
# Requires Python 3.6+
# This tool converts AW 6 telegram files into more usable formats
from struct import *
from Telegram import *
import sys
  
def MakeTelegrams(datfile, idxfile):
    with open(idxfile, 'rb') as f:
        idx = f.read()
    with open(datfile, 'rb') as f:
        dat = f.read()

    IDXLength, _, IDXEnd = unpack('<III', idx[:12])
    IDXStart, = unpack('<I', idx[0x48:0x48+4])

    telegrams = []
    blockStart = IDXStart
    while True:
        #AW's dat and idx formats are like linked lists of arrays of whatever struct they're storing.
        forward, backward, entrycount, entrieslength = unpack('<IIHH', idx[blockStart:blockStart+12])
        if entrycount == 0 or entrieslength == 0:
            break
        ENTRY_LENGTH = entrieslength // entrycount

        for i in range(entrycount):
            entryStart = blockStart + ENTRY_LENGTH * i
            
            datAddress, sentTimestamp, localID = unpack('<III', idx[entryStart+18: entryStart + 30])
            
            usernamestart = entryStart + 0x1E
            username = idx[usernamestart : usernamestart+32]

            #Stop message at first NULL NULL
            for j in range(0, len(username), 2):
                if username[j:j+2] == b'\x00\x00':
                    username = username[:j]
                    break
            username = username.decode('UTF-16')
            
            datEntryLength, = unpack('<I', dat[datAddress+2 : datAddress+6])
            
            tgtype = dat[datAddress + 0xA]

            messageStart = datAddress + 0xB
            message = dat[messageStart : datAddress+datEntryLength]

            #Stop message at first NULL NULL
            for j in range(0, len(message), 2):
                if message[j:j+2] == b'\x00\x00':
                    message = message[:j]
                    break
            message = message.decode('UTF-16')
            
            telegrams.append(Telegram(username, localID, message, sentTimestamp, tgtype))
            
        if forward == 0x00000000:
            break
        blockStart = forward

        
    return telegrams

def AskForArgs():
    dat = input('telegram5.dat file: ').strip('"')
    idx = input('telegram5.idx file: ').strip('"')
    otype = input('Output type (text | csv): ').strip('"')
    output = input('Output file: ').strip('"')
    return (dat, idx, otype, output)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dat, idx, otype, output = AskForArgs()
    elif len(sys.argv) == 5:
        dat, idx, otype, output = sys.argv[1:]
    else:
        print('USAGE: TGConverter.py <telegram5.dat> <telegram5.idx> <text | csv> <output file>')
        exit()
     
    if otype.lower() == 'text':
        func = OutputText
    elif otype.lower() == 'csv':
        func = OutputCSV
    else:
        print(f'Unknown type: {otype}')
        exit()

    telegrams = MakeTelegrams(dat, idx)
        
    with open(output, 'wb') as f:
        f.write(func(telegrams).encode('UTF-16'))
    
    
    
