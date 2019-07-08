def abstractIterableEvaluator(itemEvaluator):
    def evaluator(node, environment):
        evaluatedItems = []
        for item in node.children:
            result = itemEvaluator(item, environment)
            evaluatedItems.append(result.value)

        return evaluatedItems

    return evaluator