(* experimenting with "monomial" rational functions and kostka numbers *)

(*schur[a,b,c] is the schur polynomial with highest term
x^(a+b+c)y^(b+c)z^c.
num[a,b,c] will give the numerator of the n=2 p-part
--this has highest degree x^(2+a+b+c)y^(1+b+c)z^c*)


group={{},{1},{2}, {1,2}, {2,1}, {1,2,1}}

actword[f_,list_]:=
If[list=={}, f, actword[action[f,list[[1]] ],Drop[list,1]] ];

jjj=0;
(*gives the action of the ith simple reflection on f*)
action[f_, i_]:=
If[i==1, (x/y)^jjj(f/.{x->y, y->x})((y-x*t)/(x-y*t)+1)/2
         +(-1)^(jjj-1)(x/y)^jjj(f/.{x->-y, y->-x})((y-x*t)/(x-y*t)-1)/2
,(*else i==2*)
          (y/z)^jjj(f/.{y->z, z->y})((z-y*t)/(y-z*t)+1)/2
         +(-1)^(jjj-1)(y/z)^jjj(f/.{y->-z, z->-y})((z-y*t)/(y-z*t)-1)/2
]//Together;

mo[f_] := Sum[actword[f,
group[[jj]]], {jj,1,6}]//Simplify;

mn[f_] := Sum[actword[f,
group[[jj]]], {jj,1,6}]*denom//Cancel//Expand;

mn[a_,b_, c_] := Sum[actword[x^a y^b z^c,
group[[jj]]], {jj,1,6}]*denom//Cancel//Expand;

polyout[f_] := Block[{poly,aa,bb,cc,coeff},
   poly = f;
   Print[];
   While[!(poly === 0),
      {coeff,aa,bb,cc}=highestTerm[poly];
      Print[InputForm[{coeff,aa,bb,cc}]];
      poly=Expand[poly-coeff*x^aa*y^bb*z^cc];
   ];
];

mnout[a_, b_, c_] := Block[{poly,aa,bb,cc,coeff},
   poly = mn[a,b,c];
   Print[];
   While[!(poly === 0),
      {coeff,aa,bb,cc}=highestTerm[poly];
      Print[InputForm[{coeff,aa,bb,cc}]];
      poly=Expand[poly-coeff*x^aa*y^bb*z^cc];
   ];
];

numout[a_, b_, c_] := Block[{poly,aa,bb,cc,coeff},
   poly = num[a,b,c];
   Print[];
   While[!(poly === 0),
      {coeff,aa,bb,cc}=highestTerm[poly];
      Print[InputForm[{coeff,aa,bb,cc}]];
      poly=Expand[poly-coeff*x^aa*y^bb*z^cc];
   ];
];


mo[a_, b_,c_]:=
Sum[actword[x^(a+b+c+2)*y^(b+c+1)*z^c,
group[[jj]]], {jj,1,6}]//Simplify;

wcfN[a_, b_,c_]:=
Sum[(-1)^Length[group[[jj]]]*actword[x^(a+b+c+2)*y^(b+c+1)*z^c,
group[[jj]]], {jj,1,6}]//Simplify;

wcf[a_,b_,c_]:=wcfN[a,b,c]/delta//Simplify;

num[a_,b_,c_]:=wcf[a,b,c]*denom//Cancel//Expand;

schur[a_,b_,c_]:=(wcf[a,b,c]/.t->-1)* (x + y) (x + z) (y + z)//Cancel
eschur[a_,b_,c_]:=Block[{temp},temp=schur[a,b,c];
                 temp2=temp/2+(temp/.{x->-x,y->-y})/2;
                 temp3=temp2/2+(temp2/.{y->-y,z->-z})/2;
                 Expand[temp3]
]
dschur[a_,b_,c_]:=schur[a,b,c]/.{x->x^2, y->y^2, z->z^2}//Simplify

delta=(x^2-y^2)(y^2-z^2)(x^2-z^2);
denom=(x^2-t^2 y^2)(x^2-t^2 z^2)(y^2-t^2 z^2);
denom1=(x-t y)(x-t z)(y-t z);

wcfA1[a_, b_]:=(x^(a+b+1)*y^b-action[x^(a+b+1)*y^b,
1])/(x^2-y^2)*(x^2-t^2 y^2)//Simplify

mnA1[a_, b_]:=(x^(a+b+1)*y^b-action[x^(a+b+1)*y^b,
1])/(x^2-y^2)*(x^2-t^2 y^2)//Simplify

(*----------------------------*)

(* returns {a,b,c,d} where a is the coeff of
x^b y^c z^d*)
highestTerm[f_]:=Block[{expx, expy,expz, f1,f2},
expx=Exponent[f,x];
f1=Coefficient[f, x, expx];
expy=Exponent[f1,y];
f2=Coefficient[f1, y, expy];
expz=Exponent[f2, z];
f3=Coefficient[f2,z, expz];
{f3,expx, expy, expz}
]

mlr[v_,w_]:=Block[{poly, coeff, a,b,c},
poly=num[v[[1]],v[[2]],v[[3]]]*dschur[w[[1]],w[[2]],w[[3]]];
rlist={};
(*Print[poly!=0];*)
While[poly=!=0,
       {coeff,a,b,c}=highestTerm[poly];
       (*Print[highestTerm[poly]];*)
       num1=num[a-b-1 ,b-c-1,c];
       poly=Expand[poly-num1*coeff];
       AppendTo[rlist, {coeff, a-b-1, b-c-1, c}]
    ];
rlist
]

lr[v_,w_]:=Block[{poly, coeff, a,b,c},
poly=schur[v[[1]],v[[2]],v[[3]]]*schur[w[[1]],w[[2]],w[[3]]];
rlist={};
(*Print[poly!=0];*)
While[poly=!=0,
       {coeff,a,b,c}=highestTerm[poly];
       (*Print[highestTerm[poly]];*)
       num1=schur[a-b ,b-c,c];
       poly=Expand[poly-num1*coeff];
       AppendTo[rlist, {coeff, a-b, b-c, c}]
    ];
rlist
]

dlr[v_,w_]:=Block[{poly, coeff, a,b,c},
poly=schur[v[[1]],v[[2]],v[[3]]]*dschur[w[[1]],w[[2]],w[[3]]];
rlist={};
(*Print[poly!=0];*)
While[poly=!=0,
       {coeff,a,b,c}=highestTerm[poly];
       (*Print[highestTerm[poly]];*)
       num1=schur[a-b ,b-c,c];
       poly=Expand[poly-num1*coeff];
       AppendTo[rlist, {coeff, a-b, b-c, c}]
    ];
rlist
]

(*express dschur in terms of schur*)
dtos[d_,e_,f_]:=Block[{poly, rlist, num1,a,b,c},
poly=dschur[d,e,f];
rlist={};
(*Print[poly!=0];*)
While[poly=!=0,
       {coeff,a,b,c}=highestTerm[poly];
       (*Print[highestTerm[poly]];*)
       num1=schur[a-b ,b-c,c];
       poly=Expand[poly-num1*coeff];
       AppendTo[rlist, {coeff, a-b, b-c, c}];
    ];
rlist
]


<<Combinatorica`

(* for computing Hall-Littlewood polynomials *)
usualaction[f_, i_]:=
If[i==1, f/.{x->y, y->x},
          f/.{y->z, z->y}
]//Together;
usualactword[f_,list_]:=
If[list=={}, f, usualactword[usualaction[f,list[[1]] ],Drop[list,1]] ];

(* the parameter is T *)
vv[m_] := Product[(1-T^i)/(1-T),{i,1,m}];
hlfactor[lambda_] := Block[{pp,ii,ll,ans,zz},
		  ans=1;
		  pp = TransposePartition[Reverse[Sort[lambda]]];
		  ll=Length[pp];
		  For[ii=1,ii<=ll-1,ii++,
		     ans = ans*vv[pp[[ii]]-pp[[ii+1]]];
		     ];
		  ans = ans*vv[pp[[ll]]];
		  zz=0;
		  For[ii=1,ii<=Length[lambda],ii++,
		    If[lambda[[ii]] == 0, zz++];
		  ];
		  ans = ans*vv[zz];
		  Return[ans];
];		  

hl[a_, b_,c_]:=
If[{a,b,c}=={0,0,0}, 1,
hlfactor[{a+b+c,b+c,c}]^-1*Sum[usualactword[x^(a+b+c)*y^(b+c)*z^c*(x-T*y)*(x-T*z)*(y-T*z)/((x-y)*(x-z)*(y-z)),group[[jj]]], {jj,1,6}]//Simplify//Expand//Together];

