from jutility import util

def get_word_list(path: str, url: str) -> list[str]:
    word_list_str = util.load_or_download(path, url)
    word_list = [
        s.split()[0].lower()
        for s in word_list_str.strip().split("\n")
    ]
    return word_list

wl_1 = get_word_list(
    "data/google_20k_words.txt",
    (
        "https://raw.githubusercontent.com/first20hours/google-10000-english"
        "/refs/heads/master/20k.txt"
    ),
)
wl_2 = get_word_list(
    "data/NWL2023.txt",
    (
        "https://raw.githubusercontent.com/scrabblewords/scrabblewords/"
        "main/words/North-American/NWL2023.txt"
    ),
)
wl_3 = get_word_list(
    "data/mit_10k.txt",
    (
        "https://www.mit.edu/~ecprice/wordlist.10000"
    ),
)
word_set = set(wl_1).intersection(wl_2).intersection(wl_3)
word_list = sorted(word_set)

prefix_dict = dict()
for s in word_list:
    s_prefixes = []
    for i in range(3, len(s)+1):
        prefix = s[:i]
        if prefix in word_set:
            s_prefixes.append(prefix)

    prefix_dict[s] = s_prefixes

max_num_prefixes = max(len(v) for v in prefix_dict.values())
argmax_num_prefixes = [
    k for k, v in prefix_dict.items()
    if len(v) == max_num_prefixes
]

print(len(word_list))
print(max_num_prefixes)

threshold = 5
for np in range(3, max_num_prefixes + 1):
    util.hline()
    np_list = [
        k for k, v in prefix_dict.items()
        if len(v) == np
    ]
    for a in np_list:
        print(len(prefix_dict[a]), a, prefix_dict[a])

util.hline()
