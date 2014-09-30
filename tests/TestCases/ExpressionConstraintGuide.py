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

from tests.TestCases.TestCase import TestCase

testCases = [
    TestCase('6.2.1 Self', '404684003 |clinical finding|'),
    TestCase('6.2.2 Descendants of (brief)', '< 404684003 |clinical finding|'),
    TestCase('6.2.2 Descendants of (full)', 'descendantsOf 404684003 |clinical finding|'),
    TestCase('6.2.3 Descendants or self of (brief)','<< 404684003 |clinical finding|'),
    TestCase('6.2.3 Descendants or self of (full)', 'descendantsOrSelfOf 404684003 |clinical finding|'),
    TestCase('6.2.4 Ancestors of (brief)', '> 40541001 |acute pulmonary oedema|'),
    TestCase('6.2.4 Ancestors of (full)', 'ancestorsOf 40541001 |acute pulmonary oedema|'),
    TestCase('6.2.5 Ancestors or self of (brief)', '>> 40541001 |acute pulmonary oedema|'),
    TestCase('6.2.5 Ancestors or self of (full)', 'ancestorsOrSelfOf 40541001 |acute pulmonary oedema|'),
    TestCase('6.2.6 Members of (brief)', '^ 700043003 |example problem list subset|'),
    TestCase('6.2.6 Members of (full)', 'membersOf 700043003| example problem list subset |'),
    TestCase('6.2.6 Members of multi (brief)', '^^ 1111000000132 |medication reference sets reference set|'),
    TestCase('6.2.6 Members of multi (brief)', 'membersOf membersOf 1111000000132 |medication reference sets reference set|'),
    TestCase('6.3.1 Attributes (brief)', '''< 19829001 |disorder of lung|:
116676008 |associated morphology| = 79654002 |edema|'''),
    TestCase('6.3.1 Attributes (full)', '''descendantsOf 19829001 |disorder of lung| :
116676008 |associated morphology| = 79654002 |edema|'''),
    TestCase('6.3.1 Attributes alt (brief)', '''< 19829001 |disorder of lung|:
116676008 |associated morphology| = << 79654002 |edema|'''),
    TestCase('6.3.1 Attributes alt (full)', '''descendantsOf 19829001 |disorder of lung| :
116676008 |associated morphology| = descendantsOrSelfOf 79654002 |edema|'''),

    TestCase('6.3.2 Attribute sets', '''<< 404684003 |clinical finding|:
363698007 |finding site| = << 39057004 |pulmonary valve structure|,
116676008 |associated morphology| = << 415582006 |stenosis|'''),
    TestCase('6.3.3 Attribute groups (brief)', '''<< 404684003 |clinical finding|:
{ 363698007 |finding site| = << 39057004 |pulmonary valve structure|,
  116676008 |associated morphology| = << 415582006 |stenosis|}
{ 363698007 |finding site| = << 53085002 |right ventricular structure|,
  116676008 |associated morphology| = << 56246009 |hypertrophy|}'''),
    TestCase('6.3.3 Attribute groups (full)', '''descendantsOrSelfOf 404684003 |clinical finding|:
{ 363698007 |finding site| = descendantsOrSelfOf 39057004 |pulmonary valve structure|,
  116676008 |associated morphology| = descendantsOrSelfOf 415582006 |stenosis|}
{ 363698007 |finding site| = descendantsOrSelfOf 53085002 |right ventricular structure|,
  116676008 |associated morphology| = descendantsOrSelfOf 56246009 |hypertrophy|}'''),
    TestCase('6.3.4 Nested attributes (brief)', '''<< 404684003 |clinical finding|:
47429007 |associated with| = ( << 404684003 |clinical finding|:
116676008 |associated morphology| = << 55641003 |infarct| )'''),
    TestCase('6.3.4 Nested attributes (full)', '''descendantsOrSelfOf 404684003 |clinical finding|:
47429007 |associated with| = (descendantsOrSelfOf 404684003 |clinical finding|:
116676008 |associated morphology| = descendantsOrSelfOf 55641003 |infarct| )'''),
    TestCase('6.3.5 Attribute operators (brief)', ''' << 404684003 |clinical finding|:
47429007 |associated with| = ( << 404684003 |clinical finding|:
116676008 |associated morphology| = << 55641003 |infarct| )'''),
    TestCase('6.3.5 Attribute operators (full)', '''descendantsOrSelfOf 404684003 |clinical finding|:
descendantsOrSelfOf 47429007 |associated with| =
descendantsOrSelfOf 267038008 |oedema|'''),
    TestCase('6.3.6 Concrete values', '''< 111111 |amoxicillin tablet|:
{ 127489000 |has active ingredient| = 372687004 |amoxicillin|,
   222222 |has reference basis of strength| = 372687004 |amoxicillin|,
   333333 |strength magnitude equal to| >= #500,
   444444 |strength unit| = 258684004 |mg|}'''),
    TestCase('6.3.6 Concrete values 2', '''< XXX |amoxicillin tablet|:
{ 127489000 |has active ingredient| = 372687004 |amoxicillin|,
   XXX |has reference basis of strength | = 372687004 |amoxicillin|,
   XXX |strength magnitude equal to| >= #500,
   XXX |strength magnitude equal to| <= #800,
   XXX |strength unit| = 258684004 |mg|}'''),
    TestCase('6.3.6 Concrete values 3', '''<< 373873005 |pharmaceutical / biologic product|:
XXX |trade name| = "PANADOL"'''),
    TestCase('6.3.7 Reverse attributes (brief)', '''< 105590001 |substance|:
R 127489000 |has active ingredient| = XXX |TRIPHASIL tablet|'''),
    TestCase('6.3.7 Reverse attributes (full)', '''descendantsOf 105590001 |substance|:
reverseOf 127489000 |has active ingredient| = XXX |TRIPHASIL tablet|'''),
    TestCase('6.3.8 Cardinality 1','''< 373873005 |pharmaceutical / biologic product|:
[3..*] 127489000 |has active ingredient| = < 105590001 |substance|'''),
    TestCase('6.3.8 Cardinality 2', '''descendantsOf 373873005 |pharmaceutical / biologic product|:
[3 to many] 127489000 |has active ingredient| = descendantsOf 105590001 |substance|'''),
    TestCase('6.3.8 Cardinality 3', '''< 373873005 |pharmaceutical / biologic product|:
[1..1] 127489000 |has active ingredient| = < 105590001 |substance|'''),
    TestCase('6.3.8 Cardinality 4', '''< 373873005 |pharmaceutical / biologic product|:
[0..1] 127489000 |has active ingredient| = < 105590001 |substance|'''),
    TestCase('6.4.1 Simple expression conjunction and disjunction 1', '''< 19829001 |disorder of lung| AND < 301867009 |edema of trunk|'''),
    TestCase('6.4.1 Simple expression conjunction and disjunction 2', ''' < 19829001 |disorder of lung| and < 301867009 |edema of trunk|'''),
    TestCase('6.4.1 Simple expression conjunction and disjunction 3', '''< 19829001 |disorder of lung| And < 301867009 |edema of trunk| '''),
    TestCase('6.4.1 Simple expression conjunction and disjunction 4', ''' < 19829001 |disorder of lung| OR < 301867009 |edema of trunk|'''),
    TestCase('6.4.1 Simple expression conjunction and disjunction 5', '''< 19829001|disorder of lung| AND ^ 152725851000154106|cardiology reference set| '''),
    TestCase('6.4.2 Attribute conjunction and disjunction 1', '''<< 404684003 |clinical finding|:
363698007 |finding site| = << 39057004 |pulmonary valve structure| AND
116676008 |associated morphology| = << 415582006 |stenosis| '''),
    TestCase('6.4.2 Attribute conjunction and disjunction 2', ''' << 404684003 |clinical finding| :
116676008 |associated morphology| = << 55641003 |infarct| OR
42752001 |due to| = << 22298006 |myocardial infarction|'''),
    TestCase('6.4.3 Attribute group conjunction and disjunction', ''' << 404684003 |clinical finding|:
{ 363698007 |finding site| = << 39057004 |pulmonary valve structure|,
   116676008 |associated morphology| = << 415582006 |stenosis|} OR
{ 363698007 |finding site| = << 53085002 |right ventricular structure|,
   116676008 |associated morphology| = << 56246009 |hypertrophy|} '''),
    TestCase('6.4.4 Attribute value conjunction and disjunction 1', '''^ 1111000000132 |allergy event reference set|: 246075003 |causative agent| =
< 373873005 |pharmaceutical / biologic product| OR < 105590001 |substance| '''),
    TestCase('6.4.4 Attribute value conjunction and disjunction 2', ''' << 404684003 |clinical finding|: 116676008 |associated morphology| =
<< 56208002|ulcer| AND << 50960005|haemorrhage|'''),
    TestCase('6.4.5 Complex expression constraint conjunction and disjunction', '''(<< 404684003 |clinical finding|: 116676008 |associated morphology| = << 55641003 |infarct|)
OR
(<< 404684003 |clinical finding|: 42752001 |due to| = << 22298006 |myocardial infarction|) '''),
    TestCase('6.5.1 Negation of simple expressions 1', '''! < 301867009 |edema of trunk| '''),
    TestCase('6.5.1 Negation of simple expressions 2', '''< 19829001 |disorder of lung| AND ! < 301867009 |edema of trunk| '''),
    TestCase('6.5.1 Negation of simple expressions 3', ''' descendantsOf 19829001 |disorder of lung| AND NOT descendantsOf 301867009 |oedema of trunk|'''),
    TestCase('6.5.1 Negation of simple expressions 4', '''< 19829001 |disorder of lung| + ! ^ 152725851000154106 |cardiology reference set| '''),
    TestCase('6.5.2 Negation of attribute values 1', ''' << 404684003 |clinical finding|: 116676008 |associated morphology| =
<< 56208002 |ulcer| AND << 50960005 |haemorrhage| AND ! << 26036001 |obstruction|'''),
    TestCase('6.5.2 Negation of attribute values 2', '''<< 404684003 |clinical finding|:
116676008 |associated morphology| = ! << 26036001 |obstruction| '''),
    TestCase('6.5.2 Negation of attribute values 3', '''descendantsOrSelfOf 404684003 |clinical finding|:
116676008 |associated morphology| = NOT descendantsOrSelfOf 26036001 |obstruction| ''')
    ]