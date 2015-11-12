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
    print str(sequenceNum) + ": Sending " + str(sentMessage.__len__()) + " bytes of data"
    try:
        clientSock.sendto(sentMessage, (serverAddr, int(serverPort)))
    except:
        print "An error occured when transmitting packet"
    
    # Attempt to receive response from server
    try:
        recvMessage, recvAddress = clientSock.recvfrom(1024)
        
        recvTime = datetime.now()
        if prevRTT == None:
            prevRTT = recvTime - sentTime
        
        sampleRTT = recvTime - sentTime
        calcRTT = .875 * prevRTT.microseconds - .125 * sampleRTT.microseconds
        print str(calcRTT / 10)
        
    except timeout:
        print "Request timed out"
    
# Print conclusion
print "Sent 10 messages"
