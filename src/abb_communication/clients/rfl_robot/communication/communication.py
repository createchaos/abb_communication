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
from messages.messagetypes import CMD_SENDMOVELRELTOOL, CMD_SENDMOVELRELTCP, CMD_COORDINATED_GANTRY_MOVE, CMD_SET_SPEED_INPUT
from messages.messagetypes import CMD_OPEN_GRIPPER_ELECTRIC_1, CMD_CLOSE_GRIPPER_ELECTRIC_1, CMD_GRIPPER_ELECTRIC_POS_1, CMD_GRIPPER_ELECTRIC_REL_1, CMD_ACK_GRIPPER_ELECTRIC_1
from messages.messagetypes import CMD_OPEN_GRIPPER_ELECTRIC_2, CMD_CLOSE_GRIPPER_ELECTRIC_2, CMD_GRIPPER_ELECTRIC_POS_2, CMD_GRIPPER_ELECTRIC_REL_2, CMD_ACK_GRIPPER_ELECTRIC_2


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
        self.float_duration = 0  # duration is not used, use velocity instead
        self.int_zonedata = 10 # zonedata (in mm)
        self.int_tool = 0 # tool number
        self.int_wobj = 0 # wobj number
        self.int_rob_num = 0 # robot number to send commands to
        self.float_arbitrary = 0 # send an arbitrary float

        # home positions cartesian - to change!!!!! - stefana
        #self.tool_plane_home_mid = rg.Plane(rg.Point3d(1000,0,650), rg.Vector3d(1,0,0), rg.Vector3d(0,-1,0))
        #self.tool_plane_home_left = rg.Plane(rg.Point3d(-665.507, 629.086, 720.0), rg.Vector3d(-1,0,0), rg.Vector3d(0,1,0))

        # home positions joint targets - to change!!!! - stefana
        #self.jointtarget_home_zero = [0,0,0,0,0,0]
        #self.jointtarget_home_pickbrick = [130.9, -56.8, 58.3, 7.4, 30.1, 51.9]

        ##################################### changed stefana #########################################
        self.current_joint_values = [0,0,0,0,0,0,0,0,0]
        self.current_tool0_pose = [0,0,0,0,0,0,0,0,0,0]
        #self.ghComp = None
        self.debug_print = []
        ###############################################################################################

    # =================================================================================
    # robot convert plane to frame
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

    # Robot tool - are these still useful?

    # def set_tool_to_plane(self, plane):
    #     """ move the base to a plane position """
    #     self.tool_frame.set_to_plane(plane)

    # def get_tool_plane(self):
    #     """ return the plane of the baseframe """
    #     return self.tool_frame.plane

    # def get_tool_tmatrix_from(self):
    #     """ return the transformation matrix (Transform class of Rhino) of the baseframe to the origin """
    #     return self.tool_frame.get_tmatrix_from()

    # def get_tool_tmatrix_to(self):
    #     """ return the transformation matrix (Transform class of Rhino) of the origin to the baseframe """
    #     return self.tool_frame.get_tmatrix_to()

    # =================================================================================
    # Receive robot info
    # =================================================================================

    def get_current_pose_cartesian(self):
        """ get the current tool pose from the queue and set the tool_frame according to the pose """
        msg_current_pose_cart = self.get_from_rcv_queue(MSG_CURRENT_POSE_CARTESIAN)
        if msg_current_pose_cart != None:
            pose = msg_current_pose_cart[1]
            self.current_tool0_pose = pose
            #self.tool_frame.set_to_pose(pose)
            return pose
        else:
            return None

    def get_current_pose_cartesian_base(self):
        """ get the current tool pose from the queue in robot base coordinate system and set the tool_frame according to the pose """
        msg_current_pose_cart_base = self.get_from_rcv_queue(MSG_CURRENT_POSE_CARTESIAN_BASE)
        if msg_current_pose_cart_base != None:
            pose = msg_current_pose_cart_base[1]
            self.current_tool0_pose = pose
            #self.tool_frame.set_to_pose(pose)
            return pose
        else:
            return None

    def get_current_pose_joint(self):
        """ get the current tool pose from the queue and set the tool_frame according to the pose """
        msg_current_pose_joint = self.get_from_rcv_queue(MSG_CURRENT_POSE_JOINT)
        if msg_current_pose_joint != None:
            pose_joint = msg_current_pose_joint[1]
            self.current_joint_values = [m.degrees(pj) for pj in pose_joint]
            return pose_joint
        else:
            return None

    # =================================================================================
    # Send robot commands
    # =================================================================================

    def send_stop(self, int_arr = None):
        """ send stop to robot """
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_RAPID_STOP] + pose + [0, 0, 0, 0, self.float_arbitrary, 0]
        else:
            cmd = [CMD_RAPID_STOP] + pose + int_arr
        self.send(MSG_COMMAND, cmd)

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

    def send_axes_relative(self, axes, int_arr=None):
        """ relative joint axes commands for the abb arm """
        if int_arr:
            cmd = [CMD_GO_TO_JOINTTARGET_REL] + axes + [0] + int_arr
        else:
            cmd = [CMD_GO_TO_JOINTTARGET_REL] + axes + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, self.int_wobj]

        self.send(MSG_COMMAND, cmd)
        return cmd

    def send_axes_absolute(self, axes, int_arr=None):
        """ absolute joint axes commands for the arm """
        if int_arr:
            cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + int_arr
        else:
            # add rob_num to every function
            cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0, self.int_rob_num]
        self.send(MSG_COMMAND, cmd)

    def send_axes_absolute_list(self, axes_list, int_arr=None):
        """ absolute joint axes commands for the arm """

        for axes in axes_list:
            if int_arr:
                cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + int_arr
            else:
                cmd = [CMD_GO_TO_JOINTTARGET_ABS] + axes + [0] + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0]
            self.send(MSG_COMMAND, cmd)

    def send_movel_reltool(self, offset_axis_X, offset_axis_Y, offset_axis_Z, int_arr = None, tcp = False):
        " send command for moving relative to the tool"
        pose = [offset_axis_X, offset_axis_Y, offset_axis_Z, 0,0,0,0,0,0,0]

        # By default, this function will send a command to move relative to the current tool.
        # Here we provide a way to move relative to the TCP, which can be helpful if your tool
        # is oriented differently from the TCP.

        rel_cmd = ""
        if tcp:
            rel_cmd = [CMD_SENDMOVELRELTCP]
        else:
            rel_cmd = [CMD_SENDMOVELRELTOOL]

        if int_arr == None:
            cmd = rel_cmd + pose + [self.int_speed, self.float_duration, self.int_zonedata, self.int_tool, self.float_arbitrary, 0, self.int_rob_num]
        else:
            cmd = rel_cmd + pose + int_arr
        self.send(MSG_COMMAND, cmd)
        return cmd

    def send_open_gripper(self, int_arr = None):
        " send command for opening gripper through DO"
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_OPEN_GRIPPER] + pose + [0, 0, 0, 0, self.float_arbitrary, 0, self.int_rob_num]
        else:
            cmd = [CMD_OPEN_GRIPPER] + pose + int_arr
        self.send(MSG_COMMAND, cmd)

    def send_close_gripper(self, int_arr = None):
        " send command for closing gripper through DO"
        pose = [0,0,0,0,0,0,0,0,0,0]
        if int_arr == None:
            cmd = [CMD_CLOSE_GRIPPER] + pose + [0, 0, 0, 0, self.float_arbitrary, 0, self.int_rob_num]
        else:
            cmd = [CMD_CLOSE_GRIPPER] + pose + int_arr
        self.send(MSG_COMMAND, cmd)

    # =================================================================================
    # Electric gripper functions for Schunk IO-Link grippers
    # =================================================================================

    # Target position is mm, defined from a zero that is set during gripper referencing
    # Gripping force defined by a percentage of the maximum force: 0=100%, 1=75%, 2=50%, 3=25%

    def send_open_gripper_electric(self, gripper=1, force=0):
        "Send command for opening electric gripper through DeviceNet"
        pose = [0,0,0,0,0,0,0,0,0,0]
        # Force is passed via float_arbitrary
        if gripper == 2:
            cmd = [CMD_OPEN_GRIPPER_ELECTRIC_2] + pose + [0, 0, 0, 0, force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)
        else:
            cmd = [CMD_OPEN_GRIPPER_ELECTRIC_1] + pose + [0, 0, 0, 0, force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)

    def send_close_gripper_electric(self, gripper=1, force=0):
        "Send command for closing electric gripper through DeviceNet"
        pose = [0,0,0,0,0,0,0,0,0,0]
        # Force is passed via float_arbitrary
        if gripper == 2:
            cmd = [CMD_CLOSE_GRIPPER_ELECTRIC_2] + pose + [0, 0, 0, 0, force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)
        else:
            cmd = [CMD_CLOSE_GRIPPER_ELECTRIC_1] + pose + [0, 0, 0, 0, force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)

    def send_gripper_electric_pos(self, gripper=1, position=3.0, force=0):
        "Send command for setting electric gripper to a specific current position"
        pose = [0,0,0,0,0,0,0,0,0,0]
        # Pass relative gripper position and force via float_arbitrary.
        # The values will be separated again on the RAPID side.
        position_and_force = position + float(100*(force+1))
        print(position_and_force)
        if gripper == 2:
            cmd = [CMD_GRIPPER_ELECTRIC_POS_2] + pose + [0, 0, 0, 0, position_and_force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)
        else:
            cmd = [CMD_GRIPPER_ELECTRIC_POS_1] + pose + [0, 0, 0, 0, position_and_force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)

    def send_gripper_electric_rel(self, gripper=1, position=1.0, force=0):
        "Send command for closing electric gripper relative to its current position"
        pose = [0,0,0,0,0,0,0,0,0,0]
        # Pass relative gripper position and force via float_arbitrary.
        # The values will be separated again on the RAPID side.
        position_and_force = position + float(100*(force+1))
        if gripper == 2:
            cmd = [CMD_GRIPPER_ELECTRIC_REL_2] + pose + [0, 0, 0, 0, position_and_force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)
        else:
            cmd = [CMD_GRIPPER_ELECTRIC_REL_1] + pose + [0, 0, 0, 0, position_and_force, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)

    """
    def ack_gripper_electric(self):
        "Send command for closing electric gripper relative to its current position"
        pose = [0,0,0,0,0,0,0,0,0,0]
        # Pass relative gripper position and force via float_arbitrary.
        # The values will be separated again on the RAPID side.
        cmd = [CMD_ACK_GRIPPER_ELECTRIC] + pose + [0, 0, 0, 0, 0, 0, self.int_rob_num]
        self.send(MSG_COMMAND, cmd)
    """

    def ack_gripper_electric(self, gripper=1):
        "Send command for closing electric gripper relative to its current position"
        pose = [0,0,0,0,0,0,0,0,0,0]
        if gripper == 2:
            # pass relative gripper position as arbirary float
            cmd = [CMD_ACK_GRIPPER_ELECTRIC_2] + pose + [0, 0, 0, 0, self.float_arbitrary, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)
        else:
            cmd = [CMD_ACK_GRIPPER_ELECTRIC_1] + pose + [0, 0, 0, 0, self.float_arbitrary, 0, self.int_rob_num]
            self.send(MSG_COMMAND, cmd)

    # =================================================================================
    # Set command parameters
    # =================================================================================

    def set_rob_num(self,rob_num):
        self.int_rob_num = rob_num
        print(rob_num)

    def set_tool_to_num(self, num_tool):
        self.int_tool = num_tool

    def set_wobj_to_num(self, num_wobj):
        self.int_wobj = num_wobj

    def send_set_speed(self, speed1, speed2=10, int_arr = None):
        " send command for opening clamp through DO"
        speed = [speed1, speed2, 0, 0, 0, 0, 0, 0, 0, 0]
        if int_arr == None:
            cmd = [CMD_SET_SPEED_INPUT] + speed + [0, 0, 0, 0, self.float_arbitrary, 0, self.int_rob_num]
        else:
            cmd = [CMD_SET_SPEED_INPUT] + speed + int_arr

        self.send(MSG_COMMAND, cmd)

    def set_speed_fast(self):
        self.int_speed = 2
        self.int_zonedata = 100

    def set_speed_mid(self):
        self.int_speed = 1
        self.int_zonedata = 20

    def set_speed_slow(self):
        self.int_speed = 0
        self.int_zonedata = 10

    def set_speed_superslow(self):
        self.int_speed = 3
        self.int_zonedata = 10

# if __name__ == '__main__':
#     robot = ABBCommunication("ABB", '192.168.125.1')
#     robot.start()
#     time.sleep(1)

#     robot.set_speed_slow()
#     print (robot.get_state())

#     robot.send_pose_joint_pick_brick()

#     time.sleep(0.1)
#     print (robot.get_state())

#     while robot.get_state() <= 1:

#         #robot.send_pose_joint_home()
#         #time.sleep(0.2)
#         #robot.send_pose_joints_pick_brick()
#         time.sleep(0.01)
#         current_pose_joints = robot.get_current_pose_joint()
#         print( current_pose_joints)
#         print( robot.cmd_exec_counter_from_client)
#         print( robot.cmd_counter_to_client)

#     print( "comd sent: ", robot.cmd_counter_to_client)
#     print( "cmd exec: ", robot.cmd_exec_counter_from_client)
#     print( "state: ", robot.get_state())
#     print ("ready")
#     robot.close()
#     print ("closed")
