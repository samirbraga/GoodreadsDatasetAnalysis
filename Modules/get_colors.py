from colorthief import ColorThief
import json
from multiprocessing import Pool

# Caminho base para o diretório de imagens
IMAGES_PATH = "./images/"
# Número total de imagens
NUM_IMAGES = 54301
# Número de cores da máquina. Utilizada para o paralelismo do processamento.
NUM_CORES = 6

images = [(i, "%d.jpg" % i) for i in range(NUM_IMAGES)]

def chunks(lst, n):
    """Divide uma lista em n sublistas, tals que união de todas as subslistas resulta na lista original"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_image_color(path):
    """Retorna a cor mais predominante de uma imagem em RGB"""
    return [ColorThief(path).get_color(quality=50)]

def get_images_colors(images):
    """Dada a lista de nomes das imagens, retorna um dicionário no formato `{ index: color }`.
    Sendo `color` a cor mais predominante das imagens.
    """
    images_colors = {}
    for image_index, image_name in images:
        try:
            images_colors[image_index] = get_image_color(IMAGES_PATH + image_name)
        except:
            print("image not found: ", image_name)
    return images_colors

if __name__ == '__main__':
    images_chunks = list(chunks(images, NUM_CORES))

    # Executa o processamento em um Thread pool
    pool = Pool(NUM_CORES)
    images_colors_list = pool.map(get_images_colors, images_chunks)
    all_images_colors = {}

    for images_colors in images_colors_list:
        all_images_colors.update(images_colors)

    pool.close()
    pool.join()

    # Guarda o processamento em um arquivo .json
    with open('dominant_colors.json', 'w') as f:
        json.dump(all_images_colors, f)