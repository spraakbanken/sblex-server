from sblex.trie.trie import TrieBuilder


def test_trie():
    trie_builder = TrieBuilder()
    trie_builder.insert("ösja", b"{head:osja,pos:vb}")
    trie_builder.insert("örliga", b"{head:orliga,pos:vb}")
    print(f"{trie_builder.trie=}")
    trie = trie_builder.build()
    print(f"{trie._trie=}")
    # assert False
