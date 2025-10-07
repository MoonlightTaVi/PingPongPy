
images: dict = {}
data_folder: str = "data"


def load(filename: str) -> str:
    drawing: str
    with open(f"{data_folder}/{filename}", 'r') as f:
        drawing = f.read()
    images[filename] = drawing
    return drawing


def get_image(filename: str) -> str:
    if not filename in images:
        return load(filename)
    else:
        return images[filename]


def draw(filename: str):
    drawing: str = get_image(filename)
    print(drawing)
