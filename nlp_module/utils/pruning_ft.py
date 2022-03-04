import compress_fasttext
from argparse import ArgumentParser
from gensim.models.fasttext import load_facebook_model

# fasttext v0.9.2
# https://gist.github.com/AlexKay28/fb0dd8a3db8a3e6e4f2c880c83c296a5


def prune(model_path, new_model_path):
    """
    Сombination of feature selection and quantization
    """
    big_model = load_facebook_model(model_path).wv

    small_model = compress_fasttext.prune_ft_freq(
        big_model,
        new_vocab_size=100_000,
        new_ngrams_size=300_000,
        fp16=True,
        pq=True,
        qdim=300,
        centroids=255,
        prune_by_norm=True,
        norm_power=1,
    )
    small_model.save(new_model_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model_path", type=str)
    parser.add_argument("--new_model_path", default=None, type=str)

    args = parser.parse_args()
    prune(args.model_path, args.new_model_path)
