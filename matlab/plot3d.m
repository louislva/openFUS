% Read the STL file
fv = stlread('/Users/louisarge/Git/openFUS/lens-3d.stl');

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

voxelVolume = createLens(50, 75, 2);

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
