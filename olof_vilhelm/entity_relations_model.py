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

    def __init__(self, source, relation_word: str, char_index_from: int, char_index_to: int):
        if not isinstance(source, Source):
            raise TypeError("Argument 'source' must be of type", type(Source))

        self.source = source
        self.word = relation_word
        self.__relation_char_index_start = char_index_from
        self.__relation_char_index_end = char_index_to

        self.from_entity = None
        self.__from_entity_c_index_start = -1
        self.__from_entity_c_index_end = -1

        self.to_entity = None
        self.__to_entity_c_index_start = -1
        self.__to_entity_c_index_end = -1

    def from_(self, entity, char_index_from: int, char_index_to: int):
        if not isinstance(entity, Entity):
            raise ValueError("Argument 'entity' must be of type", type(Entity))

        self.from_entity = entity
        self.__from_entity_c_index_start = char_index_from
        self.__from_entity_c_index_end = char_index_to
        self.from_entity.relations.add(self)
        return self

    def to_(self, entity, char_index_from: int, char_index_to: int):
        if not isinstance(entity, Entity):
            raise ValueError("Argument 'entity' must be of type", type(Entity))

        self.to_entity = entity
        self.__to_entity_c_index_start = char_index_from
        self.__to_entity_c_index_end = char_index_to
        self.to_entity.relations.add(self)
        return self

    def indices(self, entity):
        if isinstance(entity, Entity):
            if entity == self.from_entity:
                return self.__from_entity_c_index_start, self.__from_entity_c_index_end
            elif entity == self.to_entity:
                return self.__to_entity_c_index_start, self.__to_entity_c_index_end
            else:
                ValueError("'entity' argument is not part of this relation.")

        elif isinstance(entity, str):
            if entity.strip().lower() == Relation.FROM:
                return self.__from_entity_c_index_start, self.__from_entity_c_index_end
            elif entity.strip().lower() == Relation.TO:
                return self.__to_entity_c_index_start, self.__to_entity_c_index_end
            elif entity.strip().lower() == Relation.RELATION:
                return self.__relation_char_index_start, self.__relation_char_index_end
            else:
                ValueError(entity, "is not a recognised option. ")
        return


class Source:

    def __init__(self, text: str, identifier: str):
        self.text = text
        self.identifier = identifier
