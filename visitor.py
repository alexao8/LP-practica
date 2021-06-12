
# Imports
if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor

from queue import LifoQueue
import turtle3d


class Visitor(logo3dVisitor):
    # Atributs per les variables locals
    context = {}
    context_stack = LifoQueue()

    # Atributs per les funcions
    f_dict = {}
    f_inicial = 'main'
    pars_inicials = None

    # Turtle
    t = turtle3d.Turtle3D()

    # Constructora
    def __init__(self, argv_list):

        size = len(argv_list)

        if size > 0:
            self.f_inicial = argv_list[0]

        if size > 1:
            self.pars_inicials = argv_list[1:]

    # Funcio principal
    def visitRoot(self, ctx):

        try:
            # Visitem el bloc del que esta format
            clist = list(ctx.getChildren())
            self.visit(clist[0])

            # Executem la funcio inicial.
            if self.f_inicial not in self.f_dict.keys():
                raise ProcNotDefined

            if self.pars_inicials is not None:

                f_pars = self.f_dict[self.f_inicial]['parameters']

                if len(f_pars) != len(self.pars_inicials):
                    raise IncorrectNumberOfParameters

                for var, val in zip(f_pars, self.pars_inicials):
                    self.context[var] = float(val)

            self.visit(self.f_dict[self.f_inicial]['code'])

        except ZeroDivisionError:
            print('No es pot dividir entre 0!')

        except ProcNotDefined:
            print(ProcNotDefined())

        except IncorrectNumberOfParameters:
            print(IncorrectNumberOfParameters())

        except ProcAlreadyDefined:
            print(ProcAlreadyDefined())

        except RepeatedFormalParameter:
            print(RepeatedFormalParameter())

    # Bloc es un conjunt de sentencies
    def visitBloc(self, ctx):

        clist = list(ctx.getChildren())
        for c in clist:
            self.visit(c)

    # Retorna el valor s'una expressio
    def visitExpr(self, ctx):
        # Agafa els fills
        clist = list(ctx.getChildren())

        # Si es una fulla retorna el seu valor
        if len(clist) == 1:

            # Mirem si es un enter
            if logo3dParser.symbolicNames[clist[0].getSymbol().type] == 'INT':
                return int(clist[0].getText())

            # Mirem si es un float
            if logo3dParser.symbolicNames[clist[0].getSymbol().type] == 'FLOAT':
                return float(clist[0].getText())

            # Sino, es una variable i s'ha d'agafar el seu valor
            else:
                var = clist[0].getText()
                return self.context[var]

        else:  # len(l) == 3

            # Expresio dins de parentesis
            if clist[0].getText() == '(':
                return self.visit(clist[1])

            # Expresio sense parentesis
            op1 = self.visit(clist[0])
            op2 = self.visit(clist[2])
            operation = clist[1].getText()

            if operation == '*':
                return op1 * op2

            elif operation == '/':
                return op1 / op2

            elif operation == '+':
                return op1 + op2

            elif operation == '-':
                return op1 - op2

            elif operation == '>':
                if op1 > op2:
                    return 1
                else:
                    return 0

            elif operation == '<':
                if op1 < op2:
                    return 1
                else:
                    return 0

            elif operation == '>=':
                if op1 >= op2:
                    return 1
                else:
                    return 0

            elif operation == '<=':
                if op1 <= op2:
                    return 1
                else:
                    return 0

            elif operation == '=':
                if op1 == op2:
                    return 1
                else:
                    return 0

            else:
                if op1 != op2:
                    return 1
                else:
                    return 0

    # Guarda una funcio en el diccionari de funcions
    def visitF_declaration_sent(self, ctx):
        clist = list(ctx.getChildren())

        # Nom de la funcio
        f_id = clist[1].getText()

        if f_id in self.f_dict.keys():
            raise ProcAlreadyDefined

        # Atributs de la funcio
        parameters = self.visit(clist[3])
        code = clist[6]

        # Guardem la nova funcio al diccionari
        self.f_dict[f_id] = {}
        self.f_dict[f_id]['parameters'] = parameters
        self.f_dict[f_id]['code'] = code

    # Retorna el nom dels parametres d'una funcio
    def visitP_decl(self, ctx):
        clist = list(ctx.getChildren())

        parameters = []
        for i in range(0, len(clist), 2):

            par = clist[i].getText()

            if par in parameters:
                raise RepeatedFormalParameter

            parameters.append(par)

        return parameters

    # Executa una funcio del diccionari de funcions
    def visitF_sent(self, ctx):
        clist = list(ctx.getChildren())

        # Nom de la funcio
        f_id = clist[0].getText()

        if f_id not in self.f_dict.keys():
            raise ProcNotDefined

        # Parametres que requereix la funcio
        f_pars = self.f_dict[f_id]['parameters']

        # Parametres que arriben en la crida
        c_pars = self.visit(clist[2])

        if len(f_pars) != len(c_pars):
            raise IncorrectNumberOfParameters

        # Guardar l'estat actual en la pila i resetejarla
        self.context_stack.put(self.context)
        self.context = {}

        # Guardar els parametres com variables locals
        for var, val in zip(f_pars, c_pars):
            self.context[var] = val

        # Cridem a la funcio
        self.visit(self.f_dict[f_id]['code'])

        # Restaurem el contexte anterior a la crida
        self.context = self.context_stack.get()

    # Retorna el valor que prendran els parametres en la crida
    def visitP_exec(self, ctx):
        clist = list(ctx.getChildren())

        parameters = []
        for i in range(0, len(clist), 2):
            parameters.append(self.visit(clist[i]))

        return parameters

    # S'assigna un valor a una variable
    def visitAssig_sent(self, ctx):
        # Agafa els fills
        clist = list(ctx.getChildren())

        # Nom de la var i valor que se li assigna
        var = clist[0].getText()
        val = self.visit(clist[2])

        # Assignem el valor en el diccionari
        self.context[var] = val

    # Llegeix un valor i l'assigna a una variable
    def visitRead_sent(self, ctx):
        clist = list(ctx.getChildren())

        var = clist[1].getText()
        val = int(input(str(var) + ' = '))

        self.context[var] = val

    # Mostra per pantalla el valor de una expressio
    def visitWrite_sent(self, ctx):
        clist = list(ctx.getChildren())
        print(self.visit(clist[1]))

    # Executa una sentencia condicional
    def visitIf_sent(self, ctx):
        clist = list(ctx.getChildren())

        # Valor de la expressio de la condicio
        cond_val = self.visit(clist[1])

        # Un valor entre -1e-6 i 1e-6 és fals, qualsevol altre valor és cert.
        if cond_val < -1e-6 or cond_val > 1e-6:
            self.visit(clist[3])

        elif len(clist) == 7:
            self.visit(clist[5])

    # Executa un bucle while
    def visitWhile_sent(self, ctx):
        clist = list(ctx.getChildren())

        while self.visit(clist[1]) < -1e-6 or self.visit(clist[1]) > 1e-6:
            self.visit(clist[3])

    # Executa un bucle for
    def visitFor_sent(self, ctx):
        clist = list(ctx.getChildren())

        # Inicialitzacio del contador
        var = clist[1].getText()
        init_value = self.visit(clist[3])
        self.context[var] = init_value

        # Valor final de comptatge
        final_value = self.visit(clist[5])

        while self.context[var] <= final_value:
            self.visit(clist[7])
            self.context[var] += 1

    # Executa una funcio del Turtle3d
    def visitTurtle_sent(self, ctx):
        clist = list(ctx.getChildren())

        f_id = clist[0].getText()
        pars = self.visit(clist[2])

        if f_id == 'forward':
            self.t.forward(pars[0])

        elif f_id == 'backward':
            self.t.backward(pars[0])

        elif f_id == 'right':
            self.t.right(pars[0])

        elif f_id == 'left':
            self.t.left(pars[0])

        elif f_id == 'up':
            self.t.up(pars[0])

        elif f_id == 'down':
            self.t.down(pars[0])

        elif f_id == 'color':
            self.t.change_color(pars)

        elif f_id == 'show':
            self.t.show()

        elif f_id == 'hide':
            self.t.hide()

        elif f_id == 'home':
            self.t.home()


class ProcAlreadyDefined(Exception):
    def __str__(self):
        return 'Ja existeix un procediment amb aquest nom'


class ProcNotDefined(Exception):
    def __str__(self):
        return 'El procediment cridat no existeix!'


class IncorrectNumberOfParameters(Exception):
    def __str__(self):
        return 'El numero de parametres no és correcte'


class RepeatedFormalParameter(Exception):
    def __str__(self):
        return 'No es poden repetir els noms dels paràmetres formals'
