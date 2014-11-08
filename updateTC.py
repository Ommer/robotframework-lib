"""
Description: it will updatetestopica test cases base on robotframework
status.
Author: Ommer Simjee
File Name:updateTc.py

"""




import sys
import os
import time
from testopia import Testopia
from robot.running import *
from robot.utils import *

class TestCase:

    def _connect_testopia(self):
        """A hook used to connect to the bugzilla. This will connect to
        testopia test cases."""


        try:
            tp = Testopia("tester@google.com","password",'http://bugzilla/xmlrpc.cgi')
            return tp
        except:
            raise RuntimeError("Could not establish Testopia connection.")

    def testopia_update(self):

        """
        This will update each test case.
        Test case must create in testopia before update.
        otherwise reture case ID incorrect
        """
        if self.update_testopia.lower()!='yes':
            print ("No Update in Testopia") 
            return
        
        
        suite_id  = self.suite_id
        tp        = self._connect_testopia()
        tester_id = 8 #user name sit id
        status    = self._get_case_status()
        case_id   = self._get_testopia_case_id()
        env_id    = self._get_testopia_env_id()
        build_id  = self._get_testopia_build_id(env_id)


        try:
            tp.testcaserun_update(int(suite_id),int(case_id),int(build_id),int(env_id),int(build_id),int(env_id),int(status),False,int(tester_id))
            self._info("case id %s in Suite %s" % (case_id,suite_id))
        except:
            self._info("Test case ID incorrect")
            pass

    def _get_test_status_in_teardown(self):

        """ Check Robotframework teardown status"""
        test = self._namespace.test

        if test and test.status !='RUNNING':
            return test
        else:
            raise RuntimeError("Keyword 'test status' can only be used in test teardown")

    def _get_case_status(self):

        """ Get Robotframework test case status """ 
        test = self._get_test_status_in_teardown()

        if test.passed:
            status = 2
        else:
            status = 3
        return status

    def _get_testopia_env_id(self):

        """ Get testopia env id"""
        tp= self._connect_testopia()

        try:
            run_suite=tp.testrun_get(int(self.suite_id))
            env_id= run_suite['environment_id']
            return env_id
        except:
            self._debug("No Environmet ID")

    def _get_testopia_build_id(self,env_id):

        """ Get testopia build id"""
        tp = self._connect_testopia()
        try:
            env =tp.environment_get(int(env_id))
            build=tp.build_check_by_name(str(self.build_name),int(env['product_id']))
            build_id =int(build['build_id'])
            return build_id
        except:
            self._debug("No Build Found")

    def _get_testopia_case_id(self):

        """Get Tesstopia Case id"""

        tp = self._connect_testopia()
        test = self._get_test_status_in_teardown()
        tname=test.name.split(':')
        run_cases= tp.testrun_list(run_id=self.suite_id)

        for case in run_cases:
            print "case",case
            print "tname",tname
            if str(case['summary']).strip() == str(tname[1]).strip():
                case_id = case['case_id']
                return case_id
        else:
            self._create_test_case()
        raise RuntimeError("No Test Case ID Found in Testopia Suite")

    def _create_test_case(self):

        """ Create Test case if testopia test case doesn't exist"""
        path = self._namespace.suite.source

        fn=open(self._namespace.suite.source)
        items=fn.read()

        regex = re.compile("Case.*\d{1,10}|\s.*:(?P<name>.*)(((?:\n|\r\n?).+)+)")

        find = regex.findall(items)
        tp = Testopia("test@google.com","password",'http://bugzilla/xmlrpc.cgi')

        plan_id = 1253
        author_id = 1
        isautomated = True
        category_id = 931
        #tp.testcase_create('testing',plan_id,author_id,isautomated,category_id,1)
        for i in range(0,len(find)):
            alias= str(sys.argv[1].split('.')[0]) + " plan:"+str(plan_id)+" case: "+str(i)
        try:
            create_case=tp.testcase_create(find[i][0],int(plan_id),int(8),False,int(931),int(2),alias,'None',1,1)
        except:
            print "error\n"
            create_case=tp.testcase_create(find[i][0].split('(')[0],int(plan_id),int(8),False,int(931),int(2),alias,'None',1,1)
        try:
            store_case=tp.testcase_store_text(create_case['case_id'],1,"automation","sit@canoga.com",find[i][1].replace('\n','<br>'), "Ensure it pass")
        except:
                pass

    @property
    def _execution_context(self):
        return EXECUTION_CONTEXTS.current

    @property
    def _namespace(self):
        return self._execution_context.namespace
