import open3d as o3d
from ReconMethods.Surface_Recon import surfaceRecon

class AlphaShape(surfaceRecon):
    def __init__(self, file_path):
        super().__init__(file_path)

    def alpha_shape_reconstruction(self):
        # Alpha shape reconstruction
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            self.mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(self.pcd, self.alpha)


    def CreateModel(self, alpha,normalestaradius,normalestamaxnn,outlier_neighbours,outlierstd_ratio):
        self.normalestaradius=normalestaradius
        self.normalestamaxnn=normalestamaxnn
        self.outlier_neighbours=outlier_neighbours
        self.outlierstd_ratio=outlierstd_ratio
    
        self.alpha=alpha
        self.preprocess_point_cloud()
        self.alpha_shape_reconstruction()

        self.postprocess_mesh()



