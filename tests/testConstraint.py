# -*- coding: utf-8 -*-
# Copyright (c) 2014, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
from parser.parser import constraint, refinedConstraintSet, simpleConstraintSet
from pyparsing import ParseException
from tests.TestCases.TestCase import fmtException

class testExpressionConstraint(unittest.TestCase):
    def test_constraint(self):
        try:
            print(simpleConstraintSet.parseString('''< 19829001 |disorder of lung|   ''', parseAll=True).asXML('simpleExpression'))
            self.assertRaises(ParseException, refinedConstraintSet.parseString, '< 19829001 |disorder of lung|', parseAll=True)
            print(refinedConstraintSet.parseString('''19829001 |disorder of lung| : 116676008 |associated morphology| = 79654002 |edema|
    ''',parseAll=True).asXML('complexExpression'))
            print(constraint.parseString('''< 19829001 |disorder of lung| : 116676008 |associated morphology| = 79654002 |edema|
    ''',parseAll=True).asXML('expression'))
            print(constraint.parseString('''< 19829001 |disorder of lung|   ''', parseAll=True).asXML('simpleExpression'))
            print(constraint.parseString('''< 19829001 |disorder of lung|:
    116676008 |associated morphology| = 79654002 |edema|''', parseAll=True).asXML('expression'))
            print(constraint.parseString('''<< 404684003 |clinical finding|:
     { 363698007 |finding site| = 39057004 }''', parseAll=True).asXML('expression'))
            print(constraint.parseString('''<< 404684003 |clinical finding|:
     { 363698007 |finding site| = 39057004 |pulmonary valve structure|}''', parseAll=True).asXML('expression'))
            print(constraint.parseString('''(< 19829001 |disorder of lung| OR 79654002 |edema|)''', parseAll=True).asXML('expression'))
        except ParseException as e:
            print(fmtException(e))
            self.assertTrue(False)
        except RuntimeError as e:
            print("Recursion Failure")

        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main()
