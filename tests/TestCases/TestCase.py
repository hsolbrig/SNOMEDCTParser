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
from pyparsing import ParseException

class TestCase():
    def __init__(self, reference, text):
        self.reference = reference
        self.text = text

def fmtException(e):
    return '\n %s \n %s^\n%s (%s)' % (e.line, ' '*e.loc, e.parserElement, e.msg)

def printProgressf(parser, string):
    try:
        print(parser(string).asXML('fail'))
    except ParseException:
        print("NO PROGRESS")


failOnError = True
printStringFirst = True
printProgress = False
printPassResult = True

def testIt(parser, string, fail=False):
    try:
        if printStringFirst: print('=' * 20 + '\n' + string)
        res = parser(string, parseAll=True)
        if printPassResult: print(res.asXML('pass'))
    except ParseException as e:
        if fail:
            return True
        print("***** %s " % string)
        print(fmtException(e))
        if printProgress: printProgressf(parser, string)
        return not failOnError
    except RuntimeError as e:
        print("***** %s" % string)
        print("     Stack Overflow")
        return False
    return not fail

