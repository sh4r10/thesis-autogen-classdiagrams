# The use of Large Language Models in the reverse engineering of Class Diagrams

## Table of Contents
- [The Thesis](https://github.com/sh4r10/thesis-autogen-classdiagrams/blob/main/submissions/thesis%20submission.pdf)
- [Scripts used for comparison](https://github.com/sh4r10/thesis-autogen-classdiagrams/tree/main/artefacts/scripts)
- [Example outputs from scripts](#example-outputs-from-scripts)

## Example outputs from scripts

### compare.py
Used for comparing two PlantUML files, used for data collection when comparing GPT diagrams with human ones.
```
{
    major: {
        tp: 5,
        fp: 6,
        fn: 6,
        precision: 0.45454545454545453,
        recall: 0.45454545454545453,
        f1: 0.45454545454545453
    },
    moderate: {
        tp: 41,
        fp: 25,
        fn: 2,
        precision: 0.6212121212121212,
        recall: 0.9534883720930233,
        f1: 0.7522935779816513
    },
    minor: {
        tp: 88,
        fp: 50,
        fn: 7,
        precision: 0.6376811594202898,
        recall: 0.9263157894736842,
        f1: 0.7553648068669527
    }
}
```

### compile_stats.py
Used for compiling statistics about a collection of diagrams, such as mean precision, recall, f1 scores as well as the comparison score for each.
```
{
major: {
    mean: 0.512020202020202,
    standard deviation: 0.250339823626073,
    variance: 0.06267002729313334
},
moderate: {
    mean: 0.7629188680564828,
    standard deviation: 0.02598095674177416,
    variance: 0.0006750101132179401
},
minor: {
    mean: 0.7334813649648696,
    standard deviation: 0.0954202853417595,
    variance: 0.009105030854702803
}
{
    t1-no-haf.stat: 14.719364787568667,
    t2-no-haf.stat: 14.565605436402057,
    t3-no-haf.stat: 15.877292274318533,
    t4-no-haf.stat: 9.221938775510203,
    t5-no-haf.stat: 14.79587857732847
}
```

### mann.py
Used for performing the Mann-Whitney U-test on a given collection of files. 
```
MannwhitneyuResult(statistic=12.5, pvalue=0.54)
Vargha-Delaney A12: 0.50
```
