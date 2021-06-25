import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns # Biblioteca que permite plots mais robustos que o plt

import colorsys
import matplotlib.ticker as ticker 
from matplotlib.colors import ListedColormap, hsv_to_rgb # Bibliotecas auxiliares para conversão de cores e criação de colormaps

from collections import Counter
from langdetect import detect # Biblioteca para detecção de idiomas
from wordcloud import WordCloud

CMAP_ICEFIRE = plt.get_cmap('icefire')
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

def plot_simple_bar_elements(x, y, n_first_elements, title, xlabel='', ylabel=''):
    '''
    Função que recebe uma lista ordenada de elementos e valores, e plota um gráfico de barras dos n_first_elements 
    '''
    x = x[:n_first_elements]
    y = y[:n_first_elements]

    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    plt.bar(x, y, color=CMAP_ICEFIRE(rescale(y)))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation = 80)
    plt.ylim(min(y) - (1/100 * min(y)), max(y) + (1/100 * max(y)))
    # plt.tight_layout()
    for i, v in enumerate(y):
        plt.text(i, 
                  v, 
               f' {round(v, 2)} ', 
               rotation=90, 
               ha='center', 
               va='top' if i < 10 else 'bottom', 
               color='white' if i < 10 else 'black', 
               fontsize=12)

def plot_most_frequent_elements(count_elems, n_most_common, title, xlabel="Count"):
    '''
    Função que gera um gráfico de barras com os n_most_common elementos de um objeto Counter
    count_elemns: Objeto do tipo Counter
    title: Título do gráfico
    xlabel: Label do eixo x do gráfico
    '''

    most_common_elements = count_elems.most_common(n_most_common)
    
    # Sort the list by count; count is at second position of the tuple
    # We sort elements here so bigger elements are show on top
    most_common_elements.sort(key=lambda el: el[1])

    x = np.array([elem for elem, count in most_common_elements])
    y = np.array([count for elem, count in most_common_elements])

    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    
    plt.barh(x, y, color=CMAP_ICEFIRE(rescale(y)))
    plt.title(title)
    plt.xlabel(xlabel, fontsize=14)
    plt.xticks(rotation=80)
    for i, (elem, count) in enumerate(most_common_elements):
        plt.text(count, 
               i, 
               f' {round(count)} ', 
               rotation=0, 
               ha='left', 
               va='center', 
               color='black', 
               fontsize=12)
    plt.tight_layout() # Change the whitespace such that all labels fit nicely
    
def plot_distribution_large_data(data, title, xaxis_interval):
    '''
    Imprime um boxplot próprio para datasets grandes
    '''
    sns.set(font_scale=1.3)
    plt.figure(figsize=(16, 8))
    plt.title(title, fontsize=16)
    ax = sns.boxenplot(data=data, palette='PuBu', saturation=1, scale='area', orient='h')
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(xaxis_interval))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.setp(ax.get_xticklabels(), rotation=45);
    
def detect_language(text):
    '''
    Retorna a sigla da linguagem da string texto.
    Exemplo: detect_language("hello") = "en"
    '''
    try:
        return detect(text)
    except:
        return 'unk'
        
def make_most_common_words(words, n_most_common):
    '''
    Retorna as n_most_common palavras mais comuns da lista words
    '''
    return Counter(words).most_common(n_most_common)
    
def generate_wordcloud(dict_):
    '''
    Dado um dicionário com os elementos da word cloud e a contagem de
    de cada elemento, é retornado um objeto WordCloud usado para gerar as
    nuvens de palavras nos gráficos
    '''
    wc = WordCloud(
        background_color='white',
        colormap=CMAP_ICEFIRE,
        width=1600, 
        height=800,
        random_state=42).generate_from_frequencies(dict_)
    return wc
    
def subplot_topic_wordcloud(wc_data, nrows, ncols, width, height, title, range_stop, range_step):
    '''
    Função que plota N x M subplots de WordClouds 
    '''
    fig, ax = plt.subplots(nrows, ncols, figsize=(width, height))
    fig.suptitle(title, fontsize=20)
    
    for i in range(0, range_stop, range_step):
        i_ax = int(i*0.5)
        ax[i_ax][0].imshow(wc_data[i][0], interpolation='bilinear')
        ax[i_ax][1].imshow(wc_data[i + 1][0], interpolation='bilinear')
        
        ax[i_ax][0].axis('off')
        ax[i_ax][0].set_title('{}'.format(wc_data[i][1]), fontdict={'fontsize': 18})
        
        ax[i_ax][1].axis('off')
        ax[i_ax][1].set_title('{}'.format(wc_data[i + 1][1]), fontdict={'fontsize': 18})
        fig.tight_layout()
  
def generate_colormaps(colors_dict, n_most_common=8):
    '''
    Dado um dicionário com os valores como uma lista de cores,
    é retornado um dicionário equivalente, que substitui as cores
    originais por um ColorMap das `n_most_common` cores mais
    frequentes ordenadas da mais para a menos frequente, onde
    essa frequência também é indicada pela transparência da cor
    '''
    colormaps = {}
    for name, colors in colors_dict.items():
        colors_count = Counter(colors)
        colors_most_common = [color for color, _ in colors_count.most_common(8)]
        # colors_most_common.sort(key=lambda c: colorsys.rgb_to_hsv(c[0], c[1], c[2]))
        colors_alphas = { color: colors_count[color] / len(colors) for color in colors_most_common }
        alphas = list(colors_alphas.values())
        alphas.sort()
        second_max = alphas[-2]
        colors_with_alpha = [
            (color[0], color[1], color[2], colors_alphas[color] / second_max)
            for color in colors_most_common
        ]
        colors_with_alpha.sort(key=lambda x: -x[3])
        first_color = colors_with_alpha[0]
        colors_with_alpha[0] = (first_color[0], first_color[1], first_color[2], 1)
        # colors_with_alpha.pop(0)
        colormaps[name] = ListedColormap(np.array(colors_with_alpha), name=name)
    return colormaps

def plot_color_gradients(cmap_category, cmap_list):
    """Plota o conjunto de colormaps como barra de cores discretas"""
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.42
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(14.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)
    axs[0].set_title(cmap_category, fontsize=20)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=cmap_list[name])
        ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=15,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()
    
    plt.show()
    

def group_colors_by_genre(full_df, min_rating, valid_genres=[]):
    '''
    df = pd.DataFrame contendo as colunas `genres`, `book_rating` e `color1`
    valid_genres = Lista dos gêneros a serem considerados na criação dos agrupamentos
    
    Retorna um dicionário de cores por gêneros contidos na lista `valid_generes`
    '''
    exploded_genres = full_df.explode('genres')
    only_common_genres = exploded_genres[exploded_genres['genres'].apply(lambda x: x in valid_genres)]
    top_best = only_common_genres.groupby('genres').count()['book_title'].sort_values()[0]
    grouped_genres = only_common_genres[only_common_genres['book_rating'] > min_rating].groupby('genres')
    
    def select_and_treat_colors(df):
        colors = df.sort_values(by='book_rating')['color1'].dropna().to_list()
        treated_colors = [treat_color(c) for c in colors]
        return [c for c in treated_colors if good_color(c)]
    
    return grouped_genres.apply(select_and_treat_colors).to_dict()

def round_to(number, step=80):
    '''Arredonda um valor de acordo com um passo
    Exemplos:
    - round_to(35, 40) = 40
    - round_to(15, 40) = 0
    - round_to(45, 40) = 40
    - round_to(70, 40) = 80
    '''
    return round(number / step) * step

def treat_color(color):
    '''
    Normaliza os fatores r, g e b de uma cor
    Reduz o espectro de cores de 255^3 para 4^3 = 64
    '''
    return tuple([round_to(c) / 255 for c in color])

def is_darkest(color):
    '''Verifica se uma cor é muito escura
    Checa se a sua luminosidade é menor que 30%
    '''
    h, l, s = colorsys.rgb_to_hls(color[0], color[1], color[2])
    return l < 0.30

def is_lightest(color):
    '''Verifica se uma cor é muito clara
    Checa se a sua luminosidade é maior que 80%
    '''
    h, l, s = colorsys.rgb_to_hls(color[0], color[1], color[2])
    return l > 0.80

def good_color(color):
    '''Verifica se a cor é satisfatível para os
    propósitos desta análise. Ou seja, se não é nem
    muito clara e nem muito escura
    '''
    return not is_darkest(color) and not is_lightest(color)