import urllib
import string
import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords

def mapping(data):

    map_list=[]

    for label in data:

        if len(data[label]) == 1:

            for word in data[label][0].split():

                map_list.append((word,label))

        else:

            for word in data[label]:

                map_list.append((word,label))

    return map_list

def reduce(map_list):

    reduce_dict = {}

    for pair in map_list:

        if pair[0] not in reduce_dict.keys():

            reduce_dict[pair[0]] = [pair[1]]

        if pair[1] in reduce_dict[pair[0]]:

            continue

        else:
            reduce_dict[pair[0]].append(pair[1])

    return reduce_dict

def load_clean(link, split_word):

    file_open = urllib.request.urlopen(link)

    text = file_open.read()

    text = text.decode("utf-8")

    # Remove preamble
    text = text.partition(split_word)[2]

    text = text.split()

    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    text_no_spec_char = [w.translate(table) for w in text]

    # convert to lower case
    text_no_spec_char_lower = [word.lower() for word in text_no_spec_char]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    text_no_stop = [w for w in text_no_spec_char_lower if not w in stop_words]

    return text_no_stop

rj_link = "https://www.gutenberg.org/files/1112/1112.txt"
kl_link = "http://www.gutenberg.org/cache/epub/1128/pg1128.txt"
mb_link = "http://www.gutenberg.org/cache/epub/2264/pg2264.txt"

spl_word_rj = "Verona. A public place."
spl_word_kl = "[King Lear's Palace.]"
spl_word_mb = "Actus Primus. Scoena Prima."

rj = load_clean(rj_link, spl_word_rj)
kl = load_clean(kl_link, spl_word_kl)
mb = load_clean(mb_link, spl_word_mb)

shakespeare_dict = {rj_link: rj,
                    kl_link: kl,
                    mb_link: mb}

map_result = mapping(shakespeare_dict)
reduce_result = reduce(map_result)

print(reduce_result)
