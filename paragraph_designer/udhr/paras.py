from parades import *

add_style(ParagraphOptions(stylecmd='UseParaDefault',
    fontsize='10pt', baseline='12pt plus.5pt minus.5pt',
    ))

add_style(ParagraphOptions(cmd='paracmd', env='para',
    space_above='10pt plus1pt minus1pt',
    ))

head_i = add_style(ParagraphOptions(cmd='HeadI',
    space_above='20pt', space_below='20pt',
    fontsize='12pt', baseline='14pt', fontcmd=r'\fontseries{b}\selectfont',
    afterpar='\\nobreak',
    ))

add_style(ParagraphOptions(cmd='HeadII',
    parent=head_i,
    space_above='15pt', space_below='15pt',
    fontsize='11pt', baseline='13pt',
    ))

add_style(ParagraphOptions(env='udhrlist', cmd='UseParaUdhrList',
    space_above='10pt plus1pt minus1pt',
    space_below='10pt plus1pt minus1pt',
    ))

add_style(ParagraphOptions(cmd='listitem',
    moresetup='\\interlinepenalty=150\\relax',
    space_above='8pt',
    boxes=(('0cm', '0.5cm'),), leftskip='0.5cm'))

main('paras')
