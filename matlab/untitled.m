speed_multiplier = 0.25;

Nx = floor(128 / speed_multiplier);   % number of grid points in the x direction
Ny = floor(128 / speed_multiplier);   % number of grid points in the y direction
dx = 0.1 * speed_multiplier;   % grid point spacing in the x direction [m]
dy = 0.1 * speed_multiplier;   % grid point spacing in the y direction [m]
kgrid = makeGrid(Nx, dx, Ny, dy);

annotation.mask = zeros(Nx, Ny);

% Define the properties of the first material
medium.sound_speed = 1500 * ones(Nx, Ny);  % [m/s]
medium.density = 1000 * ones(Nx, Ny);      % [kg/m^3]

% Define the properties of the second material
second_material_speed = 2000;  % [m/s]
second_material_density = 1200; % [kg/m^3]

% Define the region for the second material
region_x = floor(30 / speed_multiplier):floor(50 / speed_multiplier);
region_y = floor(30 / speed_multiplier):floor(50 / speed_multiplier);
annotation.mask(region_x, region_y) = 1;

medium.sound_speed(region_x, region_y) = second_material_speed;
medium.density(region_x, region_y) = second_material_density;

Sa = floor(60 / speed_multiplier);
Sb = floor(70 / speed_multiplier);
source.p0 = zeros(Nx, Ny);
source.p0(Sa:Sb, Sa:Sb) = 1; % example of a square source

sensor.mask = zeros(Nx, Ny);
sensor.mask(Sa, Sa) = 1; % example of a single point sensor

input_args = {'DisplayMask', annotation.mask};
sensor_data = kspaceFirstOrder2D(kgrid, medium, source, sensor, input_args{:});
% Add the rectangle overlay to the existing figure
hold on;
rectangle('Position', [region_y(1), region_x(1), length(region_y), length(region_x)], 'EdgeColor', 'r', 'LineWidth', 2);

imagesc(kgrid.y_vec, kgrid.x_vec, sensor_data);
xlabel('y [m]');
ylabel('x [m]');
title('Recorded Pressure');
colorbar;