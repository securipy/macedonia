#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

""" Macedonia Plugin """

import sys
import os
import smtplib
import time, datetime
from time import gmtime, strftime
import argparse
import jwt
import requests
#Delorean


__author__            = "XaviTorello"
__credits__            = "XaviTorello, GoldraK"
__version__            = "0.1"
__maintainer__        = "XaviTorello"
__email__            = "info@xaviertorello.cat"
__status__            = "Development"


class MacedoniaPlugin(object):
    """
    Macedonia Base Plugin object
    """

    __slots__ =  ('name', 'description', 'version', 'jwt', 'algorithm', 'log', 'verbose', 'args')

    def __init__(self, name, description, version, pub_key, priv_key, log=True, verbose=True, arguments=None):
        self.name = name
        self.description = description
        self.version = version

        self.algorithm = "HS256"

        self.jwt = self.__createJWT(priv_key, pub_key)

        self.log = log
        self.verbose = verbose

        parser = argparse.ArgumentParser(description=self.description)

        #Set arguments if exists
        """
        {
            "action",
            "help",
            "argument",
        }
        """
        if False and arguments:
            for option in arguments:
                parser.add_argument(option['argument'],action=option['action'],help=option['help'])
            self.args = parser.parse_args()

    def __createJWT(self, private_key, public_key):
        """
        Return an encoded JWT token
        """
        return jwt.encode({'public_key':public_key, 'module':self.name}, private_key, algorithm=self.algorithm)


    def sendEmail(self,alert_mac,opts):
        """
        This function send mail with the report
        """
        header  = 'From: %s\n' % opts.user
        header += 'To: %s\n' % opts.emailto
        if alert_mac:
            header += 'Subject: New machines connected\n\n'
            message = header + 'List macs: \n '+str(alert_mac)
        else:
            header += 'Subject: No intruders - All machines known \n\n'
            message = header + 'No intruders'

        server = smtplib.SMTP(opts.server+":"+opts.port)
        server.starttls()
        server.login(opts.user,opts.password)
        if self.verbose or self.log:
            debugemail = server.set_debuglevel(1)
            if self.verbose:
                self.consoleMessage(debugemail)
        problems = server.sendmail(opts.user, opts.emailto, message)
        print (problems)
        server.quit()


    def consoleMessage(self,message):
        """
        This function write console message
        """
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print ("[{}] {}".format(st, message))


    def writeLog(self,log):
        """
        This function write log
        """
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if os.path.isfile('log.txt'):
            try:
                file_read = open('log.txt', 'a')
                file_read.write('['+st+'] '+log+"\n")
                file_read.close()
            except IOError:
                msg = 'ERROR: Cannot open log.txt'
                if self.verbose:
                    self.consoleMessage(msg)
                sys.exit(-1)
        else:
            msg = "ERROR: The log file  doesn't exist!"
            if self.verbose:
                self.consoleMessage(msg)
            sys.exit(-1)

    def writeLogConsole(self,msg,error=False):
        if self.log or error:
            self.writeLog(msg)
        if self.verbose:
            self.consoleMessage(msg)
