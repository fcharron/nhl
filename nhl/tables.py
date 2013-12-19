from collections import namedtuple

'''

Player Stats tables.

There are many different kinds of tables for Player Stats, the available stats is different from year to year.

In order to find the correct table, we detect the table 'signature', a string of all column namne. Based on that, we look up the correct table.  
'''
SIGNATURES = [

(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,GT,OT,S,S%,TOI/G,Sft/G,FO%', 
    namedtuple("SkaterSummary", 
        u"Number, Player, Team, Pos, GP , G, A, P, PlusMinus, PIM, PP, SH, GW, GT, OT, S, SPerc, TOI_G, Sft_G, FOPerc, ID")),

(u',Player,Team,GP,GS,W,L,T,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', 
    namedtuple("GoalieSummary",
        u"Number, Player, Team, GP, GS, W, L, T, OT, SA, GA, GAA, Sv, SvPerc, SO, G, A, PIM, TOI, ID")),

(u',Player,Team,GP,GS,W,L,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', 
    namedtuple("GoalieSummary2", 
        u"Number, Player, Team, GP, GS, W, L, OT, SA, GA, GAA, Sv, SvPerc, SO, G, A, PIM, TOI, ID")),

(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,OT,S,S%,TOI/G,Sft/G,FO%', 
    namedtuple("SkaterSummary2",
        u"Number, Player, Team, Pos, GP, G, A, P, PlusMinus, PIM, PP, SH, GW, OT, S, SPerc, TOI_G, Sft_G, FOPerc, ID")),

(u'#,Player,Team,Pos,DOB,BirthCity,S/P,Ctry,HT,Wt,S,Draft,Rnd,Ovrl,Rk,GP,G,A,Pts,+/-,PIM,TOI/G', namedtuple("SkaterBios",
    u"Number, Player, Team, Pos, DOB, BirthCity, S_P, Ctry, HT, Wt, S, Draft, Rnd, Ovrl, Rk, GP, G, A, Pts, PlusMinus, PIM, TOI_G, ID")),

(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,Sv%,SO', namedtuple("GoalieBios1", "Number,Player,Team,DOB,BirthCity,S_P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,SvPerc,SO,ID")),

(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,Sv%,SO', namedtuple("GoalieBios2","Number,Player,Team,DOB,BirthCity,S_P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,SvPerc,SO,ID"))

]