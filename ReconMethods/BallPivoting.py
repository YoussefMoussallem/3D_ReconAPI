import open3d as o3d
from ReconMethods.Surface_Recon import surfaceRecon

class BPA(surfaceRecon):
    def __init__(self, file_path):
        super().__init__(file_path)

    def bpa_reconstruction(self):
        # BPA surface reconstruction
        with o3d.utility.VerbosityContextManager(
                o3d.utility.VerbosityLevel.Info) as cm:  # Adjust verbosity level as needed
            self.mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
                self.pcd, o3d.utility.DoubleVector([self.radius]))

    def CreateModel(self, radius):
        self.radius = radius
        self.preprocess_point_cloud()
        self.bpa_reconstruction()

        self.postprocess_mesh()

