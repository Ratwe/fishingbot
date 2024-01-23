def translate_fish_name(fish_name):
    match fish_name:
        case 'cod':
            fish_name = 'треска'
        case 'salmon':
            fish_name = 'лосось'
        case 'puffer':
            fish_name = 'иглобрюх'

    return fish_name
