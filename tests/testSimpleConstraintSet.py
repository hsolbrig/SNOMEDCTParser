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
from parser.parser import simpleConstraintSet, conceptReference
from tests.TestCases.TestCase import testIt


class testSimpleConstraintSet(unittest.TestCase):
    def test_simple_expression_set(self):
        self.assertTrue(testIt(conceptReference.parseString,'404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'<404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'descendantsOf 404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'<<    404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'descendantsOrSelfOf 404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'> 404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'ancestorsOf 404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'>>    404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'ancestorsOrSelfOf 404684003 |clinical finding|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'^ 700043003 |example problem list subset|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'membersof 700043003 |example problem list subset|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'^^ 1111000000132 |medication reference sets reference set|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'membersof membersof 1111000000132 |medication reference sets reference set|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'not <<  membersof membersof 1111000000132 |medication reference sets reference set|'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'not 123456'))
        self.assertTrue(testIt(simpleConstraintSet.parseString,'123456 OR < 123466 AND 1239999 | foo | , 74400008 | bar |'))

    def test_simple_expression_set2(self):
        self.assertTrue(testIt(simpleConstraintSet.parseString,'123456 OR 123466'))
      
if __name__ == '__main__':
    unittest.main()
