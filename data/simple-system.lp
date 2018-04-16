% Some ways to do a simple system with sun, earth and moon.


% First way: with references
% root(1,"MySimpleSystem","MSS").  % replace the previously defined root
% orbit(1,2,1).
% orbit(2,3,"0.01").
% is(1,sun).  is(2,earth).  is(3,moon).


% Second way: recursive
root(sun,"MySimpleSystem","MSS").
orbit(sun,orbit(earth,moon,"0.01"),1).


% Third way: recursive with references
% root(sun,"MySimpleSystem","MSS").
% orbit(sun,orbit(42,23,"0.01"),1).
% is(42,earth).  is(23,moon).


% Fourth way: mixed
% root(sun,"MySimpleSystem","MSS").
% root(sun,"MySimpleSystem","MSS").
% orbit(sun,my_earth,1).
% orbit(my_earth,moon,"0.01").
% is(my_earth,earth).
