% Lens utils

function cylinderVoxels = createCylinder(diameter, depth)
    cylinderVoxels = zeros(diameter, diameter, depth);
    [X, Y, Z] = ndgrid(1:diameter, 1:diameter, 1:depth);
    cylinder = sqrt((X - diameter/2).^2 + (Y - diameter/2).^2) <= diameter/2;
    cylinderVoxels(cylinder) = 1;
end

function lensVoxels = createLensExplicit(diameter, depth, radius, padding)
    lensVoxels = zeros(diameter, diameter, depth);
    % Add cylinder
    cylinder = createCylinder(diameter, depth);
    lensVoxels = lensVoxels + cylinder;

    % Subtract sphere
    [X, Y, Z] = ndgrid(1:diameter, 1:diameter, 1:depth);
    sphere = sqrt((X - diameter/2).^2 + (Y - diameter/2).^2 + (Z - radius - padding).^2) <= radius;
    lensVoxels(sphere) = 0;
end

function lensVoxels = createLens(diameter, radius, padding)
    depth = sqrt(radius^2 - (diameter / 2)^2) + padding;
    lensVoxels = createLensExplicit(diameter, ceil(depth), radius, padding + 1);
end

function bigVoxels = makeBig(width, height, depth, objectVoxels)
    bigVoxels = zeros(width, height, depth);
    [objWidth, objHeight, objDepth] = size(objectVoxels);
    
    % Calculate the starting indices to place objectVoxels centrally
    startX = floor((width - objWidth) / 2) + 1;
    startY = floor((height - objHeight) / 2) + 1;
    startZ = floor((depth - objDepth) / 2) + 1;
    
    % Place objectVoxels in the center of bigVoxels
    bigVoxels(startX:startX+objWidth-1, startY:startY+objHeight-1, startZ:startZ+objDepth-1) = objectVoxels;
end

function notVoxels = invertVoxels(originalVoxels)
    notVoxels = 1 - originalVoxels;
end

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
global grid_size;
grid_size = min_wave_length / 4;

% Simulation
speed_multiplier = 1;

function voxelLength = mmToVoxelLength(mm)
    global grid_size;
    voxelLength = mm / (grid_size * 1000);
end

Nx = 100;   % number of grid points in the x direction
Ny = 100;   % number of grid points in the y direction
Nz = 100;   % number of grid points in the z direction
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
lensDiameter = mmToVoxelLength(30);
lensRadius = mmToVoxelLength(22.84);
lensPadding = mmToVoxelLength(1);
lens = makeBig(Nx, Ny, Nz, createLens(lensDiameter, lensRadius, lensPadding));

annotation.mask = annotation.mask + lens;

% region_x = floor((Nx - lensDiameter) / 2):floor((Nx + lensDiameter) / 2);
% region_y = floor((Ny - lensDiameter) / 2):floor((Ny + lensDiameter) / 2);
% region_z = floor((Nz - lensDiameter) / 2):floor((Nz + lensDiameter) / 2);
% annotation.mask(region_x, region_y, region_z) = 1;

medium.sound_speed = invertVoxels(lens) * WATER_SPEED + lens * PP_SPEED;
medium.density = invertVoxels(lens) * WATER_DENSITY + lens * PP_DENSITY;

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