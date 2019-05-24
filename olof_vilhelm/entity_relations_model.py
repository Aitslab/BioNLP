class RelationalSet:
    def __init__(self, items=None):
        self.__items = list()
        self.T = None
        if items is not None:
            try:
                _ = iter(items)
                # Set the RelationalSetType to the type of the first item, if it's Entity or Source.
                for item in items:
                    self.T = type(item)
                    if self.T not in (Entity, Source):
                        raise TypeError()
                    break

                self.add(items)
            except TypeError:
                raise TypeError("Argument 'items' must be some iterable with exclusively Entity or Source objects in it.")

    def list(self):
        return self.__items

    def add(self, other):
        if not self.__items and self.T is None:  # if __items is empty and type hasn't been detected
            if isinstance(other, RelationalSet):
                self.T = other.T
            else:
                self.T = type(other)
                if self.T not in (Entity, Source):
                    try:  # Might be an Iterable
                        _ = iter(other)
                        for oi in other:
                            self.T = type(oi)
                            if self.T not in (Entity, Source):
                                raise TypeError()
                            break
                    except TypeError:
                        raise TypeError("Argument 'other' must be an Entity, Source or RelationalSet object, or some Iterable with Entity or Source objects in it.")

        if isinstance(other, self.T):
            combined_relation = False
            for e in self.__items:
                if e == other:
                    e.combine_relations(other)
                    combined_relation = True

            if not combined_relation:
                self.__items.append(other)
        elif isinstance(other, RelationalSet):
            for oi in other.__items:
                self.add(oi)
        else:
            try:
                _ = iter(other)
                if all(isinstance(oi, self.T) for oi in other):
                    for oi in other:
                        self.add(oi)
                else:
                    raise TypeError()
            except TypeError:
                raise TypeError("Argument 'other' must be an Entity, Source or RelationalSet object, or some Iterable with Entity or Source objects in it.")

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

    def __getitem__(self, item):
        return self.__items[item]

    def __len__(self):
        return len(self.__items)


class Entity:

    def __init__(self, name: str, ):
        if not isinstance(name, str):
            raise TypeError("Argument 'name' must be a string.")

        self.name = name
        self.relations = set()
        self.active_relations = set()
        self.passive_relations = set()

    def combine_relations(self, other):
        if self == other:
            self.relations |= other.relations
            self.active_relations |= other.active_relations
            self.passive_relations |= other.passive_relations
            other.relation = self.relations
            other.active_relations = self.active_relations
            other.passive_relations = self.passive_relations

    def __eq__(self, other):
        if isinstance(other, Entity):
            if self.name == other.name:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Entity):
            return self.name < other.name
        else:
            raise TypeError("Argument 'other' must be of type", type(Entity))


class Relation:
    FROM = "from"
    TO = "to"
    RELATION = "relation"

    def __init__(self, source, relation_word: str, inverse_relation_word: str, *indices: int,):
        if not isinstance(source, Source):
            raise TypeError("Argument 'source' must be of type", type(Source))

        if len(indices) % 2 != 0 and len(indices) < 2:
            raise ValueError("An even number of indices must be passed as argument ('start' and 'end' character indices). ")

        self.source = source
        self.source.relations.add(self)
        self.word = relation_word
        self.inverse_word = inverse_relation_word
        self.__relation_c_indices = list()
        for i in range(0, len(indices), 2):
            self.__relation_c_indices.append((indices[i], indices[i + 1]))

        self.from_entity = None
        self.__from_entity_c_indices = list()

        self.to_entity = None
        self.__to_entity_c_indices = list()

    def from_(self, entity, *indices: int):
        if not isinstance(entity, Entity):
            raise TypeError("Argument 'entity' must be of type entity_relations_model.Entity")

        if len(indices) % 2 != 0 and len(indices) < 2:
            raise ValueError("An even number of indices must be passed as argument ('start' and 'end' character indices). ")

        self.from_entity = entity
        for i in range(0, len(indices), 2):
            self.__from_entity_c_indices.append((indices[i], indices[i + 1]))
        self.from_entity.relations.add(self)
        self.from_entity.active_relations.add(self)
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
        self.to_entity.passive_relations.add(self)
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
        self.relations = set()

    def combine_relations(self, other):
        if self == other:
            self.relations |= other.relations
            other.relations = self.relations

    def __eq__(self, other):
        if isinstance(other, Source):
            return self.text == other.text and self.identifier == other.identifier
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


if __name__ == "__main__":
    e1 = Entity("entity 1")
    e2 = Entity("entity 2")
    e3 = Entity("entity 2")
    s1 = Source("source 1", "id 1")
    s2 = Source("source 2", "id 2")
    print("e1 == e1", e1 == e1)
    print("e1 != e1", e1 != e1)
    print("e1 == e2", e1 == e2)
    print("e1 != e2", e1 != e2, "\n")

    print("s1 == s1", s1 == s1)
    print("s1 != s1", s1 != s1)
    print("s1 == s2", s1 == s2)
    print("s1 != s2", s1 != s2, "\n")

    print("isinstance(e1, Entity)", isinstance(e1, Entity))
    print("isinstance(e1, Source)", isinstance(e1, Source))
    print("isinstance(e1, type(e1) (e1: Entity)", isinstance(e1, type(e1)))
    print("isinstance(e1, type(e2) (e2: Entity)", isinstance(e1, type(e2)))
    print("isinstance(e1, type(s1) (s1: Source)", isinstance(e1, type(s1)))

    r1 = Relation(s1, "is not", "is not (INVERSE)").from_(e1).to_(e2)
    r2 = Relation(s1, "is not", "is not (INVERSE)").from_(e2).to_(e3)
    r3 = Relation(s2, "is not", "is not (INVERSE)").from_(e3).to_(e1)
    print("Testing creating a RelationalSet by individually adding items... ", end =" ")
    e_set_1 = RelationalSet().add(e1).add(e2).add(e3)
    s_set = RelationalSet().add(s1).add(s2)
    print("Worked fine!\n")

    print("Relations:")
    print("e1 - is not - e2")
    print("e2 - is not - e3")
    print("e3 - is not - e1\n")
    print("Relations in e1:", len(e1.relations), "(should be 2)")
    print("Active relations in e1:", len(e1.active_relations), "(should be 1)")
    print("Passive relations in e1:", len(e1.passive_relations), "(should be 1)")
    print("Relations in s1:", len(s1.relations), "(should be 2)")
    print("Relations in s2:", len(s2.relations), "(should be 1)\n")

    print("Testing creating a RelationalSet from a list... ", end="")
    entities = [e1, e2, e3]
    e_set_2 = RelationalSet(entities)
    print(" Worked fine!\n")

    print("Testing creating a RelationalSet by creating an empty one and adding a list... ", end="")
    e_set_3 = RelationalSet()
    e_set_3 += [e1, e2, e3]
    print(" Worked fine!\n")

    print("Testing creating a RelationalSet by creating an empty one and adding a RelationalSet... ", end="")
    e_set_4 = RelationalSet()
    e_set_4 += e_set_3
    print(" Worked fine!\n")
