# Natural languagle processing ops.

Main module functions:
- compare input texts with the correct ones.
- evaluate users answer quality and provide tips if it's needed.

## Models are used
#### fastText
```
curl https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz \
      --output ./language_models/english_orig.bin.gz

curl https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.fr.300.bin.gz \
      --output ./language_models/french_orig.bin.gz

curl https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ru.300.bin.gz \
      --output ./language_models/russian_orig.bin.gz

curl https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.uk.300.bin.gz \
      --output ./language_models/ukrainian_orig.bin.gz
```

***
## Reduce original models using commands example
Dimensionality reduction :
```
python3 utils/reduce_dim_ft.py \
        --model_path language_models/french_orig.bin \
        --new_model_path language_models/french.bin \
        --to_size 8
```

Weights and hash-map pruning:
```
python3 utils/pruning_ft.py \
        --model_path=./language_models/ukrainian_orig.bin \
        --new_model_path=./language_models/ukrainian_pruned.bin
```
