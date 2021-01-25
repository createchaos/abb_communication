'''
. . . . . . . . . . . . . . . . . . 
.                                 .
.   <<><><>    <<><><>  <<        .
.   <<    ><   <<       <<        .
.   <<><><>    <<><><   <<        .  
.   <<  ><     <<       <<        .
.   <<   <>    <<       <<        .
.   <<    ><   <<       <<><><>   .
.                                 .
.             GKR 2016/17         .
. . . . . . . . . . . . . . . . . .

Created on 05.01.2017

@author: stefanap 
'''


from abb_communication.geometry import Frame
import ghpythonlib.components as ghcomp
import Rhino.Geometry as rg
import math as m


class Gantry(object):
    
    #===========================================================================
    def __init__(self, geo, gantry_plane):
        ''' gantry class for the rfl 
        geo = gantry geometry as list
        plane = defined gantry plane - if default - [0,0,0,x,y]
        '''
        
        self.geo = geo
        self.plane = gantry_plane
        self.frame = Frame(self.plane, draw_geo=True)
        
        self.T = rg.Transform.PlaneToPlane(self.plane, rg.Plane.WorldXY)
        self.geo_WCS = ghcomp.Transform(self.geo, self.T) # gantry aligned_with_WCS
        
        self.plane_WCS = ghcomp.Transform(self.plane, self.T) # should be WorldXY plane
    
    
    def get_transformed_geo(self, plane_new, rob_nr):
        
        self.plane = plane_new
        geo_z1, geo_z2, geo_y, geo_x, geo_fix = self.geo
        
        plane_0 = rg.Plane(rg.Point3d(0,0,0), rg.Vector3d(1,0,0), rg.Vector3d(0,1,0))

        #self.plane.YAxis.Reverse()
        #self.plane.XAxis.Reverse()
        vec_trans_1 = rg.Vector3d.Subtract(rg.Vector3d(self.plane.Origin), rg.Vector3d(rg.Plane.WorldXY.Origin))
        T1 = rg.Transform.Translation(vec_trans_1)
        
        T_rot = rg.Transform.Rotation(m.pi, rg.Vector3d.ZAxis, self.plane.Origin)
        T_mirr = rg.Transform.Mirror(self.plane.Origin, rg.Vector3d.XAxis)
            
        z_max = 4500
        vec_trans_2_z = ((z_max - vec_trans_1.Z)/2) + vec_trans_1.Z 
        vec_trans_2 = vec_trans_1
        vec_trans_2.Z = vec_trans_2_z
        T2 = rg.Transform.Translation(vec_trans_2)
        
        vec_trans_3 = rg.Vector3d(vec_trans_1.X, vec_trans_1.Y, 0)
        T3 = rg.Transform.Translation(vec_trans_3)
        
        vec_trans_4 = rg.Vector3d(vec_trans_1.X, 0, 0)
        T4 = rg.Transform.Translation(vec_trans_4)
        
        geo_z1_WCS = ghcomp.Transform(geo_z1, T1)
        geo_z2_WCS = ghcomp.Transform(geo_z2, T2)
        geo_y_WCS = ghcomp.Transform(geo_y, T3)
        
        if rob_nr == 1 or rob_nr == 3:
            geo_x_WCS = ghcomp.Transform(geo_x, T4)
        else:
            geo_x_WCS = None
        
        if rob_nr == 2 or rob_nr == 4:
            geo_z1_WCS = ghcomp.Transform(geo_z1_WCS, T_rot)
            geo_z2_WCS = ghcomp.Transform(geo_z2_WCS, T_rot)
        if rob_nr == 3 or rob_nr == 4:
            geo_y_WCS = ghcomp.Transform(geo_y_WCS, T_rot)
        if rob_nr == 3:
            geo_x_WCS = ghcomp.Transform(geo_x_WCS, T_mirr)

         
        geo_gantry = [geo_z1_WCS, geo_z2_WCS, geo_y_WCS, geo_x_WCS, geo_fix]
        
        return geo_gantry
        
        
    