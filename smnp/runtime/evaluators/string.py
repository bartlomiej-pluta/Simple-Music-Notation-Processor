from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class StringEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.string(node.value)

# TODO: make use of complex interpreter for code inside '{' and '}'
# def interpolate(string, environment):
#     interpolated = string.value
#     for scope in reversed(environment.scopes):
#         for name, value in scope.items():
#             interpolated = interpolated.replace('{' + name + '}', value.stringify())
#
#     nonMatchedVariables = re.findall(r"\{\w+\}", interpolated)
#     if len(nonMatchedVariables) > 0:
#         raise RuntimeException(f"Variable '{nonMatchedVariables[0][1:len(nonMatchedVariables[0])-1]}' is not declared",
#                                (string.pos[0], string.pos[1] + string.value.find(nonMatchedVariables[0])+1))
#
#     return interpolated
#
