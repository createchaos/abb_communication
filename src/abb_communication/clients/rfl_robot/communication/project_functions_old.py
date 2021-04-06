# Moved from communication

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

def send_pose_joint_home(self, int_arr=None):
    """ send the "home" position as jointtarget as defined in init """
    self.send_axes_absolute(self.jointtarget_home_zero, int_arr)

def send_pose_joint_pick_brick(self, int_arr=None):
    """ send the "home" position as jointtarget as defined in init """
    self.send_axes_absolute(self.jointtarget_home_pickbrick, int_arr)

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

def set_home_pos_left_to_origin(self):
    self.tool_plane_home_left = rg.Plane(rg.Point3d(-665.507, 629.086, 720.0), rg.Vector3d(-1,0,0), rg.Vector3d(0,1,0))

def get_home_pos_left(self):
    return self.tool_plane_home_left

def get_home_pos_left_for_180(self):
    plane = rg.Plane(self.get_home_pos_left())
    plane.Translate(rg.Vector3d(1200,0,0))
    plane.Rotate(m.radians(180), plane.ZAxis, plane.Origin)
    return plane

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

def send_open_clamp(self, int_arr = None):
    " send command for opening clamp through DO"
    pose = [0,0,0,0,0,0,0,0,0,0]
    if int_arr == None:
        cmd = [CMD_OPEN_CLAMP] + pose + [0, 0, 0, 0, self.float_arbitrary, 0]
    else:
        cmd = [CMD_OPEN_CLAMP] + pose + int_arr

    self.send(MSG_COMMAND, cmd)

    _plane(self, input1, input2, ext_axes_1, ext_axes_2, int_arr=None):
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