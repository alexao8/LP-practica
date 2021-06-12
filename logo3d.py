from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import Visitor
import sys

# Llegim de la entrada de consola
input_stream = FileStream(sys.argv[1])

# Lexer
lexer = logo3dLexer(input_stream)
token_stream = CommonTokenStream(lexer)

# Parser
parser = logo3dParser(token_stream)
tree = parser.root()

# Visitor
visitor = Visitor(sys.argv[2:])
visitor.visit(tree)
