% Read the STL file
fv = stlread('/Users/louisarge/Git/openFUS/lens-3d.stl');

% Define the resolution of the voxel grid
voxelSize = 50; % Adjust as needed
voxelMm = 1;
% voxelVolume = zeros(voxelSize, voxelSize, voxelSize);

% function sphereVoxels = createSphere(radius)
%     size = ceil(radius * 2);
%     sphereVoxels = zeros(size, size, size);
%     [X, Y, Z] = ndgrid(1:size, 1:size, 1:size);
%     sphere = sqrt((X - radius).^2 + (Y - radius).^2 + (Z - radius).^2) <= radius;
%     sphereVoxels(sphere) = 1;
% end

function cylinderVoxels = createCylinder(diameter, depth)
    cylinderVoxels = zeros(diameter, diameter, depth);
    [X, Y, Z] = ndgrid(1:diameter, 1:diameter, 1:depth);
    cylinder = sqrt((X - diameter/2).^2 + (Y - diameter/2).^2) <= diameter/2;
    cylinderVoxels(cylinder) = 1;
end

function lensVoxels = createLens(diameter, depth, radius, padding)
    lensVoxels = zeros(diameter, diameter, depth);
    % Add cylinder
    cylinder = createCylinder(diameter, depth);
    lensVoxels = lensVoxels + cylinder;

    % Subtract sphere
    [X, Y, Z] = ndgrid(1:diameter, 1:diameter, 1:depth);
    sphere = sqrt((X - diameter/2).^2 + (Y - diameter/2).^2 + (Z - radius - padding).^2) <= radius;
    lensVoxels(sphere) = 0;
end

function lensVoxels = createLensImplicit(diameter, radius, padding)
    depth = sqrt(radius^2 - (diameter / 2)^2) + padding;
    lensVoxels = createLens(diameter, ceil(depth), radius, padding + 1);
end

voxelVolume = createLensImplicit(50, 75, 2);

% Visualize the sphere
figure;
[x, y, z] = ind2sub(size(voxelVolume), find(voxelVolume));
scatter3(x, y, z, 'filled');
xlabel('X');
ylabel('Y');
zlabel('Z');
title('3D Visualization of Sphere');
axis equal;
grid on;
