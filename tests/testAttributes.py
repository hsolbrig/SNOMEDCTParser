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
from parser.parser import attributeSet, attribute, attributeGroup, simpleAttributeGroup
from pyparsing import ParseException
from tests.TestCases.TestCase import fmtException, testIt

# attribute = [cardinality ws] [reverseFlag ws] [attributeOperator ws] attributeName ws
# 	("=" ws expressionConstraintValue / comparisonOperator ws concreteValue)

def nullDebugAction(*args):
    """'Do-nothing' debug action, to suppress debugging output during parsing."""
    pass

def successDebugAction( instring, startloc, endloc, expr, toks ):
    print ("Matched " +  " -> " + str(toks.asList()))


class testAttributeSet(unittest.TestCase):
    def test_attribute(self):
        self.assertTrue(testIt(attribute.parseString, '74400008 = 74400008'))
        self.assertTrue(testIt(attribute.parseString, '74400008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, '< 74400008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, '<< 74400008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, 'descendantsof 74400008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, 'descendantsorselfof 744000008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, 'reverseof descendantsorselfof 744000008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, 'reverseof 744000008 |appendicitis| = 74400008 |appendicitis| '))
        self.assertRaises(ParseException, attribute.parseString, '<< reverseof 744000008  = 74400008  ', parseAll=True)
        self.assertTrue(testIt(attribute.parseString, '[0..1]74400008 = 74400008'))
        self.assertTrue(testIt(attribute.parseString, '[0..*]74400008 = 74400008'))
        self.assertTrue(testIt(attribute.parseString, '[0..many]74400008 = 74400008'))
        self.assertTrue(testIt(attribute.parseString, '[1..1]74400008 = 74400008'))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = 74400008)'))

    def test_attributeExpression(self):
        self.assertTrue(testIt(attribute.parseString, '< 74400008 |appendicitis| = < 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, '< 74400008 |appendicitis| = >> 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, ' 74400008 |appendicitis| = << 74400008 |appendicitis| '))
        self.assertTrue(testIt(attribute.parseString, ' 744000008 |appendicitis| = > 74400008 |appendicitis| '))

    def test_attributeConcreteValue(self):
        self.assertTrue(testIt(attribute.parseString, '74400008 <= #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 = #0.000413'))
        self.assertTrue(testIt(attribute.parseString, '74400008 = #-0.001'))
        self.assertTrue(testIt(attribute.parseString, '74400008 < #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 >= #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 > #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 != #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 ! = #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 not= #17'))
        self.assertTrue(testIt(attribute.parseString, '74400008 not = #17'))
        self.assertRaises(ParseException, attribute.parseString,'74400008 not < #17', parseAll=True )

        self.assertTrue(testIt(attribute.parseString, '74400008 = "abc"'))
        self.assertTrue(testIt(attribute.parseString, '74400008 = "   ab  c  "'))
        # TODO: figure out embedded stuff later on
        # self.assertTrue(testIt(attribute.parseString, r'74400008 = "abc\\" \\\\ \\“"'))

    # attributeSet = attribute *(ws conjunction ws attribute) /
    #                 "(" ws attributeSet ws ")" /
    # 	             attributeSet ws (conjunction / disjunction) ws attributeSet
    def test_attributeSet(self):
        self.assertTrue(testIt(attributeSet.parseString, '74400008 <= #17'))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 <= #17)'))

    def testx(self):
        self.assertTrue(testIt(attributeSet.parseString, '74400008 = "abc"'))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")   or  (74400008 = "def1") '))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")   or  (74400008 = "def2") '))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")  or   (74400008 = "def3") '))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")  and   (74400008 = "def4") '))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")  and   74400008 = "def5" '))
        self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")  ,   74400008 = "def6" '))


    def test2(self):
        try:
            self.assertTrue(testIt(attributeSet.parseString, '363698007 |finding site| = << 39057004 |pulmonary valve structure|'))
            self.assertTrue(testIt(attributeSet.parseString, '116676008 |associated morphology| = << 415582006 |stenosis|'))
            # TODO: the item below does not parse, but I'm not sure it should...
            #  attributeSet = attribute *(conjunction attribute) -->
            #  attribute = attributeName "=" expressionConstraintValue 363698007 |finding site| =
            #  expressionConstraintValue = simpleExpressionConstraint
            #  simpleExpressionConstraint = conceptReference conjunction simpleEpressionConstraint :: |pulmonary valve structure|, 116676008 |associated morphology|
            self.assertTrue(testIt(attributeSet.parseString, '''363698007 |finding site| = << 39057004 |pulmonary valve structure|, 116676008 |associated morphology| = << 415582006 |stenosis|'''))
            self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")'))
            self.assertTrue(testIt(attributeSet.parseString, '(74400008 = "abc")    , 74400009 <= #2'))
            self.assertTrue(testIt(attributeSet.parseString, ' 74400008 = "abc"     , 74400009 <= #2'))
            self.assertTrue(testIt(attributeSet.parseString, ' 74400008 = "abc"     and 74400009 <= #2'))
            self.assertTrue(testIt(attributeSet.parseString, ' (74400008 = "abc")     or 74400009 <= #2'))
        except ParseException as e:
            print(fmtException(e))
            self.assertTrue(False)

# attributeGroup = "{" ws attributeSet ws "}" /
#                  “(“ ws attributeGroup ws “)” /
# 	               attributeGroup ws (conjunction / disjunction) ws attributeGroup
    def testAttributeGroup(self):
        self.assertTrue(testIt(simpleAttributeGroup.parseString, '{74400008 <= #17}'))
        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17}'))
        self.assertTrue(testIt(simpleAttributeGroup.parseString, '( {74400008 <= #17} )'))
        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17},{74400008 <= #17}'))
        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17}{74400008 <= #17}'))
        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17}{74400008 <= #17}{74400008 <= #17}'))
        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17} OR {74400008 <= #17}'))
        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17} AND {74400008 <= #17}'))

        self.assertTrue(testIt(attributeGroup.parseString, '{74400008 <= #17}({74400008 <= #17} AND {74400008 <= #17})', fail=True))






if __name__ == '__main__':
    unittest.main()
