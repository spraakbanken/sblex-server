from sblex import formatting


def test_lexeme_formatting():
    j = {
        "h1": "bo",
        "depth": 2,
        "fm": ["leva..1"],
        "fp": ["PRIM..1"],
        "lem": {"bo..vb.1"},
        "lex": "bo..1",
        "l": ["bo..vb.1"],
        "mf": [
            "bebo..1",
            "bo..2",
            "boende..1",
            "bol..1",
            "boning..1",
            "bosatt..1",
            "bostad..1",
            "boställe..1",
            "bosätta_sig..1",
            "dväljas..1",
            "enstöring..1",
            "eremit..1",
            "fastboende..1",
            "flytta..2",
            "hem..1",
            "hemmaboende..1",
            "hotell..1",
            "husvagn..1",
            "huvudkvarter..1",
            "hydda..1",
            "hyresgäst..1",
            "hysa..2",
            "häcka..1",
            "härbärge..1",
            "invånare..1",
            "kampera..1",
            "närboende..1",
            "obebodd..1",
            "obeboelig..1",
            "pensionat..1",
            "samboende..1",
            "samboende..2",
            "sammanbo..1",
            "slott..1",
            "slum..1",
            "sommarboende..1",
            "stödboende..1",
            "tak_över_huvudet..1",
            "trångbodd..1",
            "tält..1",
            "vinterkvarter..1",
            "värdshus..1",
            "åretruntboende..1",
        ],
        "pf": [
            "backstugusittare..1",
            "bofast..1",
            "boningshus..1",
            "boningsplats..1",
            "boningsrum..1",
            "boplats..1",
            "bybo..1",
            "fastlandsbo..1",
            "födoråd..1",
            "förortsbo..1",
            "församlingsbo..1",
            "glesbygdsbo..1",
            "grottinvånare..1",
            "gränsbo..1",
            "gårdsfolk..1",
            "husbil..1",
            "husbåt..1",
            "husmansfolk..1",
            "internat..1",
            "internatskola..1",
            "jordbo..1",
            "kustbo..1",
            "landsbo..1",
            "landsbygdsbo..1",
            "lantbo..1",
            "mambo..2",
            "nordbo..1",
            "ort..1",
            "ortsbo..1",
            "sambo..1",
            "samhälle..2",
            "skärgårdsbo..1",
            "småstadsbo..1",
            "sockenbo..1",
            "stad..1",
            "stadsbo..1",
            "storstadsbo..1",
            "tätortsbo..1",
            "utbo..1",
            "öbo..1",
        ],
        "sorted_mf": [
            (
                "PRIM..1",
                [
                    "bebo..1",
                    "boende..1",
                    "bol..1",
                    "boning..1",
                    "bosatt..1",
                    "bostad..1",
                    "boställe..1",
                    "bosätta_sig..1",
                    "dväljas..1",
                    "hem..1",
                    "hydda..1",
                    "invånare..1",
                    "tak_över_huvudet..1",
                    "tält..1",
                ],
            ),
            ("annanstans..1", ["flytta..2"]),
            ("djur..1", ["bo..2"]),
            ("ensam..1", ["enstöring..1", "eremit..1"]),
            ("fast..1", ["fastboende..1"]),
            ("fattig..1", ["slum..1"]),
            ("främst..1", ["huvudkvarter..1"]),
            ("fågel..1", ["häcka..1"]),
            ("gäst..1", ["hotell..1", "härbärge..1", "pensionat..1", "värdshus..1"]),
            ("hemma..1", ["hemmaboende..1"]),
            ("hyra..1", ["hyresgäst..1"]),
            ("inte..1", ["obebodd..1"]),
            ("nära..1", ["närboende..1"]),
            ("omöjlig..1", ["obeboelig..1"]),
            ("samman..1", ["samboende..1", "samboende..2"]),
            ("sommar..1", ["sommarboende..1"]),
            ("stor..1", ["slott..1"]),
            ("stöd..1", ["stödboende..1"]),
            ("tillfällig..1", ["hysa..2", "kampera..1"]),
            ("tillsammans..1", ["sammanbo..1"]),
            ("trång..1", ["trångbodd..1"]),
            ("vinter..1", ["vinterkvarter..1"]),
            ("åka..1", ["husvagn..1"]),
            ("året_runt..1", ["åretruntboende..1"]),
        ],
        "sorted_pf": [
            ("Norden..1", ["nordbo..1"]),
            ("annanstans..1", ["utbo..1"]),
            ("backstuga..1", ["backstugusittare..1"]),
            ("bil..1", ["husbil..1"]),
            ("by..1", ["bybo..1"]),
            ("båt..1", ["husbåt..1"]),
            ("fast..1", ["bofast..1"]),
            ("fastland..1", ["fastlandsbo..1"]),
            ("förort..1", ["förortsbo..1"]),
            ("församling..1", ["församlingsbo..1"]),
            ("förälder..1", ["mambo..2"]),
            ("glesbygd..1", ["glesbygdsbo..1"]),
            ("grotta..1", ["grottinvånare..1"]),
            ("gräns..1", ["gränsbo..1"]),
            ("gård..1", ["gårdsfolk..1", "husmansfolk..1"]),
            ("hus..1", ["boningshus..1"]),
            ("jorden..1", ["jordbo..1"]),
            ("kust..1", ["kustbo..1"]),
            ("land..3", ["landsbo..1", "lantbo..1"]),
            ("landsbygd..1", ["landsbygdsbo..1"]),
            ("ort..1", ["ortsbo..1"]),
            (
                "plats..1",
                ["boningsplats..1", "boplats..1", "ort..1", "samhälle..2", "stad..1"],
            ),
            ("rum..1", ["boningsrum..1"]),
            ("rättighet..1", ["födoråd..1"]),
            ("skola..1", ["internat..1", "internatskola..1"]),
            ("skärgård..1", ["skärgårdsbo..1"]),
            ("småstad..1", ["småstadsbo..1"]),
            ("socken..1", ["sockenbo..1"]),
            ("stad..1", ["stadsbo..1"]),
            ("storstad..1", ["storstadsbo..1"]),
            ("tillsammans..1", ["sambo..1"]),
            ("tätort..1", ["tätortsbo..1"]),
            ("ö..2", ["öbo..1"]),
        ],
        # "lexeme": Lexeme("bo..1"),
    }

    fm = lexeme_ref(j["fm"])
    assert (
        fm
        == '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/leva..1">leva</a>'
    )
    # assert sort_children(j["sorted_mf"][1:2]) == "<table>"


def lexeme_ref(lids) -> str:
    print(f"{lids=} ({type(lids)})")
    if lids == "":
        return "*"
    return "+".join(
        [
            '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/'
            + lid
            + '">'
            + formatting.prlex(lid)
            + "</a>"
            for lid in lids  # .split()
        ]
    )


def sort_children(xss) -> str:
    s = "<table>"

    for p, xs in xss:
        s += (
            '<tr><td style="vertical-align:middle;">'
            + formatting.prlex(p)
            + ' </td><td style="vertical-align:middle;">'
            + (" ".join([lexeme_ref(x) for x in xs]))
            + "</td></tr>"
        )
    s += "</table>"
    return s
