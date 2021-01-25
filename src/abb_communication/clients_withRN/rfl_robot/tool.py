'''
. . . . . . . . . . . . . . . . . . . . . . 
.                                         .
.   <<  <<><><>  <<      ><  <<      ><   .
.   <<  <<       < ><   ><<  < ><   ><<   .
.   <<  <<><><>  << >< > ><  << >< > ><   .  
.   <<  <<       <<  ><  ><  <<  ><  ><   .
.   <<  <<       <<      ><  <<      ><   .
.   <<  <<       <<      ><  <<      ><   .
.                                         .
.             GKR 2016/17                 .
. . . . . . . . . . . . . . . . . . . . . .

Created on 02.11.2016

@author: kathrind, stefanap
'''


from abb_communication.geometry import Frame
import ghpythonlib.components as ghcomp
import Rhino.Geometry as rg
import math as m

class Tool(object):
    
    #===========================================================================
    def __init__(self, geo, tool_plane):
        ''' tool class for the robot 
        geo = tool geometry as list
        plane = defined tool plane
        geo_trfd = tool geometry transformed that the defined tool plane is aligned with the world xy plane
        '''
        
        self.geo = geo
        self.plane = tool_plane
        self.frame = Frame(self.plane, draw_geo=True)
        
        self.T = rg.Transform.PlaneToPlane(self.plane, rg.Plane.WorldXY)
        self.geo_WCS = ghcomp.Transform(self.geo, self.T) # tool aligned_with_WCS
        
        self.plane_WCS = ghcomp.Transform(self.plane, self.T) # should be WorldXY plane

        self.collision_geo = self.geo
        self.colors = [ghcomp.ColourRGB(100, 100, 150, 200)
                       for i, part in enumerate(self.geo)]
    
    #===========================================================================
    def set_collision_geo(self, collision_geo):
        """ collision geo of the LWS tool"""
        self.collison_geo = collision_geo
        self.collison_geo_WCS = ghcomp.Transform(self.collison_geo, self.T)
    
    #===========================================================================
    def get_plane(self):
        ''' returns the tool plane '''
        return rg.Plane(self.plane)
    
    #===========================================================================
    def get_frame(self):
        ''' returns the tool frame '''
        return Frame(self.get_plane())
        
    #===========================================================================
    def get_frame_axes_as_lines(self):
        ''' this method allows you to visualize the tool axes as lines and gh colors '''
        
        tool_axes = self.frame.get_axes_as_lines(length=100)
        tool_axes_colors = [ghcomp.ColourRGB(255, 255, 0, 0), ghcomp.ColourRGB(255, 0, 255, 0), ghcomp.ColourRGB(255, 0, 0, 255)]

        return tool_axes, tool_axes_colors
    
    #===========================================================================
    def get_frame_axes_as_lines_WCS(self):
        ''' this method allows you to visualize the tool axes as lines and gh colors transformed into the WCS'''
        
        tool_axes, tool_axes_colors = self.get_frame_axes_as_lines()
        tool_axes = ghcomp.Transform(tool_axes, self.T) # aligned_with_WCS
        
        return tool_axes, tool_axes_colors
    
    #===========================================================================
    def get_pose_angle_axis(self):
        ''' returns the pose with the axis angle representation '''
        
        return self.frame.get_pose_angle_axis()
    
    #===========================================================================
    def get_transformed_geo(self, T):
        ''' returns the tool geo transformed by the input transformation matrix '''
        
        return ghcomp.Transform(self.geo, T)
    
    #===========================================================================
    def get_transformed_plane(self, T):
        ''' returns the tool plane transformed by the input transformation matrix '''
        
        return ghcomp.Transform(self.plane, T)
    
    #===========================================================================
    def get_transformed_geo_WCS(self, T):
        ''' returns the tool geo_trfd transformed by the input transformation matrix '''
        
        return ghcomp.Transform(self.geo_WCS, T)
    #===========================================================================
    

class MeshMouldTool(Tool):
    
    def __init__(self, geo, tool_plane, cam_plane):
        
        Tool.__init__(self, geo, tool_plane)
        
        self.p1_fixed, self.p2_rotfront, self.p3_rotback_frame, self.p3_rotback_gripper_ret, self.p3_rotback_gripper_ext, self.collision_geo = self.geo
        #self.p1_fixed_wcs, self.p2_rotfront_wcs, self.p3_rotback_frame_wcs, self.p3_rotback_gripper_ret_wcs, self.p3_rotback_gripper_ext_wcs, self.collision_geo_wcs = self.geo_WCS
        
        self.cam_plane = cam_plane

        self.colors = [ghcomp.ColourRGB(100, 100, 100 + i*20, 150 + i*20) for i, part in enumerate(self.geo)]
        self.colors[-1] = ghcomp.ColourRGB(100, 255, 80, 110)


    def set_collision_geo(self, collision_geo):
        """ collision geo of the Meshmould tool"""
        self.collison_geo = collision_geo        
        self.collison_geo_WCS = ghcomp.Transform(self.collison_geo, self.T)
    
    def get_cam_plane_with_tool_rot_WCS(self, rot_value_back):
        
        cam_plane_WCS = ghcomp.Transform(self.cam_plane, self.T)
        T_rot_back = rg.Transform.Rotation(m.radians(rot_value_back), self.plane_WCS.ZAxis, self.plane_WCS.Origin)
        cam_plane_WCS = ghcomp.Transform(cam_plane_WCS, T_rot_back)
        
        return cam_plane_WCS  
        
    def apply_tool_transformation_WCS(self, rot_value_front, rot_value_back, extended = False):
        """ for transforming the tool which is aligned to the tool plane """
        
        geo = self.apply_tool_transformation(rot_value_front, rot_value_back, extended = extended)
        geo_WCS = ghcomp.Transform(geo, self.T) # tool aligned_with_WCS
        
        return geo_WCS
    
    def apply_coll_geo_transformation_WCS(self, rot_value_back):
        """ for transforming the collgeo which is aligned to the tool plane """       
        coll_geo = self.apply_coll_geo_transformation(rot_value_back)
        coll_geo_WCS = ghcomp.Transform(coll_geo, self.T) # tool aligned_with_WCS  
        return coll_geo_WCS
    
    def get_transformed_coll_geo_with_tool_transformation_WCS(self, T, rot_value_back):
        
        coll_geo_WCS = self.apply_coll_geo_transformation_WCS(rot_value_back)
        return ghcomp.Transform(coll_geo_WCS, T)
    
    def get_transformed_geo_with_tool_transformation_WCS(self, T, rot_value_front, rot_value_back, extended = False):
        
        geo_WCS = self.apply_tool_transformation_WCS(rot_value_front, rot_value_back, extended = extended)
        return ghcomp.Transform(geo_WCS, T)
    
    def get_transformed_geo_with_tool_transformation(self, T, rot_value_front, rot_value_back, extended = False):
        
        geo = self.apply_tool_transformation(rot_value_front, rot_value_back, extended = extended)
        return ghcomp.Transform(geo, T) 
    
    def get_transformed_plane_gripper(self, T, rot_value_front, rot_value_back, plane_gripper, extended = False):
        ''' intermediary function to check the cable routing for the welder... '''
        
        trot_plane = rg.Plane(self.plane)
        T_rot_back = rg.Transform.Rotation(m.radians(rot_value_back), trot_plane.ZAxis, trot_plane.Origin)
        
        plane_gripper = ghcomp.Transform(plane_gripper, T_rot_back)
        if extended == True:            
            return ghcomp.Transform(plane_gripper, T) 
        else:
            # maybe add a translation
            return ghcomp.Transform(plane_gripper, T) 
    
    def apply_coll_geo_transformation(self, rot_value_back):
        """ for transforming the collision geo which is in zero """
        
        trot_plane = rg.Plane(self.plane)        
        T_rot_back = rg.Transform.Rotation(m.radians(rot_value_back), trot_plane.ZAxis, trot_plane.Origin)
        collision_geo_trfd = ghcomp.Transform(self.collision_geo, T_rot_back)

        return collision_geo_trfd
        
    def apply_tool_transformation(self, rot_value_front, rot_value_back, extended = False):
        """ for transforming the tool which is in zero """
        
        #self.p1_fixed, self.p2_rotfront, self.p3_rotback_frame, self.p3_rotback_gripper_ret, self.p3_rotback_gripper_ext, self.collision_geo = self.geo

        trot_plane = rg.Plane(self.plane)
        T_rot_front = rg.Transform.Rotation(m.radians(rot_value_front), trot_plane.ZAxis, trot_plane.Origin)
        
        p2_rotfront_trfd = ghcomp.Transform(self.p2_rotfront, T_rot_front)
        
        T_rot_back = rg.Transform.Rotation(m.radians(rot_value_back), trot_plane.ZAxis, trot_plane.Origin)
        
        p3_rotback_frame_trfd = ghcomp.Transform(self.p3_rotback_frame, T_rot_back)
        p3_rotback_gripper_ret_trfd = ghcomp.Transform(self.p3_rotback_gripper_ret, T_rot_back)
        p3_rotback_gripper_ext_trfd = ghcomp.Transform(self.p3_rotback_gripper_ext, T_rot_back)
        collision_geo_trfd = ghcomp.Transform(self.collision_geo, T_rot_back)

        if extended == True:
            return [self.p1_fixed, p2_rotfront_trfd, p3_rotback_frame_trfd, p3_rotback_gripper_ext_trfd, collision_geo_trfd]
        else:
            return [self.p1_fixed, p2_rotfront_trfd, p3_rotback_frame_trfd, p3_rotback_gripper_ret_trfd, collision_geo_trfd]
        
        

class LwsGripperTool(Tool):
    
    def __init__(self, geo, tool_plane):
        
        Tool.__init__(self, geo, tool_plane)
        
        self.collision_geo = self.geo
        self.colors = [ghcomp.ColourRGB(100, 100, 150, 200) for i, part in enumerate(self.geo)]

    def set_collision_geo(self, collision_geo):
        """ collision geo of the LWS tool"""
        self.collison_geo = collision_geo        
        self.collison_geo_WCS = ghcomp.Transform(self.collison_geo, self.T)
    

class RthGripperTool(Tool):
    
    def __init__(self, geo, tool_plane):
        
        Tool.__init__(self, geo, tool_plane)
        
        self.collision_geo = self.geo
        self.colors = [ghcomp.ColourRGB(100, 100, 150, 200) for i, part in enumerate(self.geo)]

    def set_collision_geo(self, collision_geo):
        """ collision geo of the RTH tool"""
        self.collison_geo = collision_geo        
        self.collison_geo_WCS = ghcomp.Transform(self.collison_geo, self.T)
      
