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

from compas.geometry import Frame

from client_container import ClientContainer
from messages.messagetypes import MSG_CURRENT_POSE_CARTESIAN, MSG_CURRENT_POSE_JOINT, MSG_CURRENT_POSE_CARTESIAN_BASE, MSG_COMMAND, MSG_STOP
from messages.messagetypes import CMD_PICK_ROD, CMD_MILL_ROD_END, CMD_MILL_ROD_START, CMD_REGRIP_PLACE, CMD_REGRIP_PICK, CMD_SAFE_POS, CMD_OPEN_GRIPPER, CMD_CLOSE_GRIPPER, CMD_OPEN_CLAMP
from messages.messagetypes import CMD_GO_TO_TASKTARGET, CMD_GO_TO_TASKTARGET_JOINTS, CMD_GO_TO_JOINTTARGET_ABS, CMD_GO_TO_JOINTTARGET_REL, CMD_PICK_BRICK, CMD_PLACE_BRICK, CMD_PICK_BRICK_FROM_POSE
from messages.messagetypes import CMD_STU_PICK, CMD_STU_PLACE_1, CMD_STU_PLACE_2
from messages.messagetypes import CMD_MAS_PICK, CMD_MAS_PLACE, CMD_MAS_PICK_MAGAZINE, CMD_MAS_PLACE_MAGAZINE, CMD_LWS_DYNAMIC_PICKUP, CMD_RAPID_STOP, CMD_PULSEDO
from messages.messagetypes import CMD_SENDMOVELRELTOOL, CMD_COORDINATED_GANTRY_MOVE, CMD_SET_SPEED_INPUT

import time
import Rhino.Geometry as rg
import math as m

DEFAULT_AXES = [10000,10000,10000]


class ABBCommunication(ClientContainer):
    """ The class ABBComm extends the Clientcontainer class.
    It can send and receive data from the ABB arm

    """

    def __init__(self, identifier, host='127.0.0.1', port_snd=30003, port_rcv=30004, ghenv = None):
        ClientContainer.__init__(self,  identifier, host, port_snd, port_rcv, ghenv = ghenv)

        " create "
        self.tool_frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
        # init values for command messages
        self.int_speed = 0 # speed: 0 = slow, 1 = mid, 2 = fast
        self.float_duration = 0 #duration is not used, use velocity instead
        self.int_zonedata = 10 # zonedata: in mm
        self.int_tool = 0 # toolnumber: 0 = tool0, 1 = vacgrip_vert, 2 = hokuyo
        self.int_wobj = 0 # wobjnumber: 0 = wobj0, 1 = wobj_common, 2 = wobj_base
        self.int_rob_num = 0
        self.float_arbitrary = 0 #robot number to access

        # home positions cartesian - to change!!!!! - stefana
        self.tool_plane_home_mid = rg.Plane(rg.Point3d(1000,0,650), rg.Vector3d(1,0,0), rg.Vector3d(0,-1,0))
        self.tool_plane_home_left = rg.Plane(rg.Point3d(-665.507, 629.086, 720.0), rg.Vector3d(-1,0,0), rg.Vector3d(0,1,0))

        # home positions joint targets - to change!!!! - stefana
        self.jointtarget_home_zero = [0,0,0,0,0,0]
        self.jointtarget_home_pickbrick = [130.9, -56.8, 58.3, 7.4, 30.1, 51.9]

        ##################################### changed stefana #########################################
        self.current_joint_values = [0,0,0,0,0,0,0,0,0]
        self.current_tool0_pose = [0,0,0,0,0,0,0,0,0,0]
        #self.ghComp = None
        self.debug_print = []
        ###############################################################################################
    # =================================================================================
    # robot convert plane to frame
    # =================================================================================
    # =================================================================================
    def get_pose(self, input):
        if isinstance(input, rg.Plane):
            frame = Frame(input.Origin, input.XAxis, input.YAxis)
            pose = frame.point.data + frame.quaternion.wxyz
        else:
            pose = input.point.data + input.quaternion.wxyz
        return pose
    # =================================================================================
    # sets external axis
    # =================================================================================
    # =================================================================================
    def get_ext_axes(self, ext_axes_in):
        if type(ext_axes_in) == list or type(ext_axes_in) == tuple:
            if len(ext_axes_in) == 1:
                ext_axes = [ext_axes_in[0], 0, 0]
            elif len(ext_axes_in) == 2:
                ext_axes = [ext_axes_in[0], ext_axes_in[1], 0]
            elif len(ext_axes_in) == 3:
                ext_axes = ext_axes_in
            else:
                print("too many values for external axes (maximum number = 3)... first 3 values accepted")
                ext_axes = (ext_axes_in)[:3]
        else:
            print("wrong data type for external axes value")
        return ext_axes

    def get_ext_axes_list(self, ext_axes_in, inputs):
        nested_list = False

        ext_axes_list = []

        checked = False

        unexpect_list = False

        shortList = False
        try:
            if not (type(ext_axes_in[0]) == list or type(ext_axes_in[0]) == tuple):
                for value in ext_axes_in:
                    if type(value) == list or type(value) == tuple:
                        print("unexpected nested list... using default axis")
                        unexpect_list = True
                        break
                for i, input in enumerate(inputs):
                    if unexpect_list:
                        ext_axes_list.append(DEFAULT_AXES)
                    else:
                        ext_axes_list.append(self.get_ext_axes(ext_axes_in))

            else:
                for i, input in enumerate(inputs):
                    try:
                        if type(ext_axes_in[i]) == list or type(ext_axes_in[i]) == tuple:
                            nested_list = True
                            ext_axes_list.append(self.get_ext_axes(ext_axes_in[i]))
                        else:
                            if nested_list and not checked:
                                print("data type varies after " + str(i) + "... default ext_axes applied after index.")
                                checked = True
                                ext_axes_list.append(DEFAULT_AXES)
                            elif nested_list:
                                ext_axes_list.append(DEFAULT_AXES)
                            else:
                                ext_axes_list.append(self.get_ext_axes(ext_axes_in))
                    except:
                        if not shortList:
                            shortList = True
                            print("List too short... after " + str(i) + "... default ext_axes applied after index.")
                        ext_axes_list.append(DEFAULT_AXES)
            return ext_axes_list
        except:
            print("wrong data type for external axes value - list required")

    # =================================================================================
    # robot tool
    # =================================================================================
    # =================================================================================
    def set_tool_to_plane(self, plane):
        """ move the base to a plane position """
        self.tool_frame.set_to_plane(plane)
    # =================================================================================
    def get_tool_plane(self):
        """ return the plane of the baseframe """
        return self.tool_frame.plane
    # =================================================================================
    def get_tool_tmatrix_from(self):
        """ return the transformation matrix (Transform class of Rhino) of the baseframe to the origin """
        return self.tool_frame.get_tmatrix_from()
    # =================================================================================
    def get_tool_tmatrix_to(self):
        """ return the transformation matrix (Transform class of Rhino) of the origin to the baseframe """
        return self.tool_frame.get_tmatrix_to()


    # =================================================================================
    # receive robot info from queues
    # =================================================================================
    # =================================================================================

    def get_current_pose_cartesian(self):
        """ get the current tool pose from the queue and set the tool_frame according to the pose """
        msg_current_pose_cart = self.get_from_rcv_queue(MSG_CURRENT_POSE_CARTESIAN)
        if msg_current_pose_cart <> None:
            pose = msg_current_pose_cart[1]
            self.current_tool0_pose = pose
            #self.tool_frame.set_to_pose(pose)
            return pose
        else:
            return None

    # =================================================================================
    def get_current_pose_cartesian_base(self):
        """ get the current tool pose from the queue in robot base coordinate system and set the tool_frame according to the pose """
        msg_current_pose_cart_base = self.get_from_rcv_queue(MSG_CURRENT_POSE_CARTESIAN_BASE)
        if msg_current_pose_cart_base <> None:
            pose = msg_current_pose_cart_base[1]
            self.current_tool0_pose = pose
            #self.tool_frame.set_to_pose(pose)
            return pose
        else:
            return None

    # =================================================================================
    def get_current_pose_joint(self):
        """ get the current tool pose from the queue and set the tool_frame according to the pose """
        msg_current_pose_joint = self.get_from_rcv_queue(MSG_CURRENT_POSE_JOINT)
        if msg_current_pose_joint <> None:
            pose_joint = msg_current_pose_joint[1]
            self.current_joint_values = [m.degrees(pj) for pj in pose_joint]
            return pose_joint
        else:
            return None


    # =================================================================================
    # send robot commands
    # =================================================================================
    # =================================================================================
    def send_stop(self, int_arr = None):
        """ send stop to robot """
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_RAPID_STOP] + pose + [0, 0, 0, 0, self.float_arbitrary, 0]
        else:
            cmd = [CMD_RAPID_STOP] + pose + int_arr
        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_single_move_command(self, input, ext_axes, num_cmd, int_arr = None):
        """ create command from plane, frame or joint values and send to robot
        num_cmd = number of command in rapid
        """

        if isinstance(input, list):
            if len(input)==6:
                pose_axes = input + ext_axes + [0]
            else:
                print( "length of input not correct")
        else:
            pose = self.get_pose(input)
            pose_axes = pose + ext_axes
            self.debug_print = pose_axes

        if int_arr == None:
            cmd = [num_cmd] + pose_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [num_cmd] + pose_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    # =================================================================================
    def send_pose_cartesian(self, input, ext_axes_in = DEFAULT_AXES, int_arr=None):
        """ create command from plane or frame and send task target to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj]
        ext_axes values are optional, either in list format or as single float value for only one axis"""
        
        pose = self.get_pose(input)

        ext_axes = self.get_ext_axes(ext_axes_in)


        if int_arr == None:
            cmd = [CMD_GO_TO_TASKTARGET] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj, self.int_rob_num]
        else:
            cmd = [CMD_GO_TO_TASKTARGET] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    # =================================================================================
    def send_pose_cartesian_joints(self, input, ext_axes_in = DEFAULT_AXES, int_arr=None):
        """ create command from plane or frame and send task target to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj]
        ext_axes values are optional, either in list format or as single float value for only one axis"""

        pose = self.get_pose(input)

        ext_axes = self.get_ext_axes(ext_axes_in)

        if int_arr == None:
            cmd = [CMD_GO_TO_TASKTARGET_JOINTS] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_GO_TO_TASKTARGET_JOINTS] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    # =================================================================================
    def send_pose_quat(self, pose, ext_axes_in= DEFAULT_AXES, int_arr=None):
        """ create command from pose quaternions and send task target to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj]
        ext_axes values are optional, either in list format or as single float value for only one axis"""

        pose = self.get_pose(input)

        ext_axes = self.get_ext_axes(ext_axes_in)

        if int_arr == None:
            cmd = [CMD_GO_TO_TASKTARGET] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_GO_TO_TASKTARGET] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    # =================================================================================
    def send_pose_cartesian_list(self, inputs, ext_axes_in=DEFAULT_AXES, int_arr=None):
        """ create command from planes or frames and send task targets to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary] """

        #####################################add case with single value list ####################################################

        ext_axes_list = self.get_ext_axes_list(ext_axes_in,inputs)
        print (ext_axes_list)
        for i, input in enumerate(inputs):
            self.send_pose_cartesian(input, ext_axes_list[i], int_arr)

        # =================================================================================

    def send_pose_cartesian_joints_list(self, planes, ext_axes_list, int_arr=None):
        """ create command from plane and send task target to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary] """

        for i, plane in enumerate (planes):
            self.send_pose_cartesian_joints(plane, ext_axes_list[i], int_arr)

    # =================================================================================
    def send_axes_relative(self, axes, int_arr=None):
        """ relative joint axes commands for the abb arm """
        if int_arr:
            cmd = [CMD_GO_TO_JOINTTARGET_REL] + axes + [0] + int_arr
        else:
            cmd = [CMD_GO_TO_JOINTTARGET_REL] + axes + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]

        self.send(MSG_COMMAND, cmd)
        return cmd
    # =================================================================================
    def send_axes_absolute(self, axes, int_arr=None):
        """ absolute joint axes commands for the arm """
        if int_arr:
            cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + int_arr
        else:
            # add rob_num to every function
            cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0, self.int_rob_num]
        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_axes_absolute_list(self, axes_list, int_arr=None):
        """ absolute joint axes commands for the arm """

        for axes in axes_list:
            if int_arr:
                cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + int_arr
            else:
                cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0]
            self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_movel_reltool(self, offset_axis_X, offset_axis_Y, offset_axis_Z, int_arr = None):
        " send command for opening gripper through DO"
        pose = [offset_axis_X, offset_axis_Y, offset_axis_Z, 0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_SENDMOVELRELTOOL] + pose + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0]
        else:
            cmd = [CMD_SENDMOVELRELTOOL] + pose + int_arr
        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_coordinated_gantry_move(self, pose, ext_axes, int_arr=None):
        """coordinated movement of two robots on a gantry.
        Send the same procedure to both robots at the same time, and they will sync their movements.
        Important: send the same X ganrty value!"""
        if int_arr == None:
            cmd = [CMD_COORDINATED_GANTRY_MOVE] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0]
        else:
            cmd = [CMD_COORDINATED_GANTRY_MOVE] + pose + ext_axes + int_arr

        print ("send_coordinated_gantry_move sent to Rapid!"), CMD_COORDINATED_GANTRY_MOVE
        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_pose_cartesian_home(self, int_arr=None):
        """ send the "home" position as task target as defined in init """
        self.send_pose_cartesian(self.tool_plane_home_mid, int_arr)

    # =================================================================================
    def send_pose_joint_home(self, int_arr=None):
        """ send the "home" position as jointtarget as defined in init """
        self.send_axes_absolute(self.jointtarget_home_zero, int_arr)

    # =================================================================================
    def send_pose_joint_pick_brick(self, int_arr=None):
        """ send the "home" position as jointtarget as defined in init """
        self.send_axes_absolute(self.jointtarget_home_pickbrick, int_arr)

    # =================================================================================
    def send_pick_brick_from_pose(self, plane, int_arr=None):
        """ send a command for picking up the material and go to the given plane or frame
        sequence:
        1. drive from actual pos to pick up the brick at the given plane
        (== >> this routine is defined in RobotStudio, the command consist only out of the pick-up plane.
        """

        pose = self.get_pose(input)

        if int_arr == None:
            cmd = [CMD_PICK_BRICK_FROM_POSE] + pose + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_PICK_BRICK_FROM_POSE] + pose + int_arr
        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_pick_brick_from_feed(self, fullbrick = True, int_arr=None):
        """ send a command for picking up the material and go to the given plane sequence:
        1. drive from actual pos to the homeposition, defined as jointtarget, on the left side of the robot.
        2. go on the trajectory to pick up a brick from the feeder and drive back to the homeposition
        == >> this routine is defined in RobotStudio, the command consist only out of the homeposition.
        cmd = [CMD_PICK_BRICK, joints, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary] float_arbitrary => 0 = fullbrick  / 1 = halfbrick
        """

        jointpose = self.jointtarget_home_pickbrick
        float_arbitrary = 0 if fullbrick == True else 1 #this parameter has to read in Rapid, to either pick a fullbrick or a halfbrick

        if int_arr == None:
            cmd = [CMD_PICK_BRICK] + jointpose + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_PICK_BRICK] + jointpose + [0] + int_arr

        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    def send_place_brick(self, input, send_pick_brick_from_feed = True, fullbrick = True, int_arr = None):
        """ send a command for placing the material at the given plane or frame
        sequence:
        1. drive to home_pos, pick a brick and drive back to homepos
        1. drive from home pos to the a point 20 cm above the given plane
        2. go on the trajectory to place the brick and drive back to a point 20 cm above the given plane
        == >> this routine is defined in RobotStudio, and is defined
        cmd = [x,y,z,q1,q2,q3,q4,int_speed, int_zonedata, int_proc] int_proc = 3 = place the brick

        cmd = [CMD_PICK_BRICK, robtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]
        """
        if send_pick_brick_from_feed:
            self.send_pick_brick_from_feed(fullbrick, int_arr)

        pose = self.get_pose(input)


        if int_arr == None:
            cmd = [CMD_PLACE_BRICK] + pose + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_PLACE_BRICK] + pose + int_arr

        self.send(MSG_COMMAND, cmd)


    # =================================================================================
    def set_home_pos_left_to_origin(self):
        self.tool_plane_home_left = rg.Plane(rg.Point3d(-665.507, 629.086, 720.0), rg.Vector3d(-1,0,0), rg.Vector3d(0,1,0))

    # =================================================================================
    def get_home_pos_left(self):
        return self.tool_plane_home_left

    # =================================================================================
    def get_home_pos_left_for_180(self):
        plane = rg.Plane(self.get_home_pos_left())
        plane.Translate(rg.Vector3d(1200,0,0))
        plane.Rotate(m.radians(180), plane.ZAxis, plane.Origin)
        return plane

    # =================================================================================
    # functions Stefana
    # =================================================================================

    def send_pick_rod_from_feed(self, input, ext_axes, int_arr = None):
        """ send a command for picking a rod from the feeder
        sequence:
        1. drive to safe_pos_pick
        2. open gripper
        3. drive to pick up position
        4. close gripper
        5. drive to safe position up
        == >> this routine is defined in RobotStudio, and is defined
        cmd = [x,y,z,q1,q2,q3,q4,int_speed, int_zonedata, int_proc] int_proc = 7

        cmd = [CMD_PICK_ROD, robtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]"""

        pose = self.get_pose(input)



        if int_arr == None:
            cmd = [CMD_PICK_ROD] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_PICK_ROD] + pose + ext_axes + int_arr



        self.send(MSG_COMMAND, cmd)


    def send_mill_rod(self, input1, input2, ext_axes1, ext_axes2, jointpos_1, jointpos_2, int_arr=None):

        self.send_axes_absolute(jointpos_1, int_arr)
        self.send_axes_absolute(jointpos_2, int_arr)

        pose_1 = get_pose(self, input1)

        if int_arr == None:
            cmd = [CMD_MILL_ROD_START] + pose_1 + ext_axes1 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MILL_ROD_START] + pose_1 + ext_axes1 + int_arr

        self.send(MSG_COMMAND, cmd)

        pose_2 = get_pose(self, input2)

        if int_arr == None:
            cmd = [CMD_MILL_ROD_END] + pose_2 + ext_axes2 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MILL_ROD_END] + pose_2 + ext_axes2 + int_arr

        self.send(MSG_COMMAND, cmd)

        return pose_1

    def send_mill_rod3(self, plane1, plane2, ext_axes1, ext_axes2, jointpos_1, jointpos_2, int_arr=None):
        """ send a command for millig a rod
        sequence:
        1. drive to safe position for milling
        2. set velocity to superslow
        3. drive through milling planes
        4. set velocity to normal
        5. drive to safe position up
        == >> this routine is defined in RobotStudio, and is defined
        cmd = [x,y,z,q1,q2,q3,q4,int_speed, int_zonedata, int_proc] int_proc = 8, int_proc = 9

        cmd = [CMD_MILL_ROD_START, robtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]
        cmd = [CMD_MILL_ROD_END, robtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]"""

        return ("before anything python")

        self.send_axes_absolute(jointpos_1, int_arr)
        self.send_axes_absolute(jointpos_2, int_arr)

        #return "axes_sent"

        plane_local_1 = self.set_tool_to_plane_sysworld(rg.Plane(plane1))
        plane_local_1 = self.get_tool_plane_local()
        #plane_local_1 = plane1
        pose_1 = get_pose(self, plane_local_1)

        if int_arr == None:
            cmd = [CMD_MILL_ROD_START] + pose_1 + ext_axes1 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MILL_ROD_START] + pose_1 + ext_axes1 + int_arr

        self.send(MSG_COMMAND, cmd)

        plane_local_2 = self.set_tool_to_plane_sysworld(rg.Plane(plane2))
        plane_local_2 = self.get_tool_plane_local()
        #plane_local_2 = plane2
        pose_2 = get_pose(self, plane_local_2)

        if int_arr == None:
            cmd = [CMD_MILL_ROD_END] + pose_2 + ext_axes2 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MILL_ROD_END] + pose_2 + ext_axes2 + int_arr

        self.send(MSG_COMMAND, cmd)

    def send_regrip_rod(self, input1, input2, ext_axes1, ext_axes2, int_arr=None):
        """ send a command for regripping a rod
        sequence:

        == >> this routine is defined in RobotStudio, and is defined
        cmd = [x,y,z,q1,q2,q3,q4,int_speed, int_zonedata, int_proc] int_proc = 10, int_proc = 11

        cmd = [CMD_MILL_ROD_START, robtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]
        cmd = [CMD_MILL_ROD_END, robtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]"""

        pose = get_pose(self, input1)

        if int_arr == None:
            cmd = [CMD_REGRIP_PLACE] + pose + ext_axes1 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_REGRIP_PLACE] + pose + ext_axes1 + int_arr

        self.send(MSG_COMMAND, cmd)

        pose = get_pose(self, input2)

        if int_arr == None:
            cmd = [CMD_REGRIP_PICK] + pose + ext_axes2 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_REGRIP_PICK] + pose + ext_axes2 + int_arr

        self.send(MSG_COMMAND, cmd)

        return "regrip done"

    def send_move_to_safe_pos(self, joint_vals, int_arr=None):
        """ send a command for moving to safe position
        sequence:

        == >> this routine is defined in RobotStudio, and is defined
        cmd = [x,y,z,q1,q2,q3,q4,int_speed, int_zonedata, int_proc] int_proc = 12

        cmd = [CMD_SAFE_POS, jointtarget, int_speed, float_duration, int_zonedata, int_tool, float_arbitrary]"""


        if int_arr == None:
            cmd = [CMD_SAFE_POS] + joint_vals + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0]
        else:
            cmd = [CMD_SAFE_POS] + joint_vals + [0] + int_arr

        self.send(MSG_COMMAND, cmd)


    def send_position_rod(self, joint_vals, plane, ext_axes, int_arr=None):

        self.send_axes_absolute_list(joint_vals, int_arr)
        self.send_pose_cartesian(plane, ext_axes, int_arr)

    def send_pick_and_pos_rod(self, joint_pick_1, joint_pick_2, joint_vals, plane, ext_axes, int_arr=None):

        self.send_open_gripper(int_arr)
        self.send_axes_absolute(joint_pick_1, int_arr)
        self.send_close_gripper(int_arr)
        self.send_open_clamp(int_arr)
        self.send_axes_absolute(joint_pick_2, int_arr)
        self.send_axes_absolute_list(joint_vals, int_arr)
        self.send_pose_cartesian(plane, ext_axes, int_arr)

        #return "picked and positioned"

    def send_pick_pos(self, joint_pick_1, joint_pick_2, joint_vals, plane, ext_axes, int_arr=None):

        self.send_open_gripper(int_arr)
        self.send_axes_absolute(joint_pick_1, int_arr)
        self.send_axes_absolute(joint_pick_2, int_arr)
        self.send_close_gripper(int_arr)
        self.send_open_clamp(int_arr)
        self.send_axes_absolute(joint_pick_1, int_arr)

        joint_pick_3 = [joint_pick_1[0], joint_pick_1[1], joint_pick_1[2]+30, joint_pick_1[3], joint_pick_1[4], joint_pick_1[5], joint_pick_1[6], joint_pick_1[7], joint_pick_1[8]]

        self.send_axes_absolute(joint_pick_3, int_arr)

    def send_move_back(self, joint_vals, joint_vals_safe, int_arr=None):
        self.send_open_gripper(int_arr)
        self.send_axes_absolute_list(joint_vals, int_arr)
        self.send_axes_absolute(joint_vals_safe, int_arr)


    def dynamic_pickup(self, floor_distance, pipe_length, int_arr = None):
        " send command for calling the dynamic pickup procedure"
        pose = [floor_distance, pipe_length, 0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_LWS_DYNAMIC_PICKUP] + pose + [0, 0, 0, 0, self.float_arbitrary, 0]
        else:
            cmd = [CMD_LWS_DYNAMIC_PICKUP] + pose + int_arr
        self.send(MSG_COMMAND, cmd)


    def send_PulseDO(self, signal_do, pulse_length, high, int_arr = None):
        """ PulseDO is used to generate a pulse on a digital output signal.
        signal_do: The name of the signal on which a pulse is to be generated.
        pulse_length: The length of the pulse in seconds (0.001 - 2000 s). If the argument is omitted a 0.2 second pulse is generated.
        high: Specifies that the signal value should always be set to high (value 1) when the instruction is executed independently of its current state.
        """
        pose = [signal_do, pulse_length, high, 0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_PULSEDO] + pose + [0, 0, 0, 0, self.float_arbitrary, 0]
        else:
            cmd = [CMD_PULSEDO] + pose + int_arr
        self.send(MSG_COMMAND, cmd)


    def send_open_gripper(self, int_arr = None):
        " send command for opening gripper through DO"
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_OPEN_GRIPPER] + pose + [0, 0, 0, 0, self.float_arbitrary, 0, 1]
        else:
            cmd = [CMD_OPEN_GRIPPER] + pose + int_arr
        self.send(MSG_COMMAND, cmd)


    def send_open_clamp(self, int_arr = None):
        " send command for opening clamp through DO"
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_OPEN_CLAMP] + pose + [0, 0, 0, 0, self.float_arbitrary, 0]
        else:
            cmd = [CMD_OPEN_CLAMP] + pose + int_arr

        self.send(MSG_COMMAND, cmd)

    def send_set_speed(self, speed1, speed2=10, int_arr = None):
        " send command for opening clamp through DO"
        speed = [speed1,speed2,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_SET_SPEED_INPUT] + speed + [0, 0, 0, 0, self.float_arbitrary, 0]
        else:
            cmd = [CMD_SET_SPEED_INPUT] + speed + int_arr

        self.send(MSG_COMMAND, cmd)


    def send_close_gripper(self, int_arr = None):
        " send command for closing gripper through DO"
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_CLOSE_GRIPPER] + pose + [0, 0, 0, 0, self.float_arbitrary, 0, 1]
        else:
            cmd = [CMD_CLOSE_GRIPPER] + pose + int_arr

        self.send(MSG_COMMAND, cmd)

    # ========================== funcions andreas ===============================================
    def send_stu_pick(self, input, ext_axes, int_arr=None):
        """ create command from plane or frame and send pick command to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj] """

        pose = self.get_pose(input)
        if int_arr == None:
            cmd = [CMD_STU_PICK] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_STU_PICK] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    def send_stu_place_plane(self, input1, input2, ext_axes_1, ext_axes_2, int_arr=None):
        """ create command from plane or frame and send pick command to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj] """

        pose_1 = get_pose(self, input1)
        if int_arr == None:
            cmd = [CMD_STU_PLACE_1] + pose_1 + ext_axes_1 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_STU_PLACE_1] + pose_1 + ext_axes_1 + int_arr

        self.send(MSG_COMMAND, cmd)

        pose_2 = get_pose(self, input2)
        if int_arr == None:
            cmd = [CMD_STU_PLACE_2] + pose_2 + ext_axes_2 + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_STU_PLACE_2] + pose_2 + ext_axes_2 + int_arr

        self.send(MSG_COMMAND, cmd)


    # ========================== funcions MAS ===============================================
    def send_mas_pick_brick_plane(self, input, ext_axes, int_arr=None):
        """ create command from plane or frame and send pick command to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj] """

        pose = self.get_pose(input)

        if int_arr == None:
            cmd = [CMD_MAS_PICK] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MAS_PICK] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    def send_mas_place_brick_plane(self, input, ext_axes, int_arr=None):
        """ create command from plane or frame and send place command to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj] """
        pose = self.get_pose(input)

        if int_arr == None:
            cmd = [CMD_MAS_PLACE] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MAS_PLACE] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd


    def send_mas_pick_brick_magazine(self, input, ext_axes, int_arr=None):
        """ create command from plane or frame and send pick command to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj] """

        pose = self.get_pose(input)


        if int_arr == None:
            cmd = [CMD_MAS_PICK_MAGAZINE] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MAS_PICK_MAGAZINE] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    def send_mas_place_brick_magazine(self, input, ext_axes, int_arr=None):
        """ create command from plane or frame and send place command to robot,
        int_arr can be defined outside, or if None, default values are sent.
        int_arr = [int_speed, float_duration, int_zonedata, int_tool, float_arbitrary, int_wobj] """

        pose = self.get_pose(input)
        if int_arr == None:
            cmd = [CMD_MAS_PLACE_MAGAZINE] + pose + ext_axes + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]
        else:
            cmd = [CMD_MAS_PLACE_MAGAZINE] + pose + ext_axes + int_arr

        self.send(MSG_COMMAND, cmd)
        return cmd

    # =================================================================================
    # set command parameters (for int_arr)
    # =================================================================================
    # =================================================================================
    def set_speed_fast(self):
        self.int_speed = 2
        self.int_zonedata = 100
    # =================================================================================
    def set_speed_mid(self):
        self.int_speed = 1
        self.int_zonedata = 20
    # =================================================================================
    def set_speed_slow(self):
        self.int_speed = 0
        self.int_zonedata = 10
    # =================================================================================
    #added - stefana
    def set_speed_superslow(self):
        self.int_speed = 3
        self.int_zonedata = 10

    # =================================================================================
    def set_rob_num(self,rob_num):
        self.int_rob_num = rob_num
        print(rob_num)

    # =================================================================================
    def set_tool_to_num(self, num_tool):
        self.int_tool = num_tool

    # def set_tool0(self):
    #     # toolnumber: 0 = tool0, 1 = vacgrip_vert, 2 = hokuyo
    #     self.int_tool = 0
    # # =================================================================================
    # def set_tool_meshmould(self):
    #     # toolnumber: 0 = tool0, 1 = meshmould, 2 = hokuyo
    #     self.int_tool = 1
    # # =================================================================================
    # def set_tool_lrf(self):
    #     # toolnumber: 0 = tool0, 1 = vacgrip_vert, 2 = hokuyo
    #     self.int_tool = 2
    # # =================================================================================
    # def set_tool_concrete_surface(self, ttype="puncher"):
    #     # toolnumber: 0 = tool0, 1 = meshmould, 2 = hokuyo, 3 = puncher, 4 = roller, 5 = sweeper
    #     if ttype == "puncher":
    #         self.int_tool = 3
    #     elif ttype == "roller":
    #         self.int_tool = 4
    #     else: # ttype = "sweeper"
    #         self.int_tool = 5
    # # =================================================================================
    # def set_tool_mtip(self):
    #     # toolnumber: 0 = tool0, 1 = meshmould, 2 = hokuyo
    #     self.int_tool = 6

    # #################### tools stefana #######################
    # def set_tool_lws_gripper(self):
    #     self.int_tool = 7

    # def set_tool_stu_gripper(self):
    #     self.int_tool = 8

    # def set_tool_mas_gripper(self):
    #     self.int_tool = 9

    # def set_tool_mas_magazine(self):
    #     self.int_tool = 10
    ###########################################################

    # =================================================================================
    # def set_wobj_0(self):
    #     self.int_wobj = 0
    # # =================================================================================
    # def set_wobj_common(self):
    #     self.int_wobj = 1
    # # =================================================================================
    # def set_wobj_base(self):
    #     self.int_wobj = 2

    # =================================================================================
    # Edvard add for ARC574
    def set_wobj_to_num(self, num_wobj):
        self.int_wobj = num_wobj

    # =============================== workobjects Andreas =============================
    # def set_wobj_stu_pick(self):
    #     self.int_wobj = 3

    # def set_wobj_stu_base(self):
    #     self.int_wobj = 4


if __name__ == '__main__':
    robot = ABBCommunication("ABB", '192.168.125.1')
    robot.start()
    time.sleep(1)

    robot.set_speed_slow()
    print (robot.get_state())

    robot.send_pose_joint_pick_brick()

    time.sleep(0.1)
    print (robot.get_state())

    while robot.get_state() <= 1:

        #robot.send_pose_joint_home()
        #time.sleep(0.2)
        #robot.send_pose_joints_pick_brick()
        time.sleep(0.01)
        current_pose_joints = robot.get_current_pose_joint()
        print( current_pose_joints)
        print( robot.cmd_exec_counter_from_client)
        print( robot.cmd_counter_to_client)

    print( "comd sent: ", robot.cmd_counter_to_client)
    print( "cmd exec: ", robot.cmd_exec_counter_from_client)
    print( "state: ", robot.get_state())
    """
    robot.send_pose_joint_home()


    time.sleep(0.1)

    print robot.get_state()

    while robot.get_state() <> 1:

        #robot.send_pose_joint_home()
        #time.sleep(0.2)
        #robot.send_pose_joints_pick_brick()
        time.sleep(0.01)
        current_pose_joints = robot.get_current_pose_joint()
        print current_pose_joints

    robot.wait_for_state_ready(0.0)

    robot.set_speed_slow()"""

    print ("ready")
    robot.close()
    print ("closed")
