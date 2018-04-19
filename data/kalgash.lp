% Description of systems at https://planetplanet.net/2018/03/21/asimov-kalgash-take2/

% Common to all
system(black_hole,"Kalgash").


% Kalgash 2 system
orbit(black_hole,ring(8,sun),20).
orbit(black_hole,orbit(red_dwarf,earth,"0.2"),10).


% Kalgash 3 system
% orbit(black_hole,ring(sun,12,orbit(1,earth,1)),20).


% Kalgash 4 system
% orbit(black_hole,ring(sun,8),1,retrograde).
% orbit(black_hole,earth,"2.5").
% orbit(black_hole,ring(sun,8),"4").


% Kalgash 5 system
% orbit(black_hole,ring(sun,8),1,retrograde).
% orbit(black_hole,earth,"2.5").
% orbit(black_hole,ring(blue_giant,8),20).
