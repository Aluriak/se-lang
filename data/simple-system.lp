% Some ways to do a simple system with sun, earth and moon.


% First way: with references
% system(1,"MySimpleSystem").  % replace the previously defined root
% orbit(1,2,1).
% orbit(2,3,"0.01").
% is(1,sun).  is(2,earth).  is(3,moon).


% Second way: recursive
system(sun,"MySimpleSystem").
orbit(sun,orbit(earth,moon,"0.01"),1).


% Third way: recursive with references
% system(sun,"MySimpleSystem").
% orbit(sun,orbit(42,23,"0.01"),1).
% is(42,earth).  is(23,moon).


% Fourth way: mixed
% system(sun,"MySimpleSystem").
% orbit(sun,my_earth,1).
% orbit(my_earth,moon,"0.01").
% is(my_earth,earth).
