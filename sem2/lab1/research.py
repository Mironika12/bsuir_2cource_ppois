from typing import TypedDict

class Reference(TypedDict):
    reference: str
    is_read: bool = False

class Research:
    def __init__(self):
        self.__list_of_references: list[Reference] = []

    def _print_unexplored_references(self):
        for ref in self.__list_of_references:
            if not ref.get("is_read"):
                print(ref.get("reference"))

    def do_research(self):
        print("Неизученные источники:\n")
        self._print_unexplored_references()

    def add_reference(self, ref: Reference):
        if not isinstance(ref, Reference): #так нельзя, из-за тайпдикта
            raise TypeError("Тип данных не соответствует.")
        self.__list_of_references.append(ref)

    def remove_reference(self, ref: Reference):
        if not isinstance(ref, Reference):
            raise TypeError("Тип данных не соответствует.")
        self.__list_of_references.remove(ref)

    def print_references(self):
        i = 1
        for ref in self.__list_of_references:
            print(f"д{i}. {ref.get("reference")}.")
            i += 1

        if i < 5:
            print("""
                  Источников меньше пяти. Рекомендуется 
                  добавить больше источников.
                  """)

    