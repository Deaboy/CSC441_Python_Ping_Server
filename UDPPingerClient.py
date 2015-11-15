from __future__ import division
import sys
from datetime import *
from socket import *
import random

# Separate out the command line arguments
if sys.argv.__len__() != 3:
    print "Usage:"
    print "  " + sys.argv[0] + " <host> <port>"
    exit()
serverAddr = sys.argv[1]
serverPort = sys.argv[2]

# Create and set up UDP socket
clientSock = socket(AF_INET, SOCK_DGRAM)
clientSock.bind(('',0))
clientSock.settimeout(1.0)

# Initialize stat tracking variables
prevRTT = None
minRTT = None
maxRTT = None
sumRTT = 0
sumSent = 0
sumRecv = 0

# Print confirmation message once we've finally bound to a port
print 'Bound to port ' + str(clientSock.getsockname()[1])
print 'Sending 10 messages to ' + serverAddr + ':' + serverPort

# Send 10 sequential ping messages
for sequenceNum in range(1,11):
    
    # Build ping message
    sentTime = datetime.now()
    sentMessage = "Ping " + str(sequenceNum) + " " + sentTime.time().isoformat()
    
    # Send ping to server
    try:
        clientSock.sendto(sentMessage, (serverAddr, int(serverPort)))
        sumSent = sumSent + 1
    except:
        print "An error occured when transmitting packet"
        continue
    
    # Attempt to receive response from server
    try:
        recvMessage, recvAddress = clientSock.recvfrom(1024)
        recvTime = datetime.now()
        
        # Calculate RTT and receive time
        sampleRTT = recvTime - sentTime
        if prevRTT == None:
            prevRTT = sampleRTT.microseconds
        
        calcRTT = .875 * prevRTT + .125 * sampleRTT.microseconds
        prevRTT = calcRTT
        
        # Stats tracking
        if minRTT == None or sampleRTT.microseconds < minRTT:
            minRTT = sampleRTT.microseconds
        if maxRTT == None or sampleRTT.microseconds > maxRTT:
            maxRTT = sampleRTT.microseconds
        sumRTT += sampleRTT.microseconds
        sumRecv = sumRecv + 1
        
        # Print receipt message to console
        print str(recvMessage.__len__()) + " bytes received from " + recvAddress[0] + ": time=" + str(sampleRTT.microseconds / 10.0) + "ms RTT=" + str(calcRTT / 10.0) + "ms"
        print "    " + recvMessage
        
    except timeout:
        print "Request timed out"

# Print conclusion
print ""
print "--- " + serverAddr + " ping statistics ---"
print str(sumSent) + " packets transmitted, " + str(sumRecv) + " packets received, " + str((1.0 - (sumRecv / (1 if sumSent == 0 else sumSent))) * 100) + "% packet loss"
if sumRecv != 0:
    print "round-trip min/avg/max = " + str(minRTT / 10.0) + "/" + str(sumRTT / (1 if sumRecv == 0 else sumRecv) / 10.0) + "/" + str(maxRTT / 10) + " ms"

