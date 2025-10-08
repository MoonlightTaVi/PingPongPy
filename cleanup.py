import shutil
import os


def delete_dir(path: str):
    try:
        shutil.rmtree(path)
        print(f"Directory '{path}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")

def delete_file(path: str):
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"File '{path}' deleted successfully.")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
    else:
        print(f"File '{path}' does not exist.")


directories: list = [
    "./dist",
    "./build"
]
files: list = ["main.spec"]


if __name__ == "__main__":
    for dir in directories:
        delete_dir(dir)
    for file in files:
        delete_file(file)

    print("Clean-up finished.")
    input("Press any key to quit...")