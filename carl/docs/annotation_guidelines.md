# Guidelines for annotation

## Continuity

All instances where a NE has the same function must be labled in the same manner.

* E.g. negations should be categorized as such not only at symptoms but across the document.

## Named Entities used in project
* SYM
* NEG

See [named_entities.csv](named_entities.csv) for definitions

### Example useage & common problems

*Status: AT: opåverkat i vila*
"påverkad i vila" = SYM
"o" = NEG

Here transforming all "opåverkad" to "ej påverkad" helps with automatically tagging the negations usings string matchers.

## Annotation problems

: definition
