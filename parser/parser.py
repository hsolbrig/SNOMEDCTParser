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
showHiddenLabels = True
def Suppressc(item, label):
    return Suppress(item) if not showHiddenLabels else Literal(item)(label)

#=================== ws = *(SP / HTAB / CR / LF) ; optional white space
ws = " \n\t\r"
ParserElement.DEFAULT_WHITE_CHARS = ws

#=================== integerValue = ( ["-"/"+"] digitNonZero *digit ) / zero
integerValue = Regex(r'[-+]?(0|([1-9][0-9]*))(?!\.)').setParseAction(lambda i : int(i[0]))('integer')

#=================== decimalValue = integerValue "." 1*digit
decimalValue = Regex(r'[-+]?(0|([1-9][0-9]*)).\d+').setParseAction(lambda d : float(d[0]))('decimal')

#=================== digitNonZero = %x31-39
digitNonZero = '123456789'

#=================== numericValue = integerValue / decimalValue
numericValue = integerValue | decimalValue

#=================== sctId = digitNonZero 5*17( digit )
sctid = Word(digitNonZero, nums, min=6, max=18).setParseAction(lambda i: int(i[0]))("sctid")

#=================== term = 1*nonwsNonPipe *( 1*SP 1*nonwsNonPipe )
nonPipe = CharsNotIn('|')
nonwsNonPipe = CharsNotIn('|' + ws)
pipe = Literal('|')
term = Combine(nonwsNonPipe + ZeroOrMore(White(ws=' ') + nonwsNonPipe))

#==================== conceptReference = conceptId [ws "|" ws term ws "|"]
conceptReference = Group(sctid +
                         Optional(Combine(Suppress(pipe + Optional(White())) +
                                          term  +
                                          Suppress(Optional(White()) + pipe)))("term"))("conceptReference")

#==================== descendantsOf = "<" / ( ("d"/"D") ("e"/"E") ("s"/"S") ("c"/"C") ("e"/"E") ("n"/"N") ("d"/"D")
#                         ("a"/"A") ("n"/"N") ("y"/"T") ("s"/"S") ("o"/"O") ("f"/"F")  " " )
descendantsOf = (Literal('<') + ~FollowedBy(Literal('<')) ^ CaselessKeyword('descendantsof'))('descendantsOf')

#==================== descendantsOrSelfOf = "<<" / ( ("d"/"D") ("e"/"E") ("s"/"S") ("c"/"C") ("e"/"E") ("n"/"N") ("d"/"D")
#                                ("a"/"A") ("n"/"N") ("y"/"T") ("s"/"S") ("o"/"O")("r"/"R") ("s"/"S")("e"/"E") ("l"/"L")
#                                ("f"/"F") ("o"/"O")("f"/"F")  " " )
desendantsOrSelfOf = (Literal('<<') | CaselessKeyword('descendantsorselfof'))('descendantsOrSelfOf')

#==================== ancestorsOf = ">" / ( ("a"/"A") ("n"/"N") ("c"/"C") ("e"/"E") ("s"/"S") ("t"/"T") ("o"/"O")
#                     ("r"/"R") ("s"/"S") ("o"/"O")("f"/"F")  " " )
ancestorsOf = (Literal('>') | CaselessKeyword('ancestorsof'))('ancestorsOf')

#==================== ancestorsOrSelfOf = ">>" / ( ("a"/"A") ("n"/"N") ("c"/"C") ("e"/"E") ("s"/"S") ("t"/"T") ("o"/"O")
#                              ("r"/"R") ("s"/"S") ("o"/"O") ("r"/"R") ("s"/"S") ("e"/"E") ("l"/"L") ("f"/"F")
#                              ("o"/"O")("f"/"F")  " " )
ancestorsOrSelfOf = (Literal('>>') | CaselessKeyword('ancestorsorselfof'))('ancestorsOrSelfOf')

#==================== conjunction = ("a"/"A") ("n"/"N") ("d"/"D") " " / ","
conjunction = Group(Suppress(CaselessKeyword('and')) | Suppress(','))('and')

#==================== disjunction = ("o"/"O") ("r"/"R") " "
disjunction = CaselessKeyword('or')('or')

#==================== many = "*" / ( ("m"/"M") ("a"/"A") ("n"/"N") ("y"/"Y")
many = Literal('*') | CaselessKeyword('many')

#==================== attributeName = conceptReference
attributeName = conceptReference

#==================== comparisonOperator = "=" / "!" ws "=" / ("n"/"N")("o"/"O")("t"/"T") ws "=" / "<" / "<=" / ">" / ">="
eqOp = Literal('=')
neqOp = (Literal('!') + Literal('=')) | (CaselessKeyword('not') + Literal('='))
ltOp = Literal('<') | CaselessKeyword('lt')
gtOp = Literal('>') | CaselessKeyword('gt')
leOp = Literal('<=') | CaselessKeyword('le')
geOp = Literal('>=') | CaselessKeyword('ge')


#==================== stringValue = 1*(anyNonEscapedChar / escapedChar)
#                     anyNonEscapedChar = HTAB / CR / LF / %x20-21 / %x23-5B / %x5D-7E / UTF8-2 / UTF8-3 / UTF8-4
#                     escapedChar = BS QM / BS BS
#  NOTE -- a bit broader on the non escaped characters
stringValue = Regex(r'([^"”\\]|(\\")|(\\”))*')('stringValue')

#==================== concreteValue =  QM stringValue QM / “#” numericValue
#                     QM = %x22 / "“" / "”"  ; quotation mark
#  NOTE: refined QM slightly
concreteValue = \
    (Suppress(Literal('"') | Literal('“')) + stringValue.leaveWhitespace() + Suppress(Literal('"') | Literal('”'))('string') |
    (Suppress('#') + numericValue))


#==================== attribute
# attribute = [cardinality ws] [reverseFlag ws] [attributeOperator ws] attributeName ws
#	          ("=" ws expressionConstraintValue / comparisonOperator ws concreteValue)
#
# attributeOperator = descendantsOf / descendantsOrSelfOf
# comparisonOperator = "=" / "!" ws "=" / ("n"/"N")("o"/"O")("t"/"T") ws "=" / "<" / "<=" / ">" / ">="
# reverseFlag = ("r"/"R") / ( ("r"/"R") ("e"/"E") ("v"/"V") ("e"/"E") ("r"/"R") ("s"/"S") ("e"/"E")
#               ("o"/"O") ("f"/"F")  )
# cardinality = "[" integerValue ".." (integerValue / many) "]"
#  NOTE: Should be unsignedInteger
#  Question:  0..0 allowed?
#
unsignedInteger = Word(nums).setParseAction(lambda i : int(i[0]))
cardinality = Group(Suppress('[') + unsignedInteger('lower') + Suppress('..') +
                    (unsignedInteger | many('*').setParseAction(lambda x:'*'))('upper') + Suppress(']'))('cardinality')
reverseFlag = CaselessKeyword('reverseOf')
attributeWithOp = (attributeName
                   | Group(Suppress(desendantsOrSelfOf) + attributeName)('descendantsOrSelfOf')
                   | Group(Suppress(descendantsOf) + attributeName)('descendantsOf')
                  )
reverseAttribute = (attributeWithOp | Group(Suppress(reverseFlag) + attributeWithOp)('reverse'))
attributeCardinality = (reverseAttribute | Group(cardinality + reverseAttribute )('cardinalityConstraint'))

# expressionConstraintValue = simpleExpressionConstraint /
#	                          "(" ws complexExpressionConstraint ws ")"
simpleConstraint = Forward()
nestedConstraint = Forward()
expressionConstraintValue = (simpleConstraint | nestedConstraint)

attribute = Forward()
attribute << Group(
               Group(attributeCardinality + Suppress(eqOp) + concreteValue)('eq')
             | Group(attributeCardinality + Suppress(neqOp) + concreteValue)('ne')
             | Group(attributeCardinality + Suppress(leOp) + concreteValue)('le')
             | Group(attributeCardinality + Suppress(ltOp) + concreteValue)('lt')
             | Group(attributeCardinality + Suppress(geOp) + concreteValue)('ge')
             | Group(attributeCardinality + Suppress(gtOp) + concreteValue)('gt')
             | Group(attributeCardinality + Suppress('=') + expressionConstraintValue)('equivalent')
             )('attribute')



#==============================================
# attributeSet  = attribute *(ws conjunction ws attribute) /
#                 "(" ws attributeSet ws ")" /
# 	              attributeSet ws (conjunction / disjunction) ws attributeSet

attributeSet = Forward()
simpleAttributeSet = Forward()
simpleAttributeSet << (delimitedList(attribute, delim=conjunction)
                       | (Suppressc('(', 'asp') + attributeSet + Suppressc(')', 'asp')))


attributeSetConj = delimitedList(simpleAttributeSet, delim=disjunction)
attributeSet << delimitedList(attributeSetConj, delim=conjunction)



# attributeGroup = "{" ws attributeSet ws "}" /
#                  “(“ ws attributeGroup ws “)” /
# 	               attributeGroup ws (conjunction / disjunction) ws attributeGroup
simpleAttributeGroup = Forward()
attributeGroup = Forward()
simpleAttributeGroup << ((Suppress('{') + attributeSet + Suppress('}'))
                         ^ (Suppressc('(','agp') + attributeGroup + Suppressc(')','agp')))

attributeGroup << Group(simpleAttributeGroup
                   ^ Group(simpleAttributeGroup + Optional(Suppress(conjunction)) + attributeGroup)('conjunction')
                   ^ Group(simpleAttributeGroup + Suppress(disjunction) + attributeGroup)('disjunction')
                  )('attributeGroup')




# refinement = (attributeSet / attributeGroup) *( ws [conjunction ws] attributeGroup ) /
# 	           “(“ ws refinement ws “)” /
#               refinement ws (conjunction / disjunction) ws refinement
refinement = (attributeSet | attributeGroup) + ZeroOrMore(Optional(conjunction) + attributeGroup)

# negationIndicator = "!" / ( ("n"/"N") ("o"/"O") ("t"/"T") " " )
#    NOTE: Why the single trailing space (vs WS)?
negationIndicator = Literal('!') | CaselessKeyword('not')

# membersOf = "^" / ( ("m"/"M") ("e"/"E") ("m"/"M") ("b"/"B") ("e"/"E") ("r"/"R") ("s"/"S")
#                     ("o"/"O") ("f"/"F") " " )
membersOf = (Literal('^') | CaselessKeyword('membersof'))
# memberReference = conceptReference / membersOf memberReference
memberReference = Forward()
memberReference << (conceptReference | Group(Suppress(membersOf )+ memberReference)('membersOf'))


# simpleConstraint = [negationIndicator ws] [constraintOperator ws] memberReference
opWithSimpleConstraint = (memberReference
                          ^ Group(Suppress(desendantsOrSelfOf) + memberReference)("descendantsOrSelfOf")
                          ^ Group(Suppress(descendantsOf) + memberReference)("descendantsOf")
                          ^ Group(Suppress(ancestorsOrSelfOf) + memberReference)("ancestorsOrSelfOf")
                          ^ Group(Suppress(ancestorsOf) + memberReference)("ancestorsOf"))

negatedSimpleConstraint = (opWithSimpleConstraint | Group(Suppress(negationIndicator) + opWithSimpleConstraint)("not"))
simpleConstraint << negatedSimpleConstraint

# simpleConstraintSet = simpleConstraint [conjunction simpleConstraintSet]
simpleConstraintSet = Forward()
simpleConstraintSet << (simpleConstraint
                        ^ Group(simpleConstraint + Suppress(conjunction) + simpleConstraintSet)('conjunction')
                        ^ Group(simpleConstraint + Suppress(disjunction) + simpleConstraintSet)('disjunction'))


# simpleConstraint = [negationIndicator ws] [constraintOperator ws] memberReference
constraint = Forward()
nestedConstraint << (Suppress('(') + constraint + Suppress(')'))
opWithNestedConstraint = (nestedConstraint
                          ^ Group(Suppress(desendantsOrSelfOf) + nestedConstraint)("descendantsOrSelfOf")
                          ^ Group(Suppress(descendantsOf) + nestedConstraint)("descendantsOf")
                          ^ Group(Suppress(ancestorsOrSelfOf) + nestedConstraint)("ancestorsOrSelfOf")
                          ^ Group(Suppress(ancestorsOf) + nestedConstraint)("ancestorsOf"))
negatedNestedExpression = (opWithNestedConstraint ^ Group(negationIndicator + opWithNestedConstraint)("not"))
refinedConstraint = Group((simpleConstraint + ':' + refinement)('refinement')
                          ^ negatedNestedExpression)('refinedConstraint')


# refinedConstraintSet = refinedConstraint [ (conjunction / disjunction) refinedConstraintSet]
#    Conjunction operators are equal precedence and parse left to right
refinedConstraintSet = Forward()
refinedConstraintSet << (refinedConstraint + Optional(
                            Group(conjunction + refinedConstraintSet)('conjunction')
                            ^ Group(disjunction + refinedConstraintSet)('disjunction') ) )


constraint << Group(refinedConstraintSet | simpleConstraintSet)('constraint')
