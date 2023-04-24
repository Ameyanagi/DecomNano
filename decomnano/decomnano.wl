(* ::Package:: *)

L = Compile[{{D,_Real}, {R, _Real}}, Module[{}, D/2/R]]
n = Compile[{{D,_Real}, {R, _Real}}, Module[{}, 6 * L[D, R] * (20 * L[D, R] ^ 2 + 15 * L[D, R] + 7) 
        / (10 * L[D, R] ^ 3 + 15 * L[D, R] ^ 2 + 11 * L[D, R] + 3)]]
Natom = Compile[{{D,_Real}, {R, _Real}}, Module[{}, (10 * L[D, R] ^ 3 + 15 * L[D, R] ^ 2 + 11 * L[D,
         R] + 3) / 3]]

DecomNano[RPt_, RAu_, fAu_, nAuAu_, nPtPt_, nAuPt_, nPtAu_, DA_, DAP_, DP_] := 
     Module[
    {RAP, nMMAuPtNP, nAuAuAuNP, nPtPtPtNP, NAu, NPt,
         NAuPt, eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, cons1, cons2,
         cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10, NAuMAuPt, NPtMAuPt,
         NAuAuAuPt, NAuPtAuPt, NPtAuAuPt, NPtPtAuPt, XAP, XA, XP,y}
    ,
    (*Definitions of Distance and particlesize*)
    RAP = fAu * RAu + (1 - fAu) * RPt;
    (* This the prameters from experiment. It has some uncertancies.*)
        
    (* Number of bonds in AuPtNP*)
    nMMAuPtNP = n[DAP, RAP];
    nAuAuAuNP = n[DA, RAu];
    nPtPtPtNP = n[DP, RPt];
    (*Number of atoms of Au nanoparticle*)
    NAu = Natom[DA, RAu];
    (*Number of atoms of Pt nanoparticle*)
    NPt = Natom[DP, RPt];
    (*Number of atoms of AuPt nanoparticle*)
    NAuPt = Natom[DAP, RAP];
    eq1 = nMMAuPtNP == y * NAuMAuPt + (1 - y) * NPtMAuPt;
    eq2 = NAuMAuPt == NAuAuAuPt + NAuPtAuPt;
    eq3 = NPtMAuPt == NPtAuAuPt + NPtPtAuPt;
    eq4 = nAuAu == NAuAuAuPt * (XAP / (XA + XAP)) + nAuAuAuNP * (XA 
        / (XA + XAP));
    eq5 = nPtPt == NPtPtAuPt * (XAP / (XP + XAP)) + nPtPtPtNP * (XP 
        / (XP + XAP));
    eq6 = nAuPt == NAuPtAuPt * (XAP / (XA + XAP));
    eq7 = nPtAu == NPtAuAuPt * (XAP / (XP + XAP));
    eq8 = (XA + XAP + XP == 1);
    eq9 = ((XP * NPt + XAP * NAuPt * (1 - y)) == nAuPt / nPtAu *(XA * NAu + XAP * NAuPt * y));
    eq10 = y == NPtAuAuPt / (NPtAuAuPt + NAuPtAuPt);
    cons1 = 0 <= y <= 1;
    cons2 = 0 <= XAP <= 1;
    cons3 = 0 <= XA <= 1;
    cons4 = 0 <= XP <= 1;
    cons5 = 0 <= NAuMAuPt <= 12;
    cons6 = 0 <= NPtMAuPt <= 12;
    cons7 = 0 <= NAuAuAuPt <= 12;
    cons8 = 0 <= NAuPtAuPt <= 12;
    cons9 = 0 <= NPtAuAuPt <= 12;
    cons10 = 0 <= NPtPtAuPt <= 12;
    sol = NSolve[{eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, cons1,
         cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10}, {NAuMAuPt,
         NPtMAuPt, NAuAuAuPt, NAuPtAuPt, NPtAuAuPt, NPtPtAuPt, XAP, XA, XP, y
        }, Reals];
        
   If[Length[sol]>0,{RPt, RAu, fAu, nAuAu, nPtPt, nAuPt, nPtAu, DA, DAP, DP, NAuMAuPt,
         NPtMAuPt, NAuAuAuPt, NAuPtAuPt, NPtAuAuPt, NPtPtAuPt, XAP, XA, XP, y}/.sol, {{RPt, RAu, fAu, nAuAu, nPtPt, nAuPt, nPtAu, DA, DAP, DP,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null}}]
]
