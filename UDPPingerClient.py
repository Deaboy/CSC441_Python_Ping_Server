import sys
from datetime import *
from socket import *
import random

# Separate out the command line arguments
serverAddr = sys.argv[1]
serverPort = sys.argv[2]

# Create and set up UDP socket
clientSock = socket(AF_INET, SOCK_DGRAM)
clientSock.bind(('',0))
clientSock.settimeout(1.0)

prevRTT = None

# Print confirmation message once we've finally bound to a port
print 'Bound to port ' + str(clientSock.getsockname()[1])
print 'Sending 10 messages to ' + serverAddr + ':' + serverPort

# Send 10 sequential ping messages
for sequenceNum in range(1,10):
    
    # Build ping message
    sentTime = datetime.now()
    sentMessage = "Ping " + str(sequenceNum) + " " + sentTime.time().isoformat()
    
    # Send ping to server
    try:
        clientSock.sendto(sentMessage, (serverAddr, int(serverPort)))
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
        print str(recvMessage.__len__()) + " bytes received from " + recvAddress[0] + ": time=" + str(sampleRTT.microseconds / 10) + "ms RTT=" + str(calcRTT / 10) + "ms"
        
    except timeout:
        print "Request timed out"
    
# Print conclusion
print "Sent 10 messages"
