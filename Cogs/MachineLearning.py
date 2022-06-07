#import tensorFlow as tf

from Backstory import get_biography
from RemoteData import champions

if __name__ == '__main__':
    champion_names = list(champions.keys())
    biographys = []
    for champion in champion_names:
        print(f'Retrieving {champion} data')
        biography = get_biography(champion)
        #biography = tf.strings.unicode_split(biography)
        biographys.append(biography)

    print(len(''.join(biographys)))
