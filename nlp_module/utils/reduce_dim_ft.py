import os
import fasttext
import fasttext.util
from argparse import ArgumentParser

# fasttext v0.9.2
# https://gist.github.com/AlexKay28/1f48b00ea355c06c68bcda3b9df1355b


def reduce(model_path, to_size, new_model_path):
    """
    Reduce vectors size in fasttext model
    """
    model = fasttext.load_model(model_path)
    vec_size = model.get_dimension()
    if vec_size < to_size:
        raise ValueError(
            f"Cant reduce from {vec_size} to {to_size}",
        )
    if vec_size == to_size:
        print("Reducing is not needed!")
        return
    fasttext.util.reduce_model(model, to_size)
    model.save_model(new_model_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model_path", type=str)
    parser.add_argument("--to_size", type=int)
    parser.add_argument("--new_model_path", default=None, type=str)

    args = parser.parse_args()
    reduce(args.model_path, args.to_size, args.new_model_path)
