#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 09:42:38 2017

@author: dieter
"""
import maestro
import gc
import ports

class BoardDevice:
    def __init__(self, ser_port=False, verbose=True):
        self.id = id(self)
        self.verbose = verbose
        self.device = None
        self.connect(ser_port=ser_port)

    def __del__(self):
        self.verbose = False
        self.disconnect()

    def test_connection(self):
        # This is a minimal test that should be overwritten by the inheriting classes
        return self.device.isInitialized

    def connect(self, ser_port=False, disconnect_all=True):
        if self.verbose: print('\n+ Start Connecting instance', self.id)
        if disconnect_all: self.disconnect_others()
        if not ser_port:
            self.auto_connect()
        else:
            self.manual_connect(ser_port=ser_port)
        success = self.test_connection()
        if success and self.verbose: print('+ Connecting succeeded')
        if not success and self.verbose: print('+ Connecting failed')
        return success

    def manual_connect(self, ser_port):
        self.device = maestro.Device(con_port=False, ser_port=ser_port)

    def auto_connect(self):
        port_list = ports.serial_ports()
        for port in port_list:
            if self.verbose: print('+ Trying port', port, end='')
            self.device = maestro.Device(con_port=False, ser_port=port)
            success = self.test_connection()
            if success: break
            if self.verbose: print('\t--> Rejected')
        if success and self.verbose: print('\t--> OK')

    def disconnect_others(self):
        signature = str(type(self))
        for other in gc.get_objects():
            if signature in str(type(other)):
                if other.id != self.id: other.disconnect()

    def disconnect(self):
        if self.verbose: print('+ Disconnecting Board instance ', self.id)
        try:
            self.device.__del__()
        except Exception as error:
            print(error)
