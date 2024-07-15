% Read the STL file
fv = stlread('/Users/louisarge/Git/openFUS/lens-3d.stl');

% Define the resolution of the voxel grid
voxelSize = 50; % Adjust as needed
voxelMm = 1;
voxelVolume = zeros(voxelSize, voxelSize, voxelSize);

% Define the bounding box for the voxel grid
minBounds = min(fv.Points);
maxBounds = max(fv.Points);
fprintf('Min Bounds: [%f, %f, %f]\n', minBounds(1), minBounds(2), minBounds(3));
fprintf('Max Bounds: [%f, %f, %f]\n', maxBounds(1), maxBounds(2), maxBounds(3));

scale = (voxelMm * voxelSize) / (voxelSize - 1);

% Convert the STL mesh to a voxel volume
for i = 1:size(fv.ConnectivityList, 1)
    faceVertices = fv.Points(fv.ConnectivityList(i, :), :);
    % Compute the voxel indices for the vertices of the face
    voxelIndices = round((faceVertices - minBounds) ./ scale) + 1;
    % Fill the voxels corresponding to the face
    voxelVolume = fillVoxels(voxelVolume, voxelIndices);
end

% Use the voxel volume in your existing code
isosurfaceVolume = isosurface(voxelVolume, 0.5); % Adjust threshold as needed
isosurfaceVolume.faces = fliplr(isosurfaceVolume.faces); % Ensure normals point OUT

% Display the result
figure, hold on, view(3)
patch(isosurfaceVolume, 'FaceColor', 'g', 'FaceAlpha', 0.2)
axis image

% Function to fill voxels (simple example, may need refinement)
function voxelVolume = fillVoxels(voxelVolume, voxelIndices)
    for j = 1:size(voxelIndices, 1)
        voxelVolume(voxelIndices(j, 1), voxelIndices(j, 2), voxelIndices(j, 3)) = 1;
    end
end