from smnp.ast.node.none import NoneNode
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class LoopEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        iterator = expressionEvaluator(doAssert=True)(node.left, environment).value
        parameters = [ identifier.value for identifier in node.parameters ] if type(node.parameters) != NoneNode() else []

        try:
            environment.appendScope()

            output = {
                Type.INTEGER: cls.numberEvaluator,
                Type.BOOL: cls.boolEvaluator,
                Type.LIST: cls.listEvaluator,
                Type.MAP: cls.mapEvaluator
            }[iterator.type](node, environment, iterator, parameters, node.filter)

            environment.popScope()
        except KeyError:
            raise RuntimeException(f"The {iterator.type.name.lower()} type cannot stand as an iterator for loop statement", node.left.pos)

        return Type.list(output)

    @classmethod
    def numberEvaluator(cls, node, environment, evaluatedIterator, parameters, filter):
        output = []


        if len(parameters) > 1:
            raise RuntimeException(f"Loop with numeric iterator can handle only one parameter", node.parameters.pos)

        for i in range(evaluatedIterator.value):
            if len(parameters) > 0:
                environment.scopes[-1][parameters[0]] = Type.integer(i)

            if cls.doFilter(filter, environment):
                output.append(evaluate(node.right, environment).value)



        return output

    @classmethod
    def doFilter(cls, filter, environment):
        if type(filter) is not NoneNode:
            evaluation = expressionEvaluator(doAssert=True)(filter, environment).value
            if evaluation.type != Type.BOOL:
                raise RuntimeException(f"Expected {Type.BOOL.name.lower()} as filter expression, found {evaluation.type.name.lower()}", filter.pos)

            return evaluation.value

        return True



    @classmethod
    def boolEvaluator(cls, node, environment, evaluatedIterator, parameters, filter):
        output = []

        if len(parameters) > 0:
            raise RuntimeException(f"Loop with logic iterator can't' handle any parameters", node.parameters.pos)

        condition = evaluatedIterator
        while condition.value:
            if cls.doFilter(filter, environment):
                output.append(evaluate(node.right, environment).value)
            condition = expressionEvaluator(doAssert=True)(node.left, environment).value

        return output

    @classmethod
    def listEvaluator(cls, node, environment, evaluatedIterator, parameters, filter):
        output = []

        if len(parameters) > 2:
            raise RuntimeException(f"Loop with list iterator can handle only two parameters", node.parameters.pos)

        for i, value in enumerate(evaluatedIterator.value):
            if len(parameters) == 1:
                environment.scopes[-1][parameters[0]] = value
            if len(parameters) == 2:
                environment.scopes[-1][parameters[0]] = Type.integer(i)
                environment.scopes[-1][parameters[1]] = value

            if cls.doFilter(filter, environment):
                output.append(evaluate(node.right, environment).value)

        return output


    @classmethod
    def mapEvaluator(cls, node, environment, evaluatedIterator, parameters, filter):
        output = []

        if len(parameters) > 3:
            raise RuntimeException(f"Loop with map iterator can handle only three parameters", node.parameters.pos)

        i = 0
        for key, value in evaluatedIterator.value.items():
            if len(parameters) == 1:
                environment.scopes[-1][parameters[0]] = value
            if len(parameters) == 2:
                environment.scopes[-1][parameters[0]] = key
                environment.scopes[-1][parameters[1]] = value
            if len(parameters) == 3:
                environment.scopes[-1][parameters[0]] = Type.integer(i)
                environment.scopes[-1][parameters[1]] = key
                environment.scopes[-1][parameters[2]] = value
                i += 1

            if cls.doFilter(filter, environment):
                output.append(evaluate(node.right, environment).value)

        return output
