% LENS UTILITY FUNCTIONS
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

function bigVoxels = makeBig(width, height, depth, objectVoxels, x, y, z)
    bigVoxels = zeros(width, height, depth);
    [objWidth, objHeight, objDepth] = size(objectVoxels);
    
    % Calculate the starting indices to place objectVoxels centrally
    startX = ceil((width - objWidth) / 2) + 1;
    startY = ceil((height - objHeight) / 2) + 1;
    startZ = ceil((depth - objDepth) / 2) + 1;
    
    if x ~= 0
        startX = x;
    end
    if y ~= 0
        startY = y;
    end
    if z ~= 0
        startZ = z;
    end
    
    % Place objectVoxels in the center of bigVoxels
    bigVoxels(startX:startX+objWidth-1, startY:startY+objHeight-1, startZ:startZ+objDepth-1) = objectVoxels;
end

function notVoxels = invertVoxels(originalVoxels)
    notVoxels = 1 - originalVoxels;
end

% CONSTANTS
WATER_SPEED = 1500;
WATER_DENSITY = 1000;

PZT_SPEED = 4000; % Transducer material, PZT-5H
PZT_DENSITY = 7800; % (source: https://www.steminc.com/piezo/PZ_property.asp)

PP_SPEED = 2565; % Lens material, polypropylene
PP_DENSITY = 920;

SE_SPEED = 2548; % Silver epoxy, impedence transformer + electrode
SE_DENSITY = 3222;

% Simulation constants (derived from our constraints)
c_min = WATER_SPEED;
c_max = PZT_SPEED;
f_max = 500000;
min_wave_length = c_min / f_max;
global grid_size;
grid_size = min_wave_length / 4;

function voxelLength = mmToVoxelLength(mm)
    global grid_size;
    voxelLength = mm / (grid_size * 1000);
end

Nx = 75;   % number of grid points in the x direction
Ny = 75;   % number of grid points in the y direction
Nz = 100;   % number of grid points in the z direction
dx = grid_size;   % grid point spacing in the x direction [m]
dy = grid_size;   % grid point spacing in the y direction [m]
dz = grid_size;   % grid point spacing in the z direction [m]
kgrid = makeGrid(Nx, dx, Ny, dy, Nz, dz);

% Define the time array for the kgrid
% Courant-Friedrichs-Lewy (CFL) condition for stability
d = 3; % number of spatial dimensions
dt = dx / (c_max * 2 * sqrt(d)); % time step [s]

Nt = ceil(512 * 1 * (Nz / 50)); % number of time steps
kgrid.t_array = (0:Nt-1) * dt; % time array

fprintf('Time step (dt): %e seconds\n', dt);
fprintf('Total time: %e seconds\n', kgrid.t_array(end));

% DEFINE OBJECTS

center = ceil(Nx / 2);
% General transducer thing
T_x = center;
T_radius = mmToVoxelLength(30 / 2);
T_x0 = ceil(T_x - T_radius);
T_x1 = ceil(T_x0 + T_radius * 2);

% Source, PZT
S_depth = mmToVoxelLength(4.2);
S_z0 = 1;
S_z1 = ceil(S_z0 + S_depth);
transducerRaw = createCylinder(T_radius * 2, ceil(S_depth));
transducer = makeBig(Nx, Ny, Nz, transducerRaw, 0, 0, S_z0);

% Silver Epoxy
E_depth = round(mmToVoxelLength((SE_SPEED / 500000 / 4) * 1000));
fprintf('E_depth: %f\n', E_depth);
silverEpoxyRaw = createCylinder(T_radius * 2, E_depth);
silverEpoxy = makeBig(Nx, Ny, Nz, silverEpoxyRaw, 0, 0, S_z1);

E_z0 = S_z1 + 0;
E_z1 = ceil(E_z0 + E_depth);

% Lens, PP
lensDiameter = mmToVoxelLength(30);
lensRadius = mmToVoxelLength(22.84);
lensPadding = mmToVoxelLength(1);
lensRaw = createLens(lensDiameter, lensRadius, lensPadding);
L_z = E_z1 + 0;
L_z1 = ceil(L_z + size(lensRaw, 3));
lens = makeBig(Nx, Ny, Nz, lensRaw, 0, 0, L_z + 1);

% INSERT OBJECTS
annotation.mask = zeros(Nx, Ny, Nz);
medium.sound_speed = WATER_SPEED * ones(Nx, Ny, Nz);  % [m/s]
medium.density = WATER_DENSITY * ones(Nx, Ny, Nz);      % [kg/m^3]

% Transducer / Source
medium.sound_speed = invertVoxels(transducer) .* medium.sound_speed + transducer .* PZT_SPEED;
medium.density = invertVoxels(transducer) .* medium.density + transducer .* PZT_DENSITY;
annotation.mask = annotation.mask + transducer;
source.p_mask = transducer;

% Actual sine waves from source
source_freq = 500000; % 500 kHz
source_mag = 1; % magnitude of the source
t_array = kgrid.t_array; % time array from the kgrid
source.p = source_mag * sin(2 * pi * source_freq * t_array);

% Silver epoxy
medium.sound_speed = invertVoxels(silverEpoxy) .* medium.sound_speed + silverEpoxy .* SE_SPEED;
medium.density = invertVoxels(silverEpoxy) .* medium.density + silverEpoxy .* SE_DENSITY;
annotation.mask = annotation.mask + silverEpoxy;

% Lens
medium.sound_speed = invertVoxels(lens) .* medium.sound_speed + lens .* PP_SPEED;
medium.density = invertVoxels(lens) .* medium.density + lens .* PP_DENSITY;
annotation.mask = annotation.mask + lens;

% Sensors
sensor.mask = zeros(Nx, Ny, Nz);
S_start = 15;
sensor.mask(center, center, S_start:Nz) = 1; % example of a single point sensor
annotation.mask = annotation.mask + sensor.mask;

input_args = {'DisplayMask', annotation.mask};
sensor_data = kspaceFirstOrder3D(kgrid, medium, source, sensor, input_args{:});
sensor_data_max = max(sensor_data, [], 2);

% Display sensor data
figure;
imagesc(squeeze(sensor_data_max));
colorbar;
title('Sensor Data (Max Over Time)');
xlabel('...');
ylabel('mm');

% Modify y-axis labels dynamically
ax = gca;
addlistener(ax, 'YLim', 'PostSet', @(src, event) updateYTickLabels(ax, S_start));

function updateYTickLabels(ax, S_start)
    global grid_size;
    yticks = get(ax, 'YTick');
    yticks = yticks + S_start;
    yticks = yticks * grid_size * 1000;
    set(ax, 'YTickLabel', yticks);
end

updateYTickLabels(ax, S_start);