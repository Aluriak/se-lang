root(1,"CustomDemoSystem").

is(1,star("X",200)).  % a black hole of 200 solar masses

% A custom terra and custom star orbit the black hole with high eccentricity
orbit(1,planet(terra,"0.6"),params(1,"0.9")).
orbit(1,star("M5V","0.6"),params(2,"0.7"),retrograde).
