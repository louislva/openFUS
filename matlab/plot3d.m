% Read the STL file
fv = stlread('/Users/louisarge/Git/openFUS/lens-3d.stl');

% Define the resolution of the voxel grid
voxelSize = 50; % Adjust as needed
voxelMm = 1;
% voxelVolume = zeros(voxelSize, voxelSize, voxelSize);

function sphereVoxels = createSphere(radius)
    size = ceil(radius * 2);
    sphereVoxels = zeros(size, size, size);
    [X, Y, Z] = ndgrid(1:size, 1:size, 1:size);
    sphere = sqrt((X - radius).^2 + (Y - radius).^2 + (Z - radius).^2) <= radius;
    sphereVoxels(sphere) = 1;
end

function lensVoxels = createLens(width, height, radius)
    lensVoxels = ones(width, width, height);
    [X, Y, Z] = ndgrid(1:width, 1:width, 1:height);
    sphere = sqrt((X - width/2).^2 + (Y - width/2).^2 + (height - Z).^2) <= radius;
    lensVoxels(sphere) = 0;
end

voxelVolume = createLens(10, 10, 5);

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
