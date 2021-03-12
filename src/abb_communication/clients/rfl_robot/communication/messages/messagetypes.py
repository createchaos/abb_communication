'''
// /////////////////////////////////////
// Created on 06.09.2015

@author: DORF_RUST
// /////////////////////////////////////
'''

#===============================================================================
# MESSAGE TYPES ARM
#===============================================================================

""" Message Types for sending and receiving messages from the clients
Message always consists of uint4: length of message, uint4: type of message, message (depends on the specific kind) """

MSG_INVALID = 0

MSG_COMMAND = 1 # [cmd_type, val1-val7 (joint or robtarget), velocity, duration, zone, tool, arbitrary]
MSG_STOP = 2
MSG_IDLE = 3
MSG_COMMAND_RECEIVED = 4 # [counter]
MSG_CURRENT_POSE_CARTESIAN = 5 # [position, orientation]
MSG_CURRENT_POSE_JOINT = 6 # [j1, j2, j3, j4, j5, j6]
MSG_STRING = 7 # [string]
MSG_FLOAT_LIST = 8 # [float, float, ...]
MSG_OPERATION = 9 # [string] (the name of the operation)
MSG_ACTUATOR_INIT = 10 # tool[position, orientation] + base[position, orientation]
MSG_ANALOG_IN = 11
MSG_ANALOG_OUT = 12
MSG_DIGITAL_IN = 13
MSG_DIGITAL_OUT = 14
MSG_COMMAND_EXECUTED = 15
MSG_IDENTIFIER = 16
MSG_CURRENT_POSE_CARTESIAN_BASE = 17


arm_msg_types_str_array = ["MSG_INVALID","MSG_COMMAND", "MSG_STOP", "MSG_IDLE", "MSG_COMMAND_RECEIVED", \
                            "MSG_CURRENT_POSE_CARTESIAN", "MSG_CURRENT_POSE_JOINT", "MSG_STRING", \
                            "MSG_FLOAT_LIST", "MSG_OPERATION","MSG_ACTUATOR_INIT", "MSG_ANALOG_IN", \
                            "MSG_ANALOG_OUT", "MSG_DIGITAL_IN", "MSG_DIGITAL_OUT", "MSG_COMMAND_EXECUTED", \
                            "MSG_IDENTIFIER"]

#===============================================================================
# COMMAND TYPES ARM
#===============================================================================

CMD_IDLE_MODE = 0
CMD_GO_TO_JOINTTARGET_ABS = 1
CMD_GO_TO_TASKTARGET = 2
CMD_PICK_BRICK = 3
CMD_PLACE_BRICK = 4
CMD_GO_TO_JOINTTARGET_REL = 5
CMD_PICK_BRICK_FROM_POSE = 6

#Commands Stefana

CMD_PICK_ROD = 7
CMD_MILL_ROD_START = 8
CMD_MILL_ROD_END = 9
CMD_REGRIP_PLACE = 10
CMD_REGRIP_PICK = 11
CMD_SAFE_POS = 12
CMD_OPEN_GRIPPER = 13
CMD_CLOSE_GRIPPER = 14
CMD_OPEN_CLAMP = 15
CMD_CLOSE_CLAMP = 16
CMD_GO_TO_TASKTARGET_JOINTS = 17
CMD_STU_PICK = 18
CMD_STU_PLACE_1 = 19
CMD_STU_PLACE_2 = 20

CMD_MAS_PICK = 21
CMD_MAS_PLACE = 22
CMD_MAS_PICK_MAGAZINE = 23
CMD_MAS_PLACE_MAGAZINE = 24

CMD_LWS_DYNAMIC_PICKUP = 27
CMD_RAPID_STOP = 28
CMD_PULSEDO = 29
CMD_SENDMOVELRELTOOL = 31
CMD_SENDMOVELRELTCP = 32
CMD_COORDINATED_GANTRY_MOVE = 33

CMD_SET_SPEED_INPUT = 50


arm_cmd_types_str_array = ["CMD_IDLE_MODE", "CMD_GO_TO_JOINTTARGET_ABS", "CMD_GO_TO_TASKTARGET", \
                           "CMD_PICK_BRICK", "CMD_PLACE_BRICK", "CMD_GO_TO_JOINTTARGET_REL", \
                           "CMD_PICK_BRICK_FROM_POSE", "CMD_PICK_ROD", "CMD_MILL_ROD_START", \
                           "CMD_MILL_ROD_END", "CMD_REGRIP_PLACE", "CMD_REGRIP_PICK", "CMD_SAFE_POS", \
                           "CMD_OPEN_GRIPPER", "CMD_CLOSE_GRIPPER", "CMD_OPEN_CLAMP", "CMD_CLOSE_CLAMP", \
                           "CMD_GO_TO_TASKTARGET_JOINTS", "CMD_STU_PICK", "CMD_STU_PLACE_1", "CMD_STU_PLACE_2", \
                           "CMD_MAS_PICK", "CMD_MAS_PLACE", "CMD_MAS_PICK_MAGAZINE", "CMD_MAS_PLACE_MAGAZINE", \
                           "CMD_LWS_DYNAMIC_PICKUP", "CMD_RAPID_STOP", "CMD_PULSEDO", "CMD_SENDMOVELRELTOOL", \
                           "CMD_SENDMOVELRELTCP", "CMD_COORDINATED_GANTRY_MOVE" ]

#===============================================================================
# MESSAGE TYPES BASE
#===============================================================================

""" Message Identifiers for sending and receiving messages from the BASE only
Message always consists of [Length[just message body in {}, 4 byte int], MsgType[4byte int], {counter[4byte int], timestamp[8byte double], msg[length depending]}] """

MSG_INVALID = 0

# FOR BASE MOVE CMDS SENDING
MSG_CMD_TRANSLATE = 1 # [float1] float1: distance in mm (-:backward, + forward)
MSG_CMD_ROTATE = 2 # [float1]: float1: angle in radian (- clockwise, + counterclockwise)
MSG_CMD_POSE = 3 # [x, y, angle] xposition [mm], yposition[mm], angle_destination [radiant]
MSG_CMD_SCAN = 4 # [int1] int1: number of scans

# BASE POSE INFORMATION AS STREAM
MSG_BASE_CURRENT_POSE = 5 # [x, y, z, q1, q2, q3, q4]

# FOR BASE MOVE CMDS RECEIVING
MSG_BASE_CMD_EXECUTED = 6 # [] empty message

# MESSAGES FROM BASE FOR PASSING ON ARM MANIPULATION TASKS TO ABB ARM
MSG_BASE_MOVE_ARM_TO_POSE = 7 # [x, y, z, qw, qx, qy, qz]
MSG_BASE_PLACE_BRICK = 8 # [x, y, z, qw, qx, qy, qz]
MSG_BASE_SCAN_AT_POSE = 9 # [x, y, z, qw, qx, qy, qz]

MSG_CMD_EXECUTED = 10 # []

MSG_BASE_GET_IMU_QUAT = 11 #[]
MSG_BASE_IMU_QUAT = 12 #[q1, q2, q3, q4]

base_msg_types_str_array = ["MSG_INVALID", "MSG_CMD_TRANSLATE", "MSG_CMD_ROTATE", "MSG_CMD_POSE", "MSG_CMD_SCAN", \
                            "MSG_BASE_CURRENT_POSE", "MSG_BASE_CMD_EXECUTED", \
                            "MSG_BASE_MOVE_ARM_TO_POSE", "MSG_BASE_PLACE_BRICK", "MSG_BASE_SCAN_AT_POSE", "MSG_CMD_EXECUTED", \
                            "MSG_BASE_GET_IMU_QUAT", "MSG_BASE_IMU_QUAT"]


#===============================================================================
# MESSAGE TYPES VISION
#===============================================================================

""" Message Identifiers for sending and receiving messages from the BASE only
Message always consists of [Length[just message body in {}, 4 byte int], MsgType[4byte int], {counter[4byte int], timestamp[8byte double], msg[length depending]}] """

MSG_INVALID = 0

# WIRE LINE ESTIMATION
MSG_VISION_GET_CURRENT_WIRE_LINE = 1 # msg is empty
MSG_VISION_CURRENT_WIRE_LINE = 2 # client returns [x_p1, y_p1, z_p1, x_p2, y_p2, z_p2]
MSG_VISION_GET_CURRENT_WIRE_LINE_1LINEINPUT = 3 # msg is [x_p1, y_p1, z_p1, x_p2, y_p2, z_p2] = expected line from and line to in camera frame
MSG_VISION_CURRENT_WIRE_LINE_1LINEOUTPUT = 4 # client returns [x_m1, y_m1, z_m1, x_v1, y_v1, z_v1] = midpoint of estimated wire (= intersection of normal plane), vector of the wire direction unified
MSG_VISION_GET_CURRENT_WIRE_LINE_3LINEINPUT = 5 # msg is [estimation_type, x_p1_l1, y_p1_l1, z_p1_l1, x_p2_l1, y_p2_l1, z_p2_l1 * 3] = expected 3 lines, continuous element and two discrete elements, line from and line to in camera frame, int est_type tells which one to match
MSG_VISION_CURRENT_WIRE_LINE_3LINEOUTPUT = 6 # client returns [x_m1, y_m1, z_m1, x_v1, y_v1, z_v1 * 2] = midpoint of estimated wire (= intersection of normal plane), vector of the wire direction unified, startpoint of the discrete wire element, vector of the discrete wire element direction unified

# CAMERA CALIBRATION
MSG_VISION_SEND_CURRENT_ARM_POSE = 7  # send msg is the current pose of the arm [x, y, z, qw, qx, qy, qz] --> client returns msg MSG_VISION_SUCCESS (empty msg)

# GENERIC
MSG_VISION_SEND_SUCCESS = 8 # server sends empty msg (as OK!)
MSG_VISION_SUCCESS = 9 # client returns empty msg (as OK!)

# BASE POSE ESTIMATION
MSG_VISION_GET_CURRENT_BASE_POSE = 10 # msg ist empty
MSG_VISION_CURRENT_BASE_POSE = 11 # client returns [x, y, z, qw, qx, qy, qz]

vision_msg_types_str_array = ["MSG_INVALID", "MSG_VISION_GET_CURRENT_WIRE_LINE", "MSG_VISION_CURRENT_WIRE_LINE", \
                              "MSG_VISION_GET_CURRENT_WIRE_LINE_1LINEINPUT", "MSG_VISION_CURRENT_WIRE_LINE_1LINEOUTPUT", \
                              "MSG_VISION_GET_CURRENT_WIRE_LINE_3LINEINPUT", "MSG_VISION_CURRENT_WIRE_LINE_3LINEOUTPUT", \
                              "MSG_VISION_SEND_CURRENT_ARM_POSE", "MSG_VISION_SEND_SUCCESS", "MSG_VISION_SUCCESS", \
                              "MSG_VISION_GET_CURRENT_BASE_POSE", "MSG_VISION_CURRENT_BASE_POSE"]
