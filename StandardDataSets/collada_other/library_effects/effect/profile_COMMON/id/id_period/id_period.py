
# Copyright (c) 2012 The Khronos Group Inc.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and /or associated documentation files (the "Materials "), to deal in the Materials without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Materials, and to permit persons to whom the Materials are furnished to do so, subject to
# the following conditions:
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Materials. 
# THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

# See Core.Logic.FJudgementContext for the information
# of the 'context' parameter.
# [WARNING] this structure is subject to changes.
#

# This sample judging object does the following:
#
# JudgeBaseline: just verifies that the standard steps did not crash.
# JudgeExemplary: also verifies that the validation steps are not in error.
# JudgeSuperior: same as intermediate badge.

# Status value:
# -1000 : Initail status: test does not start yet.
# 0 : Failed
# 1 : Successful

from Core.Common.DOMParser import *
from Core.Common.CheckingModule import *

from xml.dom.minidom import parse, parseString
import os

# Please feed your node list here:
tagLst = ['library_effects', 'effect', 'profile_COMMON']

class SimpleJudgingObject:
    def __init__(self, status_basic_, status_intermediate_, status_advanced_, tagLst_):
        self.status_basic = status_basic_
        self.status_intermediate = status_intermediate_
        self.status_advanced = status_advanced_
        self.tagLst = tagLst_
        self.inputFilleName = ''
        self.outputFilleNameLst = []        
    
    def AdditionExemplaryChk(self):
        testIO = DOMParserIO( self.inputFilleName, self.outputFilleNameLst )
        # load files and generate root
        testIO.Init()
        testPChecker = PresChecker(testIO.GetRoot(self.inputFilleName), testIO.GetRoot(self.outputFilleNameLst[0])  )
        
        # get input profile_COMMON list
        profile_COMMONInputLst = GetElementsByTags(testIO.GetRoot(self.inputFilleName), self.tagLst)
        profile_COMMONOutputLst = GetElementsByTags(testIO.GetRoot(self.outputFilleNameLst[0]), self.tagLst)
        
        if profile_COMMONInputLst != None and profile_COMMONOutputLst != None:

            resSetEle = testPChecker.ResetElements(profile_COMMONInputLst, profile_COMMONOutputLst)
                    
            # check whether there is id retrived correctly
            if resSetEle[0] == True:            
                resChkVale = testPChecker.checkAttri('id')
                if resChkVale[0] == True:
                    testIO.Delink()
                    return [True, 'Pass: id of profile_COMMON is preserved.']
                else:
                    testIO.Delink()
                    return [False, 'Failed: id of profile_COMMON is not preserved.']
            else:
                testIO.Delink()
                return [False, 'Failed: id of profile_COMMON is not found.']
        else:
            testIO.Delink()
            return [False, 'Failed: profile_COMMON is not found.']
    
    # This function is enough to test whether baked matrix is correct or not. through image comparison
    def JudgeBaseline(self, context):
        
        if len(self.tagLst) == 0:
            context.Log("Error: judging script doesn't have enough information about tag names.")
            return False
        
        # This is where you can test XML or force the comparison of image files
        # or any custom verification you want to do...
        if (context.HasStepCrashed()):
            context.Log("FAILED: Crashes during required steps.")
            return False
        else:
            context.Log("PASSED: No crashes.")

        # Check the required steps for positive results and that a rendering was done.
        if not context.HaveStepsPassed([ "Import", "Export", "Validate" ]):
            context.Log("FAILED: Import, export and validate steps must be present and successful.")
            self.status_basic = 0
            return False
        else:
            # Get the input file
            self.inputFilleName = context.GetAbsInputFilename(context.GetCurrentTestId())
            
            # Get the output file
            outputFilenames = context.GetStepOutputFilenames("Export")
            
            if len(outputFilenames) == 0:
                context.Log("FAILED: There are no export steps.")
                return False
            else:
                del self.outputFilleNameLst[:]
                self.outputFilleNameLst.extend( outputFilenames )
               
            context.Log("PASSED: Required steps executed and passed.")
        
            resAdditionExemplaryChk = self.AdditionExemplaryChk()
            
            if resAdditionExemplaryChk[0] == True:
                self.status_basic = 1
                return True
            else:
                self.status_basic = 0
                context.Log("FAILED: " + resAdditionExemplaryChk[1])
                return False
      
        self.status_basic = 0
        return False
  
    # To pass intermediate you need to pass basic, this object could also include additional 
    # tests that were specific to the intermediate badge.
    def JudgeExemplary(self, context):        
        context.Log("N/A")
        return False
    
    # To pass advanced you need to pass intermediate, this object could also include additional
    # tests that were specific to the advanced badge
    def JudgeSuperior(self, context):
        context.Log("N/A")
        return False

    # To pass FX you need to pass basic?
    # This object could also include additional
    # tests that were specific to the FX badges
    def JudgeFx(self, context):
        context.Log("N/A")
        return False

    # To pass advanced you need to pass intermediate, this object could also include additional
    # tests that were specific to the advanced badge
    def JudgePhysics(self, context):
        context.Log("N/A")
        return False

# This is where all the work occurs: "judgingObject" is an absolutely necessary token.
# The dynamic loader looks very specifically for a class instance named "judgingObject".
#
judgingObject = SimpleJudgingObject(-1000, -1000, -1000, tagLst);