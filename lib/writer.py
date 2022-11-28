# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 21:09:25 2022

@author: Administrador
"""

import csv

class Writer:
    def __init__(self, filename):
    
        self.filename = open(filename, "w", newline="")
        self.filename.truncate()

        return csv.writer(self.filename, delimiter=";")         
         