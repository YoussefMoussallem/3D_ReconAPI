import open3d as o3d
from ReconMethods.Surface_Recon import surfaceRecon
import numpy as np
import matplotlib.pyplot as plt

class Poisson(surfaceRecon):

    def __init__(self, file_path):
        super().__init__(file_path)

    def poisson_reconstruction(self):
        with o3d.utility.VerbosityContextManager(
                o3d.utility.VerbosityLevel.Debug) as cm:
            self.mesh, self.densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                self.pcd, self.depth)  


    def maskMesh(self):
        self.densities=np.asarray(self.densities)
        densitiy_colors=plt.get_cmap('plasma')(
            (self.densities-self.densities.min())/(self.densities.max()-self.densities.min()))
        densitiy_colors=densitiy_colors[:,:3]
        density_mesh=o3d.geometry.TriangleMesh()
        density_mesh.vertices=self.mesh.vertices
        density_mesh.triangles=self.mesh.triangles
        density_mesh.triangle_normals=self.mesh.triangle_normals
        density_mesh.vertex_colors=o3d.utility.Vector3dVector(densitiy_colors)
        
        vertices_to_remove=self.densities<np.quantile(self.densities,0.05)
        self.mesh.remove_vertices_by_mask(vertices_to_remove)

    
    def CreateModel(self,depth,normalestaradius,normalestamaxnn,outlier_neighbours,outlierstd_ratio):
        self.depth=depth
        self.normalestaradius=normalestaradius
        self.normalestamaxnn=normalestamaxnn
        self.outlier_neighbours=outlier_neighbours
        self.outlierstd_ratio=outlierstd_ratio
        
        self.preprocess_point_cloud()
        self.poisson_reconstruction()

        self.maskMesh()
        self.postprocess_mesh()
        




