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
from parser.parser import *


class testNumbers(unittest.TestCase):
    def test_integers(self):
        self.assertEqual(12345, unsignedInteger.parseString('12345', parseAll=True)[0])
        self.assertRaises(ParseException, unsignedInteger.parseString, '-1', parseAll=True)
        self.assertEqual(-7440000008, integerValue.parseString('-7440000008', parseAll=True)[0])
        self.assertRaises(ParseException, integerValue.parseString,'001', parseAll=True)
        self.assertRaises(ParseException, integerValue.parseString,'0.', parseAll=True)
        self.assertRaises(ParseException, integerValue.parseString,'-001', parseAll=True)
        self.assertEqual(0, integerValue.parseString('0', parseAll=True)[0])
        self.assertEqual(0, integerValue.parseString('-0', parseAll=True)[0])
        self.assertEqual(0, integerValue.parseString('+0', parseAll=True)[0])

        self.assertRaises(ParseException,unsignedInteger.parseString,'-12345', parseAll=True)
        self.assertRaises(ParseException,unsignedInteger.parseString,'-12345z', parseAll=True)

    def test_decimals(self):
        self.assertEqual(-17.2, decimalValue.parseString('-17.200', parseAll=True)[0])
        self.assertEqual(1722.34, decimalValue.parseString('+1722.34', parseAll=True)[0])
        self.assertEqual(0.0, decimalValue.parseString('0.0', parseAll=True)[0])
        self.assertEqual(0.0, decimalValue.parseString('-0.0', parseAll=True)[0])
        self.assertEqual(0.0, decimalValue.parseString('+0.0', parseAll=True)[0])
        self.assertEqual(0.001, decimalValue.parseString('  0.001 ', parseAll=True)[0])
        self.assertRaises(ParseException, decimalValue.parseString, '- 0.0', parseAll=True)
        self.assertRaises(ParseException, decimalValue.parseString, '-', parseAll=True)

    def test_numerics(self):
        res = numericValue.parseString('-17',parseAll=True)
        self.assertEqual(-17,res.integer)
        self.assertFalse(res.decimal)
        res = numericValue.parseString('0.00017', parseAll=True)
        self.assertEqual(0.00017, res.decimal)
        self.assertFalse(res.integer)
if __name__ == '__main__':
    unittest.main()
