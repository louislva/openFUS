% Constants

WATER_SPEED = 1500;
WATER_DENSITY = 1000;

PZT_SPEED = 4000;
PZT_DENSITY = 7800; % (source: https://www.steminc.com/piezo/PZ_property.asp)

% Lens material, polypropylene
PP_SPEED = 2565;
PP_DENSITY = 920;

% Silver epoxy
SE_SPEED = 2548;
SE_DENSITY = 3222;

c_min = WATER_SPEED;
c_max = PZT_SPEED;
f_max = 500000;
min_wave_length = c_min / f_max;
grid_size = min_wave_length / 4;

% Simulation
speed_multiplier = 1;

Nx = 128;   % number of grid points in the x direction
Ny = 128;   % number of grid points in the y direction
Nz = 128;   % number of grid points in the z direction
dx = grid_size * speed_multiplier;   % grid point spacing in the x direction [m]
dy = grid_size * speed_multiplier;   % grid point spacing in the y direction [m]
dz = grid_size * speed_multiplier;   % grid point spacing in the z direction [m]
kgrid = makeGrid(Nx, dx, Ny, dy, Nz, dz);

% Define the time array for the kgrid
% Courant-Friedrichs-Lewy (CFL) condition for stability
d = 3; % number of spatial dimensions
dt = dx / (c_max * sqrt(d)); % time step [s]

Nt = 512; % number of time steps
kgrid.t_array = (0:Nt-1) * dt; % time array

fprintf('Time step (dt): %e seconds\n', dt);
fprintf('Total time: %e seconds\n', kgrid.t_array(end));


annotation.mask = zeros(Nx, Ny, Nz);

% Define the properties of the first material
medium.sound_speed = WATER_SPEED * ones(Nx, Ny, Nz);  % [m/s]
medium.density = WATER_DENSITY * ones(Nx, Ny, Nz);      % [kg/m^3]

% Define the region for the lens
region_x = floor(30 / speed_multiplier):floor(50 / speed_multiplier);
region_y = floor(30 / speed_multiplier):floor(50 / speed_multiplier);
region_z = floor(30 / speed_multiplier):floor(50 / speed_multiplier);
annotation.mask(region_x, region_y, region_z) = 1;

medium.sound_speed(region_x, region_y, region_z) = PP_SPEED;
medium.density(region_x, region_y, region_z) = PP_DENSITY;

Sa = floor(60 / speed_multiplier);
Sb = floor(70 / speed_multiplier);

% Define a time-varying sinusoidal source
source_freq = 500000; % 1 MHz
source_mag = 1; % magnitude of the source
t_array = kgrid.t_array; % time array from the kgrid
source.p = source_mag * sin(2 * pi * source_freq * t_array);

% Define source location
source.p_mask = zeros(Nx, Ny, Nz);
source.p_mask(Sa:Sb, Sa:Sb, Sa:Sb) = 1; % example of a cubic source region

sensor.mask = zeros(Nx, Ny, Nz);
sensor.mask(Sa, Sa, Sa) = 1; % example of a single point sensor

input_args = {'DisplayMask', annotation.mask};
sensor_data = kspaceFirstOrder3D(kgrid, medium, source, sensor, input_args{:});
% Add the rectangle overlay to the existing figure
imagesc(kgrid.y_vec, kgrid.x_vec, squeeze(sensor_data(:, :, floor(Nz/2))));
xlabel('y [m]');
ylabel('x [m]');
title('Recorded Pressure');
colorbar;