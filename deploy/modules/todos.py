from viur.core.prototypes import List


class Todos(List):
    #listTemplate = "example_list"

    def listFilter(self, query):
        return query  # everyone can see everything!

Todos.json = True