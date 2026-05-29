import argparse
import pathlib

import fasttext


def train(data_path: str, output_path: str, lr: float, epoch: int, word_ngrams: int) -> None:
    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    model = fasttext.train_supervised(
        input=data_path,
        lr=lr,
        epoch=epoch,
        wordNgrams=word_ngrams,
        loss="softmax",
        dim=50,
    )
    model.save_model(output_path)

    result = model.test(data_path)
    print(f"Samples: {result[0]}")
    print(f"Precision: {result[1]:.4f}")
    print(f"Recall: {result[2]:.4f}")
    print(f"Model saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train fastText goodnight detector")
    parser.add_argument("--data", default="data/train.txt", help="Path to training data")
    parser.add_argument("--output", default="model/goodnight.bin", help="Output model path")
    parser.add_argument("--lr", type=float, default=0.5, help="Learning rate")
    parser.add_argument("--epoch", type=int, default=100, help="Number of epochs")
    parser.add_argument("--word-ngrams", type=int, default=2, help="Word n-grams")
    args = parser.parse_args()
    train(args.data, args.output, args.lr, args.epoch, args.word_ngrams)


if __name__ == "__main__":
    main()