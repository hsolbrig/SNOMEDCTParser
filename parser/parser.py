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
from pyparsing import *

# Numbers
digitNonZero = '123456789'
unsignedInteger = Word(digitNonZero, nums).setParseAction(lambda i : int(i[0]))
integerValue = Regex(r'[-+]?(0|([1-9][0-9]*))([^.]|$)').setParseAction(lambda i : int(i[0]))('integer')
decimalValue = Regex(r'[-+]?(0|([1-9][0-9]*)).\d+').setParseAction(lambda d : float(d[0]))('decimal')
numericValue = integerValue | decimalValue

# Concept Reference (Note bug: trailing spaces are part of term)
sctid = Word(digitNonZero, nums, min=6, max=18).setParseAction(lambda i: int(i[0]))('sctid')
nonPipe = printables.replace('|','') + alphas8bit
term = Suppress(Literal('|')) + Combine(CharsNotIn('|'))('term') + Suppress(Literal('|'))
conceptReference = Group(sctid + Optional(term))

# Operators
descendantsOf = (Literal('<') + ~FollowedBy(Literal('<')) | CaselessKeyword('descendantsof'))('descendantsOf')
desendantsOrSelfOf = (Literal('<<') | CaselessKeyword('descendantsorselfof'))('descendantsOrSelfOf')
ancestorsOf = ((Literal('>') + ~FollowedBy(Literal('>'))) | CaselessKeyword('ancestorsof'))('ancestorsOf')
ancestorsOrSelfOf = (Literal('>>') | CaselessKeyword('ancestorsorselfof'))('ancestorsOrSelfOf')
conjunction = ((CaselessKeyword('and') | ','))('and')
disjunction = (CaselessKeyword('or'))('or')
conjOrDisj = (conjunction | disjunction)

constraintOperator = descendantsOf | desendantsOrSelfOf | ancestorsOf | ancestorsOrSelfOf
many = Literal('*') | CaselessKeyword('many')

cardinality = Group('[' + unsignedInteger + '..' + (unsignedInteger | many) + ']')
reverseFlag = CaselessKeyword('reverseOf')
attributeOperator = descendantsOf | desendantsOrSelfOf
attributeName = conceptReference
notEqual = '!=' | (CaselessKeyword('not') + '=')

comparisonOperator = '=' | notEqual | '<=' | '<' | '>=' | '>'
# TODO: get all the escaped thingise in
stringValue = Word(alphanums)
concreteValue = Group(Literal('"') | Literal('“')) + stringValue + (Literal('"') | Literal('”')) |\
                Group(Literal('#') + numericValue)


expressionConstraint = Forward()
simpleExpressionConstraint = Forward()
complexExpressionConstraint = Forward()

# Refinements
expressionConstraintValue = simpleExpressionConstraint | ('(' + complexExpressionConstraint + ')')
attribute = (Optional(cardinality) + Optional(reverseFlag) + Optional(attributeOperator) + attributeName +
             ((Suppress('=') + expressionConstraintValue) | (comparisonOperator + concreteValue)))
attributeSet = Forward()
attributeSet << ((attribute + ZeroOrMore(conceptReference + attribute)) |
                 (Suppress('(') + attributeSet + Suppress(')')) |
                 (attributeSet + conjOrDisj + attributeSet))

attributeGroup = Forward()
attributeGroup << (('{' + attributeSet + '}') |
                  ("(" + attributeGroup + ')'))
attributeGroups = (attributeGroup + conjOrDisj + attributeGroup)


refinement = Group(attributeSet | attributeGroups) + ZeroOrMore(Optional(conjunction) + attributeGroup)


negationIndicator = Literal('!') | CaselessKeyword('not')
membersOf = (Literal('^') | CaselessKeyword('membersof'))('membersOf')




# Simple and complex expressions
# simpleExpressionConstraint << Optional(negationIndicator) + Optional(constraintOperator) + ZeroOrMore(membersOf) +\
#                              conceptReference + ZeroOrMore(conjOrDisj + simpleExpressionConstraint)
simpleExpressionConstraint << Optional(negationIndicator) + Optional(constraintOperator) + ZeroOrMore(membersOf) + conceptReference


# complexExpressionConstraint = ((simpleExpressionConstraint + Optional(Literal(':') + refinement)) |
#                                (expressionConstraint + OneOrMore(conjOrDisj + expressionConstraint)) |
#                                (Optional(negationIndicator) + Optional(constraintOperator) +
#                                 '(' + complexExpressionConstraint + ')'))
complexExpressionConstraint << simpleExpressionConstraint + Literal(':')('refinement') + refinement

# Root node -- expressionConstraint
expressionConstraint << (simpleExpressionConstraint |
                        complexExpressionConstraint  |
                        Group(Literal('(') + expressionConstraint + Literal(')')))


