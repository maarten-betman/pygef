# -*- coding: utf-8 -*-
"""
Created on Wed May  8 07:14:59 2019

@author: mbet
"""
import json
import pandas as pd

class AGS:
    """
    Class to load AGS 4 file and return data as pandas dataframe
    
    Methods:
        __init__:
            input argmuments:
                agsFilePath: string location of the AGS file
    
        read_ags_group:
            Loop through file and collect different groups.
            Group discription is looked up from JSON file.
            This method must be run before the get_data() method can be called 

        get_data:
            input arguments:
                group  - abbreviation of group name to collect
                
                groupnames can be found under class variable groupList
            return:
                Pandas DataFrame with requested group data
    
    """
            
    def __init__(self, agsFilePath):
        
        self.agsFilePath = agsFilePath
        
        with open('./files/ags4.min.json') as f:
            self.data = json.load(f)
        
        
    def read_ags_group(self):
        """
        read AGS Groups.
        """
        n = 0
        self.groupList = []
        self.groups = {}
        
        with open(self.agsFilePath, 'rt') as agsFile:
            for line in agsFile:
                if '"GROUP",' in line[:8]:
                    groupName = line.split('"')[-2]
                    lineStart = n
                    inBlock = True
    #                 print(groupName, lineStart, inBlock)
    
                if len(line.strip()) == 0:
                    lineEnd = n
                    self.groups[groupName] = {'lineStart':lineStart, 'lineEnd':lineEnd}
    #                 print('End reached of block')
                    try:
                        group_description = self.data['groups'][groupName]['group_description']
                    except:
                        group_description = 'Unknown'
                    if inBlock:
                        self.groupList.append([groupName, lineStart, lineEnd, group_description])
                    inBlock = False
                n+=1
  
    def get_data(self, group):
        """
        Get requested group data
        """
        
        DATA = []
        start = self.groups[group]['lineStart']
        end = self.groups[group]['lineEnd']
        
        with open(self.agsFilePath, 'rt') as agsFile:    
            for i, line in enumerate(agsFile):
                if i == start + 1:
                    headers = line.replace('"','').replace('\n','').split(',')[1:]
                if i >= start + 4:
                    lineData = line.replace(', ',' ').replace('"','').replace('\n','').split(',')[1:]
                    DATA.append(lineData)
                if i == end - 1:
                    break

        df = pd.DataFrame(DATA, columns=headers)
        df = df.apply(pd.to_numeric, errors='ignore')
        df = df.dropna(axis=0, how='all')\
               .dropna(axis=1, how='all')
        
        return df