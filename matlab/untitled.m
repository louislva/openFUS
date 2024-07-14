speed_multiplier = 0.25;

Nx = floor(128 / speed_multiplier);   % number of grid points in the x direction
Ny = floor(128 / speed_multiplier);   % number of grid points in the y direction
dx = 0.1 * speed_multiplier;   % grid point spacing in the x direction [m]
dy = 0.1 * speed_multiplier;   % grid point spacing in the y direction [m]
kgrid = makeGrid(Nx, dx, Ny, dy);

medium.sound_speed = 1500;  % [m/s]
medium.density = 1000;      % [kg/m^3]

Sa = floor(60 / speed_multiplier);
Sb = floor(70 / speed_multiplier);
source.p0 = zeros(Nx, Ny);
source.p0(Sa:Sb, Sa:Sb) = 1; % example of a square source

sensor.mask = zeros(Nx, Ny);
sensor.mask(Sa, Sa) = 1; % example of a single point sensor

sensor_data = kspaceFirstOrder2D(kgrid, medium, source, sensor);

imagesc(kgrid.y_vec, kgrid.x_vec, sensor_data);
xlabel('y [m]');
ylabel('x [m]');
title('Recorded Pressure');
colorbar;
