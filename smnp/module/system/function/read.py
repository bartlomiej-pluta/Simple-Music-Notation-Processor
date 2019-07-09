
# TODO read function
# def read(args, env):
#     if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
#         print(args[0], end="")
#         value = input()
#         if args[1] == "integer":
#             try:
#                 return int(value)
#             except ValueError as v:
#                 pass # not int
#         elif args[1] == "string":
#             return value
#         # TODO: note - wydzielić parsowanie nut do osobnej funkcji w pakiecie smnp.note
#         # elif args[1] == "note":
#         #     chars, token = tokenizeNote(value, 0, 0)
#         #     if chars == 0:
#         #         return # not note
#         #     return parseNote([token], None).value
#         else:
#             pass # invalid type
#     elif len(args) == 1 and isinstance(args[0], str):
#         print(args[0], end="")
#         return input()
#     elif len(args) == 0:
#         return input()
#     else:
#         pass # not valid signature