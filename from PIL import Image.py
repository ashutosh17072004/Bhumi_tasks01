from PIL import Image

def logistic_map(x, a=4):
    return a * x * (1 - x)

def encrypt(image_path, key):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    # Transform the image into a one-dimensional sequence
    pixel_sequence = [pixels[x, y] for y in range(height) for x in range(width)]

    # Generate a random sequence based on the logistic map
    x = key / 256
    random_sequence = [logistic_map(x) for _ in range(len(pixel_sequence))]

    # Apply the random sequence to the pixel sequence
    encrypted_pixel_sequence = [int(min(255, max(0, p + r))) for p, r in zip(pixel_sequence, random_sequence)]

    # Convert the encrypted pixel sequence back to an image
    encrypted_image = Image.new("RGB", (width, height))
    encrypted_pixels = encrypted_image.load()
    for y in range(height):
        for x in range(width):
            encrypted_pixels[x, y] = encrypted_pixel_sequence[x + y * width]

    return encrypted_image

def decrypt(encrypted_image_path, key):
    encrypted_image = Image.open(encrypted_image_path)
    pixels = encrypted_image.load()
    width, height = encrypted_image.size

    # Transform the image into a one-dimensional sequence
    pixel_sequence = [pixels[x, y] for y in range(height) for x in range(width)]

    # Generate a random sequence based on the logistic map
    x = key / 256
    random_sequence = [logistic_map(x) for _ in range(len(pixel_sequence))]

    # Apply the inverse of the random sequence to the pixel sequence
    original_pixel_sequence = [int(min(255, max(0, p - r))) for p, r in zip(pixel_sequence, random_sequence)]

    # Convert the original pixel sequence back to an image
    original_image = Image.new("RGB", (width, height))
    original_pixels = original_image.load()
    for y in range(height):
        for x in range(width):
            original_pixels[x, y] = original_pixel_sequence[x + y * width]

    return original_image