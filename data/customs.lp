system(root,"CustomDemoSystem").

is(root,star("X",200)).  % a black hole of 200 solar masses

% A custom terra with moon and a custom star orbit the black hole with high eccentricity
orbit(root,orbit(planet(terra,"0.6"),moon,"0.002"),params(1,"0.9")).
orbit(root,star("M5V","0.8"),params(2,"0.7"),retrograde).
