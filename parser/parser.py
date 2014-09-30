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

# Debug code for determining where suppressed things come from
showHiddenLabels = False
def Suppressc(item, label):
    return Suppress(item) if not showHiddenLabels else Literal(item)(label)

# ws = *(SP / HTAB / CR / LF) ; optional white space
ws = " \n\t\r"
ParserElement.DEFAULT_WHITE_CHARS = ws

# integerValue = ( ["-"/"+"] digitNonZero *digit ) / zero
integerValue = Regex(r'[-+]?(0|([1-9][0-9]*))(?!\.)').setParseAction(lambda i : int(i[0]))('integer')

# decimalValue = integerValue "." 1*digit
decimalValue = Regex(r'[-+]?(0|([1-9][0-9]*)).\d+').setParseAction(lambda d : float(d[0]))('decimal')

# digitNonZero = %x31-39
digitNonZero = '123456789'

# numericValue = integerValue / decimalValue
numericValue = integerValue ^ decimalValue

# sctId = digitNonZero 5*17( digit )
sctid = Word(digitNonZero, nums, min=6, max=18).setParseAction(lambda i: int(i[0]))("sctid")

# term = 1*nonwsNonPipe *( 1*SP 1*nonwsNonPipe )
# Question: why can you have leading and trailing tabs, cr's and lf's but not embedded?
nonPipe = CharsNotIn('|')
nonwsNonPipe = CharsNotIn('|' + ws)
pipe = Literal('|')
term = Combine(nonwsNonPipe + ZeroOrMore(White(ws=' ') + nonwsNonPipe))

#conceptReference = conceptId [ws "|" ws term ws "|"]
conceptReference = Group(sctid +
                         Optional(Combine(Suppress(pipe + Optional(White())) +
                                          term  +
                                          Suppress(Optional(White()) + pipe)))("term"))("conceptReference")

# descendantsOf = "<" / ( ("d"/"D") ("e"/"E") ("s"/"S") ("c"/"C") ("e"/"E") ("n"/"N") ("d"/"D")
#                         ("a"/"A") ("n"/"N") ("y"/"T") ("s"/"S") ("o"/"O") ("f"/"F")  " " )
descendantsOf = (Literal('<') + ~FollowedBy(Literal('<')) ^ CaselessKeyword('descendantsof'))('descendantsOf')

# descendantsOrSelfOf = "<<" / ( ("d"/"D") ("e"/"E") ("s"/"S") ("c"/"C") ("e"/"E") ("n"/"N") ("d"/"D")
#                                ("a"/"A") ("n"/"N") ("y"/"T") ("s"/"S") ("o"/"O")("r"/"R") ("s"/"S")("e"/"E") ("l"/"L")
#                                ("f"/"F") ("o"/"O")("f"/"F")  " " )
desendantsOrSelfOf = (Literal('<<') | CaselessKeyword('descendantsorselfof'))('descendantsOrSelfOf')

# ancestorsOf = ">" / ( ("a"/"A") ("n"/"N") ("c"/"C") ("e"/"E") ("s"/"S") ("t"/"T") ("o"/"O")
#                     ("r"/"R") ("s"/"S") ("o"/"O")("f"/"F")  " " )
ancestorsOf = (Literal('>') | CaselessKeyword('ancestorsof'))('ancestorsOf')

# ancestorsOrSelfOf = ">>" / ( ("a"/"A") ("n"/"N") ("c"/"C") ("e"/"E") ("s"/"S") ("t"/"T") ("o"/"O")
#                              ("r"/"R") ("s"/"S") ("o"/"O") ("r"/"R") ("s"/"S") ("e"/"E") ("l"/"L") ("f"/"F")
#                              ("o"/"O")("f"/"F")  " " )
ancestorsOrSelfOf = (Literal('>>') | CaselessKeyword('ancestorsorselfof'))('ancestorsOrSelfOf')

# constraintOperator = descendantsOf / descendantsOrSelfOf / ancestorsOf / ancestorsOrSelfOf
constraintOperator = desendantsOrSelfOf | descendantsOf |  ancestorsOrSelfOf | ancestorsOf

# conjunction = ("a"/"A") ("n"/"N") ("d"/"D") " " / ","
conjunction = Group(CaselessKeyword('and') | ',')('and')

# disjunction = ("o"/"O") ("r"/"R") " "
disjunction = CaselessKeyword('or')('or')


# -- Added as a helper ---
conjOrDisj = (conjunction | disjunction)


# many = "*" / ( ("m"/"M") ("a"/"A") ("n"/"N") ("y"/"Y")
many = Literal('*') | CaselessKeyword('many')

# cardinality = "[" integerValue ".." (integerValue / many) "]"
#  NOTE: Tightened up the lower value.
#  Question:  0..0 allowed?
unsignedInteger = Word(nums).setParseAction(lambda i : int(i[0]))
cardinality = Group(Suppress('[') + unsignedInteger('lower') + Suppress('..') +
                    (unsignedInteger | many('*').setParseAction(lambda x:'*'))('upper') + Suppress(']'))('cardinality')

# reverseFlag = ("r"/"R") / ( ("r"/"R") ("e"/"E") ("v"/"V") ("e"/"E") ("r"/"R") ("s"/"S") ("e"/"E")
#               ("o"/"O") ("f"/"F")  )
reverseFlag = CaselessKeyword('reverseOf')

# attributeOperator = descendantsOf / descendantsOrSelfOf
# Q: Reverse order in abnf?
attributeOperator = desendantsOrSelfOf | descendantsOf

# attributeName = conceptReference
attributeName = conceptReference

# comparisonOperator = "=" / "!" ws "=" / ("n"/"N")("o"/"O")("t"/"T") ws "=" / "<" / "<=" / ">" / ">="
comparisonOperator = (Literal('=')('eq') |
                      Group( (Literal('!') + Literal('=')) |
                             (Literal('not') + Literal('='))).setParseAction(lambda x: ''.join(x[0]))('neq') |
                      Literal('<=')('leq') | Literal('<')('lt') | Literal('>=')('geq') | Literal('>')('gt'))

# stringValue = 1*(anyNonEscapedChar / escapedChar)
# anyNonEscapedChar = HTAB / CR / LF / %x20-21 / %x23-5B / %x5D-7E / UTF8-2 / UTF8-3 / UTF8-4
# escapedChar = BS QM / BS BS
#  NOTE -- a bit broader on the non escaped characters
stringValue = Regex(r'([^"”\\]|(\\")|(\\”))*')('stringValue')

# concreteValue =  QM stringValue QM / “#” numericValue
# QM = %x22 / "“" / "”"  ; quotation mark
#  NOTE: refined QM slightly
concreteValue = \
    (Suppress(Literal('"') | Literal('“')) + stringValue.leaveWhitespace() + Suppress(Literal('"') | Literal('”'))('string') |
    (Suppress('#') + numericValue))


simpleConstraint = Forward()
refinedConstraint = Forward()

# attribute = [cardinality ws] [reverseFlag ws] [attributeOperator ws] attributeName ws
#	          ("=" ws expressionConstraintValue / comparisonOperator ws concreteValue)
attributeWithOp = (attributeName
                   | Group(Suppress(desendantsOrSelfOf) + attributeName)('descendantsOrSelfOf')
                   | Group(Suppress(descendantsOf) + attributeName)('descendantsOf')
                  )
reverseAttribute = (attributeWithOp | Group(Suppress(reverseFlag) + attributeWithOp)('reverse'))
attributeCardinality = (reverseAttribute | Group(cardinality + reverseAttribute )('cardinality'))
attribute = Group(attributeCardinality + Suppress('=') + (simpleConstraint | refinedConstraint ))('equivalent') |

(Group(comparisonOperator + concreteValue)('concrete') |



# attributeSet = attribute *(ws conjunction ws attribute) /
#                 "(" ws attributeSet ws ")" /
# 	             attributeSet ws (conjunction / disjunction) ws attributeSet
simpleAttributeSet = Forward()
simpleAttributeSet << Group(
                    Group( attribute + ZeroOrMore((conjunction) + attribute))
                    | (Suppressc('(', 'asp') + simpleAttributeSet + Suppressc(')', 'asp'))
                 )('attributeSet')

attributeSet = simpleAttributeSet + ZeroOrMore(conjOrDisj + simpleAttributeSet)

def foo(e):
    print(e)
    return e

# attributeGroup = "{" ws attributeSet ws "}" /
#                  “(“ ws attributeGroup ws “)” /
# 	               attributeGroup ws (conjunction / disjunction) ws attributeGroup
# TODO: ERROR - conjunction/disjunction need to be optional, at least in the case of brackets
simpleAttributeGroup = Forward()
simpleAttributeGroup << (Group((Suppress('{') + attributeSet + Suppress('}')))('attributeGroup') |
                        (Suppressc('(','agp') + simpleAttributeGroup + Suppressc(')','agp')('i1')))

attributeGroup = Group(simpleAttributeGroup + ZeroOrMore(Optional(conjOrDisj) + simpleAttributeGroup)).setParseAction(lambda e: foo(e))




# refinement = (attributeSet / attributeGroup) *( ws [conjunction ws] attributeGroup ) /
# 	           “(“ ws refinement ws “)” /
#               refinement ws (conjunction / disjunction) ws refinement
refinement = (attributeSet | attributeGroup) + ZeroOrMore(Optional(conjunction) + attributeGroup)

# negationIndicator = "!" / ( ("n"/"N") ("o"/"O") ("t"/"T") " " )
#    NOTE: Why the single trailing space (vs WS)?
negationIndicator = Literal('!') | CaselessKeyword('not')

# membersOf = "^" / ( ("m"/"M") ("e"/"E") ("m"/"M") ("b"/"B") ("e"/"E") ("r"/"R") ("s"/"S")
#                     ("o"/"O") ("f"/"F") " " )
membersOf = (Literal('^') | CaselessKeyword('membersof'))('membersOf')


# A simpleConstraint is is a constraint is
#                             (a) it is conceptReference
#                             (b) it is membersOf (a) or (b)
#                             (c) it is a constraint on (a) or (b)
#                             (d) it is a negation of (a), (b) or (c)
#                             (e) it is a conjunction of (a-d) with (a-d)
#
# simpleExpressionConstraint =  [negationIndicator ws] [constraintOperator ws] *(membersOf ws)
# 	conceptReference *( ws (conjunction / disjunction) ws simpleExpressionConstraint)

membersOfExpression = Forward()
membersOfExpression << (conceptReference | Group(Suppress(membersOf) + membersOfExpression)("membersOf"))
constrainedReference = (membersOfExpression | Group(constraintOperator + membersOfExpression)("constraint"))
negatedReference = (constrainedReference | Group(negationIndicator + conceptReference)("not"))

simpleSimpleConstraint = Forward()
simpleSimpleConstraint << (negatedReference ^ (Suppress('(') + simpleSimpleConstraint + Suppress(')')))
simpleConstraint << (simpleSimpleConstraint + ZeroOrMore(conjOrDisj + simpleSimpleConstraint))


# A refinedConstraint is a constraint with a refinement.  A refinedConstraint cannot itself be refined
#
refinedConstraint << (Group(
                        Group(simpleConstraint + Suppress(':') + (refinedConstraint | simpleConstraint))("refinement") |
                        Group(refinedConstraint + Suppress(conjunction) + refinedConstraint)("conjunction") |
                        Group(refinedConstraint + Suppress(disjunction) + refinedConstraint)("disjunction") |
                        (Suppress('(') + refinedConstraint + Suppress(')'))
                    )("refinedConstraint"))


# An expression is complex if (a) it is a refinement
#                             (b) it is a constraint on expression enclosed in parenthesis
#                             (b) it is a conjunction or disjunction of a parenthesized
#                             (c) it is a negation of a complex expression
#                             (d) it is an operation on a complex expression
#
# complexExpressionConstraint = simpleExpressionConstraint ws ":" ws refinement /
# 	expressionConstraint 1*(ws (conjunction / disjunction) ws expressionConstraint /
# 	 [negationIndicator ws] 	[constraintOperator ws]
# 	"(" ws complexExpressionConstraint ws ")"
# nestedComplexExpression = Group(Suppress("(") + complexExpressionConstraint + Suppress(")"))('group')
# nestedComplexExpression = complexExpressionConstraint
# constrainedExpression = (nestedComplexExpression | Group(constraintOperator + nestedComplexExpression)('constraint'))
# negatedComplexExpression = (constrainedExpression | Group(negationIndicator + constrainedExpression)("not"))
#
# complexExpressionConstraint << (Group(simpleExpressionConstraint + Suppress(':') + refinement)('refinement') |
#                                 negatedComplexExpression + ~FollowedBy(conjOrDisj) |
#                                 Group(negatedComplexExpression + Suppress(conjunction) + complexExpressionConstraint)('conjunction') |
#                                 Group(negatedComplexExpression + Suppress(disjunction) + complexExpressionConstraint)('disjunction'))
#
# refinedExpression =


# Root node -- expressionConstraint
#
#  expressionConstraint = ws (simpleExpressionConstraint / complexExpressionConstraint /
# #	                      "(" ws expressionConstraint ws ")" ) ws """
# expressionConstraint << (simpleExpressionConstraint + ~FollowedBy(':') |
#                          complexExpressionConstraint )


# General notion: a refinedConstraint is a constraint that includes a refinement.  A refined constraint cannot itself
# be refined
#
# Operator precedence:
#
# UNARY Operators
#   membersOf        -- can only be applied to conceptReference or another membersOf
#   refinement
#   constraintOperator
#   negationIndicator
#   reverse
#   cardinality
