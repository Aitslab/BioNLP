class EntitySet:
    def __init__(self, entities=None):
        self.__entities = list()
        if entities is not None:
            try:
                _ = iter(entities)
                self.add(entities)
            except TypeError:
                raise TypeError("Argument 'entities' must be some iterable with", type(Entity), "objects in it.")

    def list(self):
        return self.__entities

    def add(self, other):
        if isinstance(other, Entity):
            combined_relation = False
            for e in self.__entities:
                if e == other:
                    e.combine_relations(other)
                    combined_relation = True

            if not combined_relation:
                self.__entities.append(other)
        elif isinstance(other, EntitySet):
            for oe in other.__entities:
                self.add(oe)
        else:
            try:
                _ = iter(other)
                if all(isinstance(oe, Entity) for oe in other):
                    for oe in other:
                        self.add(oe)
                else:
                    raise TypeError("Argument 'entities' must be some iterable with", type(Entity), "objects in it.")
            except TypeError:
                raise TypeError("Argument 'other' must be of type " + str(type(Entity)) + ",", type(EntitySet), "or some Iterable with", type(Entity), "objects in it.")

        return self

    def append(self, other):
        return self.add(other)

    def __add__(self, other):
        return self.add(other)

    def __iadd__(self, other):
        return self.add(other)

    def __or__(self, other):
        return self.add(other)

    def __ior__(self, other):
        return self.add(other)


class Entity:

    def __init__(self, name: str, ):
        if not isinstance(name, str):
            raise TypeError("Argument 'name' must be a string.")

        self.name = name
        self.relations = set()

    def combine_relations(self, other):
        if self == other:
            self.relations |= other.relations
            other.relation = self.relations

    def __eq__(self, other):
        if isinstance(other, Entity):
            if self.name == other.name:
                return True
        return False

    def __lt__(self, other):
        if isinstance(other, Entity):
            return self.name < other.name
        else:
            raise TypeError("Argument 'other' must be of type", type(Entity))


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
            raise TypeError("Argument 'entity' must be of type", type(Entity))

        if len(indices) % 2 != 0 and len(indices) < 2:
            raise ValueError("An even number of indices must be passed as argument ('start' and 'end' character indices). ")

        self.from_entity = entity
        for i in range(0, len(indices), 2):
            self.__from_entity_c_indices.append((indices[i], indices[i + 1]))
        self.from_entity.relations.add(self)
        return self

    def to_(self, entity, *indices: int):
        if not isinstance(entity, Entity):
            raise TypeError("Argument 'entity' must be of type", type(Entity))

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
