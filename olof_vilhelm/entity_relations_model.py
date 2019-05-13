class Entity:

    def __init__(self, name: str, ):
        if not isinstance(name, str):
            raise TypeError("Entity name has to be a string.")

        self.name = name
        self.relations = set()

    def __eq__(self, other):
        if isinstance(other, Entity):
            if self.name == other.name:
                self.relations |= other.relations
                other.relation = self.relations
                return True
        return False


class Relation:
    FROM = "from"
    TO = "to"
    RELATION = "relation"

    def __init__(self, source, relation_word: str, *indices: int):
        if not isinstance(source, Source):
            raise TypeError("Argument 'source' must be of type", type(Source))

        if len(indices) % 2 != 0 and len(indices) < 2:
            raise ValueError("An even number of indices must be passed as argument ('start' and 'end' character indices). ")

        self.source = source
        self.word = relation_word
        self.__relation_c_indices = list()
        for i in range(0, len(indices), 2):
            self.__relation_c_indices.append((indices[i], indices[i + 1]))

        self.from_entity = None
        self.__from_entity_c_indices = list()

        self.to_entity = None
        self.__to_entity_c_indices = list()

    def from_(self, entity, *indices: int):
        if not isinstance(entity, Entity):
            raise ValueError("Argument 'entity' must be of type", type(Entity))

        if len(indices) % 2 != 0 and len(indices) < 2:
            raise ValueError("An even number of indices must be passed as argument ('start' and 'end' character indices). ")

        self.from_entity = entity
        for i in range(0, len(indices), 2):
            self.__from_entity_c_indices.append((indices[i], indices[i + 1]))
        self.from_entity.relations.add(self)
        return self

    def to_(self, entity, *indices: int):
        if not isinstance(entity, Entity):
            raise ValueError("Argument 'entity' must be of type", type(Entity))

        if len(indices) % 2 != 0 and len(indices) < 2:
            raise ValueError("An even number of indices must be passed as argument ('start' and 'end' character indices). ")

        self.to_entity = entity
        for i in range(0, len(indices), 2):
            self.__to_entity_c_indices.append((indices[i], indices[i + 1]))
        self.to_entity.relations.add(self)
        return self

    def indices(self, entity):
        if isinstance(entity, Entity):
            if entity == self.from_entity:
                return self.__from_entity_c_indices
            elif entity == self.to_entity:
                return self.__to_entity_c_indices
            else:
                ValueError("'entity' argument is not part of this relation.")

        elif isinstance(entity, str):
            if entity.strip().lower() == Relation.FROM:
                return self.__from_entity_c_indices
            elif entity.strip().lower() == Relation.TO:
                return self.__to_entity_c_indices
            elif entity.strip().lower() == Relation.RELATION:
                return self.__relation_c_indices
            else:
                ValueError(entity, "is not a recognised option. ")
        return


class Source:

    def __init__(self, text: str, identifier: str):
        self.text = text
        self.identifier = identifier
