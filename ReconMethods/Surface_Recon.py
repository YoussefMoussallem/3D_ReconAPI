import open3d as o3d
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

class surfaceRecon:
    def __init__(self,file_path):
        self.pcd = o3d.io.read_point_cloud(file_path)

    def preprocess_point_cloud(self):
        self.pcd.remove_statistical_outlier(nb_neighbors=self.outlier_neighbours, std_ratio=self.outlierstd_ratio)
        self.pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=self.normalestaradius, max_nn=self.normalestamaxnn))

    def postprocess_mesh(self):
        self.mesh.remove_unreferenced_vertices()
        self.mesh.remove_degenerate_triangles()
        self.mesh.remove_duplicated_triangles()
        self.mesh.remove_duplicated_vertices()
        self.mesh.remove_non_manifold_edges()

    def visualizeandsave(self,nameadtype):
        o3d.visualization.draw_geometries([self.mesh])
        o3d.io.write_triangle_mesh(nameadtype, self.mesh)
    
    def save(self,nameadtype):
        o3d.io.write_triangle_mesh(nameadtype, self.mesh)