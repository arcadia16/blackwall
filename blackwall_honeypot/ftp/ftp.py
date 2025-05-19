"""
Either leave it like this and add logging or write proxy for real ftp server in container
FTP code seems deprecated in Twisted, so no pylint for it.
Need to add logging somehow
"""
# pylint: skip-file

import logging
from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB
from twisted.internet import reactor

logger = logging.getLogger(__name__)
logging.basicConfig(filename='ftp.log', level=logging.INFO)
logger.info('Starting FTP server...')
# FilePasswordDB does not work, but whatever
p = Portal(FTPRealm('./'), [AllowAnonymousAccess(), FilePasswordDB("pass.dat")])

f = FTPFactory(p)
f.welcomeMessage = "MASU-CSPFMBA FTP"

reactor.listenTCP(21, f)
reactor.run()
