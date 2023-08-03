(* ::Package:: *)

L = Compile[{{D,_Real}, {d, _Real}}, Module[{}, D/2/d]]
n = Compile[{{D,_Real}, {d, _Real}}, Module[{}, 6 * L[D, d] * (20 * L[D, d] ^ 2 + 15 * L[D, d] + 7) 
        / (10 * L[D, d] ^ 3 + 15 * L[D, d] ^ 2 + 11 * L[D, d] + 3)]]
Natom = Compile[{{D,_Real}, {d, _Real}}, Module[{}, (10 * L[D, d] ^ 3 + 15 * L[D, d] ^ 2 + 11 * L[D,
         d] + 3) / 3]]

nh = Compile[{{D, _Real}, {Dh, _Real}, {d, _Real}}, 
  Module[{}, 
   24*(L[D, d]*(5*L[D, d]^2 + 3*L[D, d] + 1) - (15*L[Dh, d]^3 + 
         18*L[Dh, d]^2 + 12*L[Dh, d] + 3))/(10*L[D, d]^3 + 
       15*L[D, d]^2 + 11*L[D, d] - 10*L[Dh, d]^3 + 15*L[Dh, d]^2 + 
       11*L[Dh, d])]]

Natomh = 
 Compile[{{D, _Real}, {Dh, _Real}, {d, _Real}}, 
  Module[{}, Natom[D, d] - Natom[Dh, d]]]

DecomNano[dP_, dA_, fA_, nAuAu_, nPtPt_, nAuPt_, nPtAu_, DA_, DAP_, DP_] := 
     Module[
    {dAP, nMMAP, nAAA, nPPP, NA, NP,
         NAP, eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, cons1, cons2,
         cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10, nAMAP, nPMAP,
         nAAAP, nAPAP, nPAAP, nPPAP, XAP, XA, XP,y}
    ,
    (*Definitions of Distance and particlesize*)
    dAP = fA * dA + (1 - fA) * dP;
    
    (* This the prameters from experiment. It has some uncertancies.*)
        
    (* Number of bonds in AuPtNP*)
    nMMAP = n[DAP, dAP];
    nAAA = n[DA, dA];
    nPPP = n[DP, dP];
    (*Number of atoms of Au nanoparticle*)
    NA = Natom[DA, dA];
    (*Number of atoms of Pt nanoparticle*)
    NP = Natom[DP, dP];
    (*Number of atoms of AuPt nanoparticle*)
    NAP = Natom[DAP, dAP];
    eq1 = nMMAP == y * nAMAP + (1 - y) * nPMAP;
    eq2 = nAMAP == nAAAP + nAPAP;
    eq3 = nPMAP == nPAAP + nPPAP;
    eq4 = nAuAu == nAAAP * (XAP / (XA + XAP)) + nAAA * (XA 
        / (XA + XAP));
    eq5 = nPtPt == nPPAP * (XAP / (XP + XAP)) + nPPP * (XP 
        / (XP + XAP));
    eq6 = nAuPt == nAPAP * (XAP / (XA + XAP));
    eq7 = nPtAu == nPAAP * (XAP / (XP + XAP));
    eq8 = (XA + XAP + XP == 1);
    (*The mass balance of Au and Pt particles were fixed to Au:Pt=fAu:1-fAu*)
    eq9 = ((XP * NP + XAP * NAP * (1 - y)) * fA == (1 - fA) *(XA * NA + XAP * NAP * y));
    eq10 = y == nPAAP / (nPAAP + nAPAP);
    cons1 = 0 <= y <= 1;
    cons2 = 0 <= XAP <= 1;
    cons3 = 0 <= XA <= 1;
    cons4 = 0 <= XP <= 1;
    cons5 = 0 <= nAMAP <= 12;
    cons6 = 0 <= nPMAP <= 12;
    cons7 = 0 <= nAAAP <= 12;
    cons8 = 0 <= nAPAP <= 12;
    cons9 = 0 <= nPAAP <= 12;
    cons10 = 0 <= nPPAP <= 12;
    sol = NSolve[{eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, cons1,
         cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10}, {nAMAP,
         nPMAP, nAAAP, nAPAP, nPAAP, nPPAP, XAP, XA, XP, y
        }, Reals];
        
   If[Length[sol]>0,{dP, dA, fA, nAuAu, nPtPt, nAuPt, nPtAu, DA, DAP, DP, nAMAP,
         nPMAP, nAAAP, nAPAP, nPAAP, nPPAP, XAP, XA, XP, y}/.sol, {{dP, dA, fA, nAuAu, nPtPt, nAuPt, nPtAu, DA, DAP, DP,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null}}]
]

DecomNanoh[dP_, dA_, fA_, nAuAu_, nPtPt_, nAuPt_, nPtAu_, DA_, DAP_, DP_, DAPh_] := 
     Module[
    {dAP, nMMAP, nAAA, nPPP, NA, NP,
         NAP, eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, cons1, cons2,
         cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10, nAMAP, nPMAP,
         nAAAP, nAPAP, nPAAP, nPPAP, XAP, XA, XP,y}
    ,
    (*Definitions of Distance and particlesize*)
    dAP = fA * dA + (1 - fA) * dP;
    
    (* This the prameters from experiment. It has some uncertancies.*)
        
    (* Number of bonds in AuPtNP*)
    nMMAP = nh[DAP, dAP, DAPh];
    nAAA = n[DA, dA];
    nPPP = n[DP, dP];
    (*Number of atoms of Au nanoparticle*)
    NA = Natom[DA, dA];
    (*Number of atoms of Pt nanoparticle*)
    NP = Natom[DP, dP];
    (*Number of atoms of AuPt nanoparticle*)
    NAP = Natomh[DAP, dAP, DAPh];
    eq1 = nMMAP == y * nAMAP + (1 - y) * nPMAP;
    eq2 = nAMAP == nAAAP + nAPAP;
    eq3 = nPMAP == nPAAP + nPPAP;
    eq4 = nAuAu == nAAAP * (XAP / (XA + XAP)) + nAAA * (XA 
        / (XA + XAP));
    eq5 = nPtPt == nPPAP * (XAP / (XP + XAP)) + nPPP * (XP 
        / (XP + XAP));
    eq6 = nAuPt == nAPAP * (XAP / (XA + XAP));
    eq7 = nPtAu == nPAAP * (XAP / (XP + XAP));
    eq8 = (XA + XAP + XP == 1);
    (*The mass balance of Au and Pt particles were fixed to Au:Pt=fAu:1-fAu*)
    eq9 = ((XP * NP + XAP * NAP * (1 - y)) * fA == (1 - fA) *(XA * NA + XAP * NAP * y));
    eq10 = y == nPAAP / (nPAAP + nAPAP);
    cons1 = 0 <= y <= 1;
    cons2 = 0 <= XAP <= 1;
    cons3 = 0 <= XA <= 1;
    cons4 = 0 <= XP <= 1;
    cons5 = 0 <= nAMAP <= 12;
    cons6 = 0 <= nPMAP <= 12;
    cons7 = 0 <= nAAAP <= 12;
    cons8 = 0 <= nAPAP <= 12;
    cons9 = 0 <= nPAAP <= 12;
    cons10 = 0 <= nPPAP <= 12;
    sol = NSolve[{eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, cons1,
         cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10}, {nAMAP,
         nPMAP, nAAAP, nAPAP, nPAAP, nPPAP, XAP, XA, XP, y
        }, Reals];
        
   If[Length[sol]>0,{dP, dA, fA, nAuAu, nPtPt, nAuPt, nPtAu, DA, DAP, DP, nAMAP,
         nPMAP, nAAAP, nAPAP, nPAAP, nPPAP, XAP, XA, XP, y}/.sol, {{dP, dA, fA, nAuAu, nPtPt, nAuPt, nPtAu, DA, DAP, DP,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null}}]
]
