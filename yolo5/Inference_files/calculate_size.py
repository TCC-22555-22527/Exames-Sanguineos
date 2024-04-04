
def calculate_size_in_micrometers(pixel_width, pixel_height):
    # Adapte esse método conforme a relação pixel-micrômetro na sua aplicação
    pixel_to_micrometer_ratio = 0.1  # Exemplo: 1 pixel = 0.1 micrômetro
    size_micrometers_width = pixel_width * pixel_to_micrometer_ratio
    size_micrometers_height = pixel_height * pixel_to_micrometer_ratio

    # Retorna a média dos tamanhos em micrômetros (pode ajustar conforme sua necessidade) # noqa: E501
    return (size_micrometers_width + size_micrometers_height) / 2
