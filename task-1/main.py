import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread


parser = argparse.ArgumentParser(description="Process files in folder.")


parser.add_argument("--source", metavar="-s", help="source folder")
parser.add_argument("--output", metavar="-o", default="dist", help="output folder")


args = vars(parser.parse_args())
source_folder = Path(args.get("source"))
output_folder = Path(args.get("output"))


folders = []


def folder_reader(path: Path) -> None:
    logging.info(f"Start reading {path}")

    for element in path.iterdir():
        if element.is_dir():
            folders.append(element)
            folder_reader(element)


def file_mover(path: Path) -> None:
    for element in path.iterdir():
        if element.is_file():
            extension = element.suffix[1:]
            new_folder = output_folder / extension

            try:
                new_folder.mkdir(parents=True, exist_ok=True)
                copyfile(element, new_folder / element.name)
            except OSError as error:
                logging.error(error)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: %(processName)s, %(threadName)s - %(message)s",
    )

    folders.append(source_folder)
    folder_reader(source_folder)

    threads = []

    for folder in folders:
        thread = Thread(target=file_mover, args=(folder,))
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]

    logging.info(f"Finishing reading folder {source_folder}. All files are sorted.")
