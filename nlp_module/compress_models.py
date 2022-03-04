import os

_MODELS_PATH = "./language_models"


def main(prune: bool = False, reduce: bool = True, new_size: int = 8):
    format = ".bin"
    model_names = [
        name.split(".")[0] for name in os.listdir(_MODELS_PATH) if name.endswith(format)
    ]
    for model_name in model_names:
        print(f"Compressing: {model_name}")
        path = os.path.join(_MODELS_PATH, model_name)

        if prune:
            print(f"-> Pruning <{model_name}>")
            cmd = (
                f"python ./utils/pruning_ft.py "
                f"--model_path={path}{format} "
                f"--new_model_path={path}{format}"
            )
            os.system(cmd)

        if reduce:
            print(f"-> Reducing <{model_name}>")
            cmd = (
                f"python ./utils/reduce_dim_ft.py "
                f"--to_size={new_size} "
                f"--model_path={path}{format} "
                f"--new_model_path={path}{new_size}{format}"
            )
            os.system(cmd)


if __name__ == "__main__":
    main()
