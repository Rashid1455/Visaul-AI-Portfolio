"""Contact details and descriptive labels for the existing collection."""

CONTACT_EMAIL = "Rashidhussain473888@gmail.com"

IMAGE_TITLES = {
    "attention.png": "Attention, by design",
    "cdcddcdcdc.png": "Systems built for growth",
    "cddddd.png": "The cost of bad marketing",
    "design changes what people see.png": "Design shapes perception",
    "me .png": "Color and contrast — studio portrait",
    "me.png": "Color and contrast — studio portrait",
    "me12.png": "A world within — double exposure",
    "my image.png": "Create with purpose",
    "new look.jpg": "Monochrome portrait study",
    "Rashid Ali Soomro.png": "Small people, big dreams",
    "Rashid Ali.png": "Creative founder",
    "Rashid style picture.png": "Portrait on parchment",
}


def media_title(path, index, kind):
    if path.name in IMAGE_TITLES:
        return IMAGE_TITLES[path.name]
    if path.name.startswith("Sneaker_commercial"):
        return "Sneaker commercial — motion concept"
    if path.name.startswith("Giant_and_miniature"):
        return "Giant and miniature — motion concept"
    if "cubify" in path.name.lower():
        return f"Cubify Digital — motion study {index + 1:02d}"
    return f"{kind} study / {index + 1:02d}"
