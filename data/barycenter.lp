% Showcase for barycenter.
system(root,"CustomDemoSystem").

is(root,barycenter).  % barycenter of binary black holes

% the two last args of params/6 are ascending node and arg of pericenter
orbit(root,black_hole,params("0.1","0.5",0,0,70,180)).
orbit(root,black_hole,params("0.1","0.5")).
