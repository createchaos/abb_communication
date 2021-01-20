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

Created on 09.12.2016

@author: kathrind, stefanap
'''



from abb_communication.geometry import Frame
import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import math as m

from communication import ABBCommunication


class Robot(object):

    #===========================================================================
    def __init__(self, link_geo, base_geo, joint_planes, ip_abb = '192.168.125.1', tool = None):
        ''' the robot class, it contains:
        1) the geometry of the robot
        2) the communication modules to send commands to the ABB arm.
        '''

        self.link_geo = link_geo
        self.base_geo = base_geo

        self.joint_planes = joint_planes
        self.tool = tool # has to be set with the Tool class

        self.origin_plane = rg.Plane.WorldXY

        self.joint_values = [0,0,0,0,0,0]

        # transform world to robot origin
        self.T_W_R = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, self.origin_plane)
        # transform robot to world
        self.T_R_W = rg.Transform.PlaneToPlane(self.origin_plane, rg.Plane.WorldXY)

        geo = self.get_geo_with_rotated_joints_in_world(self.joint_values)
        # --> then self.T_R_TOOL0 and self.T_W_TOOL0 are set

        self.comm = ABBCommunication("ABB", ip_abb, port_snd=30003, port_rcv=30004)

        self.colors_links = [ghcomp.ColourRGB(150, 220, 220, 220) for part in link_geo]
        self.colors_base = [ghcomp.ColourRGB(150, 220, 220, 220) for part in base_geo]

    #===========================================================================
    def set_tool(self, tool):
        ''' sets the tool of the robot using the tool class '''

        self.tool = tool # shall be of the class Tool

    #===========================================================================
    def set_robot_origin(self, plane):
        ''' sets to origin plane of the robot '''

        self.origin_plane = plane
        self.T_W_R = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, self.origin_plane)
        self.T_R_W = rg.Transform.PlaneToPlane(self.origin_plane, rg.Plane.WorldXY)

    #===========================================================================
    def set_robot_origin_with_measured_base(self, base_plane):
        ''' sets to origin plane of the robot based on a manual measured base '''

        T = rg.Transform.PlaneToPlane(base_plane, rg.Plane.WorldXY)
        plane = ghcomp.Transform(rg.Plane.WorldXY, T)

        self.set_robot_origin(plane)

    #===========================================================================
    def get_tool_plane_in_RCS(self, tool_plane_WCS):
        ''' returns the tool plane in the robot coordinate system from a plane in the world cs'''

        tool_plane_RCS = ghcomp.Transform(tool_plane_WCS, self.T_R_W)
        return tool_plane_RCS

    #===========================================================================
    def get_tool_pose_in_RCS(self, tp_WCS):
        ''' returns the tool pose in the robot coordinate system from a plane in the world cs'''

        frame = Frame(self.get_tool_plane_in_RCS(tp_WCS))
        return frame.get_pose_angle_axis()

    #===========================================================================
    def get_tool0_plane_in_RCS(self, tp_WCS):
        ''' returns the tool0 plane in the robot coordinate system from a plane in the world cs -
        we want to 'subtract' the tool T from the tool plane in RCS '''

        tool_plane_in_RCS = self.get_tool_plane_in_RCS(tp_WCS)

        T_TP_in_zero_W = rg.Transform.PlaneToPlane(self.tool.plane, rg.Plane.WorldXY)

        tool0_plane_in_RCS = rg.Plane.WorldXY
        tool0_plane_in_RCS.Transform(T_TP_in_zero_W)

        T_W_TP_in_RCS = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool_plane_in_RCS)
        tool0_plane_in_RCS.Transform(T_W_TP_in_RCS)

        return tool0_plane_in_RCS

    #===========================================================================
    def get_tool_plane_from_pose_quaternion(self, pose_quaternion):
        ''' Returns the tool plane according to the given pose in angle axis. '''
        frame = Frame()
        frame.set_to_pose_quaternion(pose_quaternion)
        return frame.get_plane()

    #===========================================================================
    def get_tool0_plane_from_pose_quaternion(self, pose_quaternion):
        ''' Returns the tool0 plane according to the given pose in angle axis. '''
        tool_plane_RCS = self.get_tool_plane_from_pose_quaternion(pose_quaternion)

        # Edit Romana:
        T1 = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool_plane_RCS)
        T2 = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, self.tool.get_plane())
        tool0_plane_RCS = rg.Plane.WorldXY
        tool0_plane_RCS.Transform(T1 * T2)

        # Kathrin TODO: this does not work... why??
        #T = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, self.tool.get_plane())
        #tcp_plane_RCS = ghcomp.Transform(tool_plane_RCS, T)
        return tool0_plane_RCS

    def get_geo_with_rotated_joints_in_world(self, joint_values):
        ''' the joint values (in degrees) serve as the input, the method returns the link geo (and tool geo) and tool0 plane transformed '''

        # the angles in radians
        joint_values = [m.radians(j) for j in joint_values]
        a1, a2, a3, a4, a5, a6 = joint_values
        L1, L2, L3, L4, L5, L6 = self.link_geo

        # calculate transformations
        j1, j2, j3, j4, j5, j6 = [rg.Plane(jp) for jp in self.joint_planes]

        T1 = rg.Transform.Rotation(a1, j1.ZAxis, j1.Origin)
        T2 = T1 * rg.Transform.Rotation(a2, j2.ZAxis, j2.Origin)
        T3 = T2 * rg.Transform.Rotation(a3, j3.ZAxis, j3.Origin)
        T4 = T3 * rg.Transform.Rotation(a4, j4.ZAxis, j4.Origin)
        T5 = T4 * rg.Transform.Rotation(a5, j5.ZAxis, j5.Origin)
        T6 = T5 * rg.Transform.Rotation(a6, j6.ZAxis, j6.Origin)

        L1_t = ghcomp.Transform(L1, T1)
        L2_t = ghcomp.Transform(L2, T2)
        L3_t = ghcomp.Transform(L3, T3)
        L4_t = ghcomp.Transform(L4, T4)
        L5_t = ghcomp.Transform(L5, T5)
        L6_t = ghcomp.Transform(L6, T6)

        link_geo_transformed = [L1_t, L2_t, L3_t, L4_t, L5_t, L6_t]

        tool0_plane_transformed = ghcomp.Transform(j6, T6)
        self.T_R_TOOL0 = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed)

        link_geo_transformed_world = ghcomp.Transform(link_geo_transformed, self.T_W_R)
        tool0_plane_transformed_world = ghcomp.Transform(tool0_plane_transformed, self.T_W_R)
        base_geo_world = ghcomp.Transform(self.base_geo, self.T_W_R)

        self.T_W_TOOL0 = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed_world)

        if self.tool:
            tool_geo_trfd_world = ghcomp.Transform(self.tool.geo, rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed_world))
            return [base_geo_world, link_geo_transformed_world, tool_geo_trfd_world]
        else:
            return [base_geo_world, link_geo_transformed_world]


    def get_attachment_planes_for_cables(self, plane_transformer, plane_gripper, joint_values, tool_joint_values, extended = True, transformer_on_axis = 3):

        tool0_plane_transformed_world = self.get_tool0_plane_from_joint_values_world(joint_values)

        # the angles in radians
        joint_values = [m.radians(j) for j in joint_values]
        a1, a2, a3, a4, a5, a6 = joint_values

        # calculate transformations
        j1, j2, j3, j4, j5, j6 = [rg.Plane(jp) for jp in self.joint_planes]

        T1 = rg.Transform.Rotation(a1, j1.ZAxis, j1.Origin)
        T2 = T1 * rg.Transform.Rotation(a2, j2.ZAxis, j2.Origin)
        T3 = T2 * rg.Transform.Rotation(a3, j3.ZAxis, j3.Origin)
        T4 = T3 * rg.Transform.Rotation(a4, j4.ZAxis, j4.Origin)
        T5 = T4 * rg.Transform.Rotation(a5, j5.ZAxis, j5.Origin)
        T6 = T5 * rg.Transform.Rotation(a6, j6.ZAxis, j6.Origin)

        if transformer_on_axis == 6: plane_transformer_transformed = ghcomp.Transform(plane_transformer, T6)
        if transformer_on_axis == 4: plane_transformer_transformed = ghcomp.Transform(plane_transformer, T4)
        if transformer_on_axis == 3: plane_transformer_transformed = ghcomp.Transform(plane_transformer, T3)

        plane_transformer_transformed_world = ghcomp.Transform(plane_transformer_transformed, self.T_W_R)

        T = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed_world)
        plane_gripper_transformed_world = self.tool.get_transformed_plane_gripper(T, tool_joint_values[0], tool_joint_values[1], plane_gripper, extended = extended)

        return (plane_transformer_transformed_world, plane_gripper_transformed_world)

    def get_geo_with_rotated_joints_in_world_with_tool_rot(self, joint_values, tool_joint_values, extended = True):
        ''' the joint values (in degrees) serve as the input, the method returns the link geo (and tool geo) and tool0 plane transformed '''

        # the angles in radians
        joint_values = [m.radians(j) for j in joint_values]
        a1, a2, a3, a4, a5, a6 = joint_values
        L1, L2, L3, L4, L5, L6 = self.link_geo

        # calculate transformations
        j1, j2, j3, j4, j5, j6 = [rg.Plane(jp) for jp in self.joint_planes]

        T1 = rg.Transform.Rotation(a1, j1.ZAxis, j1.Origin)
        T2 = T1 * rg.Transform.Rotation(a2, j2.ZAxis, j2.Origin)
        T3 = T2 * rg.Transform.Rotation(a3, j3.ZAxis, j3.Origin)
        T4 = T3 * rg.Transform.Rotation(a4, j4.ZAxis, j4.Origin)
        T5 = T4 * rg.Transform.Rotation(a5, j5.ZAxis, j5.Origin)
        T6 = T5 * rg.Transform.Rotation(a6, j6.ZAxis, j6.Origin)

        L1_t = ghcomp.Transform(L1, T1)
        L2_t = ghcomp.Transform(L2, T2)
        L3_t = ghcomp.Transform(L3, T3)
        L4_t = ghcomp.Transform(L4, T4)
        L5_t = ghcomp.Transform(L5, T5)
        L6_t = ghcomp.Transform(L6, T6)

        link_geo_transformed = [L1_t, L2_t, L3_t, L4_t, L5_t, L6_t]

        tool0_plane_transformed = ghcomp.Transform(j6, T6)
        self.T_R_TOOL0 = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed)

        link_geo_transformed_world = ghcomp.Transform(link_geo_transformed, self.T_W_R)
        tool0_plane_transformed_world = ghcomp.Transform(tool0_plane_transformed, self.T_W_R)
        base_geo_world = ghcomp.Transform(self.base_geo, self.T_W_R)

        self.T_W_TOOL0 = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed_world)

        if self.tool:
            T = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, tool0_plane_transformed_world)
            tool_geo_trfd_world = self.tool.get_transformed_geo_with_tool_transformation(T, tool_joint_values[0], tool_joint_values[1], extended = extended)
            return [base_geo_world, link_geo_transformed_world, tool_geo_trfd_world]
        else:
            return [base_geo_world, link_geo_transformed_world]


    def get_tool0_plane_from_joint_values(self, joint_values):
        ''' the joint values (in degrees)'''

        # the angles in radians
        joint_values = [m.radians(j) for j in joint_values]
        a1, a2, a3, a4, a5, a6 = joint_values

        # calculate transformations
        j1, j2, j3, j4, j5, j6 = [rg.Plane(jp) for jp in self.joint_planes]

        T1 = rg.Transform.Rotation(a1, j1.ZAxis, j1.Origin)
        T2 = T1 * rg.Transform.Rotation(a2, j2.ZAxis, j2.Origin)
        T3 = T2 * rg.Transform.Rotation(a3, j3.ZAxis, j3.Origin)
        T4 = T3 * rg.Transform.Rotation(a4, j4.ZAxis, j4.Origin)
        T5 = T4 * rg.Transform.Rotation(a5, j5.ZAxis, j5.Origin)
        T6 = T5 * rg.Transform.Rotation(a6, j6.ZAxis, j6.Origin)

        tool0_plane_transformed = ghcomp.Transform(j6, T6)

        return tool0_plane_transformed

    def get_tool0_pose_from_joint_values(self, joint_values):
        ''' the joint values (in degrees)'''

        frame = Frame(self.get_tool0_plane_from_joint_values(joint_values))
        return frame.get_pose_quaternion()

    def get_tool0_plane_from_joint_values_world(self, joint_values):
        ''' the joint values (in degrees)'''

        tool0_plane_transformed = self.get_tool0_plane_from_joint_values(joint_values)
        tool0_plane_transformed_world = ghcomp.Transform(tool0_plane_transformed, self.T_W_R)

        return tool0_plane_transformed_world

    def get_tool0_pose_from_joint_values_world(self, joint_values):
        ''' the joint values (in degrees)'''

        frame = Frame(self.get_tool0_plane_from_joint_values_world(joint_values))
        return frame.get_pose_quaternion()
