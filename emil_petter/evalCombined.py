import pickle
from corpus import getCorpus


def getUnion(A, B):
    union = []

    overlap = None
    startFrom = 0
    for a in A:
        for i in range(startFrom, len(B)):
            b = B[i]
            if a[1] < b[0]:
                if overlap != a:
                    union.append(a)
                break
            elif a[0] <= b[1] and b[0] <= a[1]:
                union.append(U(a, b))
                overlap = a
                startFrom = i
            elif B[-1][1] < a[0]:
                union.append(a)
                break

    overlap = None
    startFrom = 0
    for b in B:
        for i in range(startFrom, len(union)):
            u = union[i]
            if b[1] < u[0]:
                if overlap != b:
                    union.append(b)
                    union.sort()
                break
            elif b[0] <= u[1] and u[0] <= b[1]:
                overlap = b
                startFrom = i
            elif union[-1][1] < b[0]:
                union.append(b)
                break

    return set(union)


def U(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


def getIntersect(A, B):
    intersect = []

    startFrom = 0
    for a in A:
        for i in range(startFrom, len(B)):
            b = B[i]
            if a[1] < b[0]:
                break
            elif a[0] <= b[1] and b[0] <= a[1]:
                intersect.append(U(a, b))
                startFrom = i

    return set(intersect)


def I(a, b):
    return (max(a[0], b[0]), min(a[1], b[1]))


def main():
    _, entities = getCorpus()

    bertMatches = pickle.load(open("out/bertMatches.out", "rb"))
    dictMatches = pickle.load(open("out/dictMatches.out", "rb"))

    union = getUnion(bertMatches, dictMatches)
    intersect = getIntersect(dictMatches, bertMatches)
    
    nEntities = len(entities)

    nTruePositive = len(union & entities)
    nPositive = len(union)

    recall = nTruePositive / nEntities
    precision = nTruePositive / nPositive
    f1 = (2*recall*precision) / (recall + precision)

    print("--Union--")
    print("Recall:\n" + str(recall))
    print("Precision:\n" + str(precision))
    print("F1-score:\n" + str(f1))

    nTruePositive = len(intersect & entities)
    nPositive = len(intersect)

    recall = nTruePositive / nEntities
    precision = nTruePositive / nPositive
    f1 = (2*recall*precision) / (recall + precision)

    print("\n--Intersect--")
    print("Recall:\n" + str(recall))
    print("Precision:\n" + str(precision))
    print("F1-score:\n" + str(f1))


if __name__ == "__main__":
    main()
