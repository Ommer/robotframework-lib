"""
Description: it will updatetestopica test cases base on robotframework
status.
Author: Ommer Simjee
File Name: 

"""

import re
import sys
import os, time

class File(object):

    def edit_config_file(self, name, value,fileName='temp.txt'):
        """Edit Config File specified by item name and item value'.

        `Edit config file' directory is in the temp directory where the
        file will modify.

        `name` is the name of the file item that needs to be set. This
         corresponds to the key in the config file. Thus, `name` is
         case-sensitive.


        `Config file name don't need to be specified, if the name is
        'temp.txt'

         Examples-1:
         | *Keyword*       | *Argument 1*     |*Argument 2* |*Argument 3*
         |Edit File |  SystemInfo  | DUT         |
         |Edit File |  SystemInfo  | DUT         |file.txt

        """
        #
        #Change directory to temp
        #
        try:
            os.chdir('../temp/')
        except Execption:
            raise AssertionError("No directory found")
            return
        #
        #Read from the file
        #
        try:
            fr=open(fileName,'r')
            items=fr.read()
            fr.close()
        except  IOError:
              raise AssertionError("No File Exist")

        #
        #Search the "item name = value"
        #
        fw=open(fileName,'w')
        regex = re.compile("(?P<name>.*) = (?P<value>.*)\r\n")
        find_cfg = regex.findall(items)
        #
        #Replace "item name = vlaue" with new "item name = value"
        #
        for name_cfg,value_cfg in find_cfg:
            if name_cfg==name:
                name_cfg=re.escape(name_cfg)
                fw.write(re.sub(name_cfg+' = '+value_cfg,name+' = '+value,items))
        fw.close()

    def config_file_should_be(self, name, value, fileName='temp.txt'):
        """This verifies that the file item is written to a certain value.

        `name` is the name of the item that needs to be set. This
         corresponds to the key in the config file. Thus, `name` is
         case-sensitive.

        `value` is a string that is verified for the config file item.

        `Config file name don't need to be specified, if the name is
        'file.txt'

         Examples:
         | *Keyword*              | *Argument 1*     | *Argument 2* |*Argument 3*|
         | File Should Be  | SystemInfo  |  DUT         |            |
         | File Should Be  | SystemInfo   |  DUT         |file.txt   |

        """
        #
        #Change directory to temp
        #
        try:
            os.chdir('../temp/')
        except Execption:
            raise AssertionError("No directory found")
            return
        #
        #Read from the file
        #
        try:
            fr=open(fileName,'r')
            items=fr.read()
            fr.close()
        except  IOError:
              raise AssertionError("No File Exist")
        #
        #Search the "Item name = value"
        #
        name=re.escape(name)
        find_value=re.search(name+' = '+value,items)
        if find_value is not None:
                self._info("Match item: '%s'"% find_value.group())
        else:
            raise AssertionError("Value did not match in '%s'"%name)

