#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


@pytest.mark.sphinx('review')
def test_basic(app, status, warning):
    app.builder.build_all()

#    import pdb; pdb.set_trace()

    re = (app.outdir / 'basic.re').text()

    expected = [
        u'={section-1} section 1',
        u'=={section-2} section 2',
        u'==={section-3} section 3',
        u'==={section-4-0} section 4.0',
        u'===={section-5} section 5',
        u'==={section-4-1} section 4.1',
    ]
    for e in expected:
        assert e in re

    expected = [
        u'@<i>{強調}',
        u'@<b>{強い強調}',
        u'数式@<m>{a^2 + b^2 = c^2}です',
        u'@<href>{https://github.com/kmuto/review/blob/master/doc/format.rdoc,フォーマット}',
        u'@<href>{https://github.com/kmuto/review/blob/master/doc/format.rdoc}',
        u'ここは@<fn>{f1}脚注@<fn>{f2}',
        u'//footnote[f2][脚注2は@<i>{インライン}@<b>{要素}を@<href>{https://github.com/kmuto/review,含みます}]',
        u'#@# コメントです',
        u'#@# コメントブロック1\n#@# コメントブロック2',
        u'//raw[|html|<hr width=50 size=10>]',
        u'@<u>{下線}を引きます',
        u'索引@<hidx>{インデックス}インデックスを作ります',  # TODO: インデックス文字が入っている
        u'numref:@<chap>{section-1},@<chap>{section-2},@<chap>{section-3}',
    ]
    print(re)
    for e in expected:
        assert e in re


@pytest.mark.sphinx('review')
def test_code(app, status, warning):
    app.builder.build_all()

    re = (app.outdir / 'code.re').text()

    # list
    expected = (u'//list[なにもなしname][][c]{')
    assert expected in re
    expected = (u'//listnum[行番号付きname][][ruby]{')
    assert expected in re

    # TODO: captionとnameを併用できない？
    #    expected = ('//list[キャプション付きname][キャプション][c]{')
    #    assert expected in re
    #    expected = ('//listnum[行番号付きキャプション付きname][行番号付きキャプション][ruby]{')
    #    assert expected in re

    # em
    expected = [
        u'//emlist[][c]{',
        u'//emlist[][c]{',
        u'//emlist[emcaption][c]{',
        u'//emlistnum[][ruby]{',
        ]
    for e in expected:
        assert e in re

    # firstlinenum
    expected = (u'//firstlinenum[100]')
    assert expected in re

    # codeinline
    expected = (u'@<code>{p = obj.ref_cnt}')
    assert expected in re

    # cmd
    expected = (u'//cmd{\n$ cd /\n$ sudo rm -rf /\n//}')
    assert expected in re

    # reference
    expected = (u' * numref:@<list>{なにもなしname}\n')
    assert expected in re


@pytest.mark.sphinx('review')
def test_admonition(app, status, warning):
    app.builder.build_all()

    re = (app.outdir / 'admonition.re').text()

    expected = [
        u'//tip[tipキャプション]{',
        u'//note[noteキャプション]{',
        u'//caution[dangerキャプション]{',
        u'//info[hintキャプション]{',
        u'//warning[warningキャプション]{',
        u'//warning{',
        u'//quote{\n百聞は一見にしかず\n//}',
    ]

    for e in expected:
        assert e in re


@pytest.mark.sphinx('review')
def test_list(app, status, warning):
    app.builder.build_all()

    re = (app.outdir / 'list.re').text()

    expected = [
        u' * 第3の項目\n\nLorem ipsum dolor sit amet,\n',
        u' 3. 第3の条件\n\nLorem ipsum dolor sit amet,\n',
        u' : 第1の項目\n   第1の項目の説明\n\n',
        u' : 第2の項目\n   第2の項目の説明@<br>{}\n   第2の項目のさらなる説明\n\n',
        u' : 第3の項目\n   第3の項目の説明@<br>{}\n   第3の項目のさらなる説明\n\n//cmd',
        u'//}\n\n : 第4の項目\n'
    ]

    for e in expected:
        assert e in re


@pytest.mark.sphinx('review')
def test_table(app, status, warning):
    app.builder.build_all()

    re = (app.outdir / 'table.re').text()

    expected = [
        u'//table[compact-label][]{\nA\tnot A\n------------\nFalse\tTrue\nTrue\tFalse\n//}',
        u'//table[tablename][Frozen Delights!]{\nTreat\tQuantity\tDescription',
        (u'//table[multiple-paragraph][]{\nA\tnot A\n------------\nLorem ipsum@<br>{}@<br>{}dolor sit amet,\t'
         u'consectetur adipiscing elit,\n//}'),
    ]

    for e in expected:
        assert e in re

    # reference
    expected = (u' * numref:@<table>{compact-label}\n')
    assert expected in re


@pytest.mark.sphinx('review')
def test_figure(app, status, warning):
    app.builder.build_all()

    re = (app.outdir / 'figure.re').text()

    expected = [
        u'//image[picture][ここはfigureのキャプションです。]{',
        u'//image[picture][]{',
    ]

    for e in expected:
        assert e in re

    # reference
    expected = (u' * numref:@<img>{picture}\n')
    assert expected in re


@pytest.mark.sphinx('review')
def test_reference(app, status, warning):
    app.builder.build_all()

    re = (app.outdir / 'ref.re').text()

    expected = [
        u'numfig@<img>{figure|picture}です',
        u'numfig@<table>{table|compact-label}です',
        u'numfig@<list>{code|なにもなしname}です',
        u'numfig@<chap>{basic|section-1}です',
        u'numfig@<chap>{basic|section-2}です',
    ]

    for e in expected:
        assert e in re
