MODULE A009_ComRhino_22
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIP CO 11.1 / Gustave-Naville-Weg 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A009_LightwightStructur
    !
    ! FUNCTION    :  Communication with Rhino
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2016.11.02 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    ! Comment     :  Code from Kathrin Doerfler copyed
    !
    !***********************************************************************************


    !************************************************
    !
    ! Code from   :     Modul tcpip_params Start
    !    
    !************************************************

    RECORD TCPIP_MSG_RAW
        num msg_type;
        rawbytes data;
    ENDRECORD

    RECORD TCPIP_MSG_RAW_RECEIVER
        num msg_type;
        num msg_counter;
        num timestamp_sec;
        num timestamp_nanosec;
        rawbytes data;
    ENDRECORD

    RECORD TCPIP_MSG_COMMAND
        num cmd_type;
        
        !either: 6 values for jointtarget or 7 values for robtarget
        !Changed to either 9 or 10 values - stefana
        num val1;
        num val2;
        num val3;
        num val4;
        num val5;
        num val6;
        num val7;
        num val8;
        num val9;
        num val10;

        num velocity;
        num duration;
        num zone;
        num tool;
        num arbitrary;
        num wobj;

    ENDRECORD

    RECORD TCPIP_MSG_CP_CARTESIAN
        num msg_type;
        robtarget target;
    ENDRECORD

    RECORD TCPIP_MSG_CP_JOINT
        num msg_type;
        robjoint joints;
        !in DEGREES TODO:check!!
    ENDRECORD

    RECORD TCPIP_MSG_COMMAND_EXEC
        num msg_type;
        num cmd_exec_counter;
    ENDRECORD

    RECORD TCPIP_MSG_COMMAND_REC
        num msg_type;
        num msg_rec_counter;
    ENDRECORD

    !new message
    PERS TCPIP_MSG_COMMAND tcpip_message;
    PERS bool TCPIP_new_message:=FALSE;
    !these variables should use waittestandset for read/write protection to prevent conflicts

    !locks
    PERS bool msg_lock:=FALSE;
    PERS bool cmd_exec_lock:=FALSE;
    PERS bool sender_socket_lock:=FALSE;
    PERS bool msg_send_counter_lock:=FALSE;

    !cmd buffer
    !CONST num MAX_BUFFER_SIZE:=2048;
    CONST num MAX_BUFFER_SIZE:=100;

    PERS TCPIP_MSG_COMMAND tcpip_message_command_buffer_r1{MAX_BUFFER_SIZE};
    PERS num BUFFER_LENGTH_R1;
    PERS num READ_PTR_R1;
    PERS num WRITE_PTR_R1;

    PERS TCPIP_MSG_COMMAND tcpip_message_command_buffer_r2{MAX_BUFFER_SIZE};
    PERS num BUFFER_LENGTH_R2;
    PERS num READ_PTR_R2;
    PERS num WRITE_PTR_R2;

    PERS TCPIP_MSG_COMMAND tcpip_message_command_buffer_r3{MAX_BUFFER_SIZE};
    PERS num BUFFER_LENGTH_R3;
    PERS num READ_PTR_R3;
    PERS num WRITE_PTR_R3;

    PERS TCPIP_MSG_COMMAND tcpip_message_command_buffer_r4{MAX_BUFFER_SIZE};
    PERS num BUFFER_LENGTH_R4;
    PERS num READ_PTR_R4;
    PERS num WRITE_PTR_R4;

    !counter    
    PERS num msg_rec_counter;
    PERS num cmd_exec_counter;
    PERS num msg_send_counter;

    !server
    !CONST string address:="192.168.125.1"; 
    !CONST string address:="127.0.0.1";
    !CONST string address:="192.168.0.11";
    CONST string address:="192.168.0.21";
    
    CONST num port_receiver:=30003;
    CONST num port_sender:=30004;
    CONST num port_sender_sync:=30005;

    !for interrupts
    PERS bool send_msg_cmd_exec:=FALSE;
    PERS bool send_msg_cmd_rcv:=FALSE;

    !clock
    VAR clock tcpip_clock;

    ! reset interrupts
    PERS bool reset_to_main:=FALSE;

    !************************************************
    !
    ! Code from   :     Modul tcpip_params End
    !    
    !************************************************


    !************************************************
    !
    ! Code from   :     Modul tcpip_msgs Start
    !    
    !************************************************


    !---------------------------------------------------------------------------------------------------------------------------------      
    !Message TYPES
    !--------------------------------------------------------------------------------------------------------------------------------- 
    CONST num MSG_COMMAND:=1;
    ![counter,position,orientation,optional values]
    CONST num MSG_STOP:=2;
    CONST num MSG_IDLE:=3;
    CONST num MSG_COMMAND_RECEIVED:=4; ![counter]
    CONST num MSG_CURRENT_POSE_CARTESIAN:=5; ![position,orientation,external axes]
    CONST num MSG_CURRENT_POSE_JOINT:=6; ![j1,j2,j3,j4,j5,j6,e1,e2,e3]
    CONST num MSG_STRING:=7; ![string]
    CONST num MSG_FLOAT_LIST:=8; ![float,float,...]
    CONST num MSG_OPERATION:=9; ![string] (the name of the operation)
    CONST num MSG_ACTUATOR_INIT:=10; !tool[position,orientation] + base[position,orientation]

    CONST num MSG_ANALOG_IN:=11;
    CONST num MSG_ANALOG_OUT:=12;
    CONST num MSG_DIGITAL_IN:=13;
    CONST num MSG_DIGITAL_OUT:=14;
    CONST num MSG_COMMAND_EXECUTED:=15; ![counter]
    CONST num MSG_IDENTIFIER:= 16;
    
    CONST num MSG_CURRENT_POSE_CARTESIAN_BASE:=17;
    !---------------------------------------------------------------------------------------------------------------------------------

    !---------------------------------------------------------------------------------------------------------------------------------      
    !Command TYPES
    !--------------------------------------------------------------------------------------------------------------------------------- 
    CONST num CMD_IDLE_MODE:=0;
    CONST num CMD_GO_TO_JOINTTARGET_ABS:=1;
    CONST num CMD_GO_TO_TASKTARGET:=2;
    CONST num CMD_PICK_BRICK:=3;
    CONST num CMD_PLACE_BRICK:=4;
    CONST num CMD_GO_TO_JOINTTARGET_REL:=5;
    CONST num CMD_PICK_BRICK_FROM_POSE:=6;
    CONST num CMD_PICK_ROD:=7;
    CONST num CMD_MILL_ROD_START:=8;
    CONST num CMD_MILL_ROD_END:=9;
    CONST num CMD_REGRIP_PLACE:=10;
    CONST num CMD_REGRIP_PICK:=11;
    CONST num CMD_SAFE_POS:=12;
    CONST num CMD_OPEN_GRIPPER:=13;
    CONST num CMD_CLOSE_GRIPPER:=14;
    CONST num CMD_OPEN_CLAMP:=15;
    CONST num CMD_CLOSE_CLAMP:=16;
    CONST num CMD_GO_TO_TASKTARGET_JOINTS:=17;
    !added for A019 sp 170110
    CONST num CMD_STU_PICK:=18;
    CONST num CMD_STU_PLACE:=19;
    !added for MAS sp 170220
    CONST num CMD_MAS_PICK:=21;
    CONST num CMD_MAS_PLACE:=22;


    !---------------------------------------------------------------------------------------------------------------------------------
    !Functions for sending messages 
    !---------------------------------------------------------------------------------------------------------------------------------       
    PROC TCPIP_send_msg(VAR socketdev client_socket,VAR TCPIP_MSG_RAW message)
        !send byte message: add message length,msg_type,raw_msg

        VAR rawbytes buffer;
        VAR num time_sync;
        VAR num time_sec;
        VAR num time_nanosec;

        time_sync:=ClkRead(tcpip_clock);

        time_sec:=Trunc(time_sync);
        time_nanosec:=Trunc((time_sync-time_sec)*1000);

        WaitTestAndSet msg_send_counter_lock;
        Incr msg_send_counter;
        msg_send_counter_lock:=FALSE;

        !WaitTestAndSet sender_socket_lock;
        PackRawBytes RawBytesLen(message.data)+12,  buffer,1,\IntX:=ULINT; !Raw Message Length
        PackRawBytes message.msg_type,              buffer,9,\IntX:=ULINT;!Message type

        PackRawBytes msg_send_counter,              buffer,17,\IntX:=UDINT; !counter of total sent messages
        PackRawBytes time_sec,                      buffer,21,\IntX:=UDINT; !timestamp TODO: needs to be written into sec and nanosec
        PackRawBytes time_nanosec,                  buffer,25,\IntX:=UDINT;!empty        
        CopyRawBytes message.data,1,                buffer,29; !Message data

        SocketSend client_socket\RawData:=buffer;
        ClearRawBytes message.data;
        !sender_socket_lock:=FALSE;

    ERROR
        RAISE ; !raise errors to calling code
    ENDPROC

    PROC TCPIP_send_msg_command_received(VAR socketdev client_socket)
        !send the waypoint counter to the server

        VAR TCPIP_MSG_RAW raw_message;

        !Force message header to the correct values
        raw_message.msg_type:=MSG_COMMAND_RECEIVED;

        !Pack data into message
        PackRawBytes msg_rec_counter,raw_message.data,1,\IntX:=UDINT;

        TCPIP_send_msg client_socket,raw_message;

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    PROC TCPIP_send_msg_command_executed(VAR socketdev client_socket)
        !send the command executed to the server


        VAR TCPIP_MSG_RAW raw_message;

        TPWrite "Command exec: "+ValToStr(cmd_exec_counter);

        !Force message header to the correct values
        raw_message.msg_type:=MSG_COMMAND_EXECUTED;

        !Pack data into message
        PackRawBytes cmd_exec_counter,raw_message.data,1,\IntX:=UDINT;

        TCPIP_send_msg client_socket,raw_message;

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    PROC TCPIP_send_msg_cp_cartesian(VAR socketdev client_socket)
        !send the current position of the current tool to the server

        VAR TCPIP_MSG_RAW raw_message;
        VAR robtarget TCPIP_current_pos_1;
        VAR robtarget TCPIP_current_pos_2;
        VAR robtarget TCPIP_current_pos_3;
        VAR robtarget TCPIP_current_pos_4;

        !TCPIP_current_pos:=CRobT(); !:=CRobT(\Tool:=tool0 \WObj:=wobj0);
        !* TCPIP_current_pos_1:=CRobT(\TaskRef:=T_ROB11Id\Tool:=tool0\WObj:=wobj0);
        !* TCPIP_current_pos_2:=CRobT(\TaskRef:=T_ROB12Id\Tool:=tool0\WObj:=wobj0);
        TCPIP_current_pos_3:=CRobT(\TaskRef:=T_ROB21Id\Tool:=tool0\WObj:=wobj0);
        TCPIP_current_pos_4:=CRobT(\TaskRef:=T_ROB22Id\Tool:=tool0\WObj:=wobj0);


        !Force message header to the correct values
        raw_message.msg_type:=MSG_CURRENT_POSE_CARTESIAN;

        !Pack data into message
        !robot 1
        PackRawBytes TCPIP_current_pos_1.trans.x,raw_message.data,1,\Float4;
        PackRawBytes TCPIP_current_pos_1.trans.y,raw_message.data,5,\Float4;
        PackRawBytes TCPIP_current_pos_1.trans.z,raw_message.data,9,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q1,raw_message.data,13,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q2,raw_message.data,17,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q3,raw_message.data,21,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q4,raw_message.data,25,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_1.extax.eax_a,raw_message.data,29,\Float4;
        PackRawBytes TCPIP_current_pos_1.extax.eax_b,raw_message.data,33,\Float4;
        PackRawBytes TCPIP_current_pos_1.extax.eax_c,raw_message.data,37,\Float4;

        !robot 2
        PackRawBytes TCPIP_current_pos_2.trans.x,raw_message.data,41,\Float4;
        PackRawBytes TCPIP_current_pos_2.trans.y,raw_message.data,45,\Float4;
        PackRawBytes TCPIP_current_pos_2.trans.z,raw_message.data,49,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q1,raw_message.data,53,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q2,raw_message.data,57,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q3,raw_message.data,61,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q4,raw_message.data,65,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_2.extax.eax_a,raw_message.data,69,\Float4;
        PackRawBytes TCPIP_current_pos_2.extax.eax_b,raw_message.data,73,\Float4;
        PackRawBytes TCPIP_current_pos_2.extax.eax_c,raw_message.data,77,\Float4;

        !robot 3
        PackRawBytes TCPIP_current_pos_3.trans.x,raw_message.data,81,\Float4;
        PackRawBytes TCPIP_current_pos_3.trans.y,raw_message.data,85,\Float4;
        PackRawBytes TCPIP_current_pos_3.trans.z,raw_message.data,89,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q1,raw_message.data,93,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q2,raw_message.data,97,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q3,raw_message.data,101,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q4,raw_message.data,105,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_3.extax.eax_a,raw_message.data,109,\Float4;
        PackRawBytes TCPIP_current_pos_3.extax.eax_b,raw_message.data,113,\Float4;
        PackRawBytes TCPIP_current_pos_3.extax.eax_c,raw_message.data,117,\Float4;

        !robot 4
        PackRawBytes TCPIP_current_pos_4.trans.x,raw_message.data,121,\Float4;
        PackRawBytes TCPIP_current_pos_4.trans.y,raw_message.data,125,\Float4;
        PackRawBytes TCPIP_current_pos_4.trans.z,raw_message.data,129,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q1,raw_message.data,133,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q2,raw_message.data,137,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q3,raw_message.data,141,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q4,raw_message.data,145,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_4.extax.eax_a,raw_message.data,149,\Float4;
        PackRawBytes TCPIP_current_pos_4.extax.eax_b,raw_message.data,153,\Float4;
        PackRawBytes TCPIP_current_pos_4.extax.eax_c,raw_message.data,157,\Float4;

        TCPIP_send_msg client_socket,raw_message;

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    
    PROC TCPIP_send_msg_cp_cartesian_base(VAR socketdev client_socket)
        !send the current position of the current tool to the server

        VAR TCPIP_MSG_RAW raw_message;
        VAR robtarget TCPIP_current_pos_1;
        VAR robtarget TCPIP_current_pos_2;
        VAR robtarget TCPIP_current_pos_3;
        VAR robtarget TCPIP_current_pos_4;

        !TCPIP_current_pos:=CRobT(); !:=CRobT(\Tool:=tool0 \WObj:=wobj0);
        !* TCPIP_current_pos_1:=CRobT(\TaskRef:=T_ROB11Id\Tool:=tool0\WObj:=wobj_base_r1);
        !* TCPIP_current_pos_2:=CRobT(\TaskRef:=T_ROB12Id\Tool:=tool0\WObj:=wobj_base_r2);
        TCPIP_current_pos_3:=CRobT(\TaskRef:=T_ROB21Id\Tool:=tool0\WObj:=wobj_base_r3);
        TCPIP_current_pos_4:=CRobT(\TaskRef:=T_ROB22Id\Tool:=tool0\WObj:=wobj_base_r4);


        !Force message header to the correct values
        raw_message.msg_type:=MSG_CURRENT_POSE_CARTESIAN_BASE;

        !Pack data into message
        !robot 1
        PackRawBytes TCPIP_current_pos_1.trans.x,raw_message.data,1,\Float4;
        PackRawBytes TCPIP_current_pos_1.trans.y,raw_message.data,5,\Float4;
        PackRawBytes TCPIP_current_pos_1.trans.z,raw_message.data,9,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q1,raw_message.data,13,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q2,raw_message.data,17,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q3,raw_message.data,21,\Float4;
        PackRawBytes TCPIP_current_pos_1.rot.q4,raw_message.data,25,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_1.extax.eax_a,raw_message.data,29,\Float4;
        PackRawBytes TCPIP_current_pos_1.extax.eax_b,raw_message.data,33,\Float4;
        PackRawBytes TCPIP_current_pos_1.extax.eax_c,raw_message.data,37,\Float4;

        !robot 2
        PackRawBytes TCPIP_current_pos_2.trans.x,raw_message.data,41,\Float4;
        PackRawBytes TCPIP_current_pos_2.trans.y,raw_message.data,45,\Float4;
        PackRawBytes TCPIP_current_pos_2.trans.z,raw_message.data,49,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q1,raw_message.data,53,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q2,raw_message.data,57,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q3,raw_message.data,61,\Float4;
        PackRawBytes TCPIP_current_pos_2.rot.q4,raw_message.data,65,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_2.extax.eax_a,raw_message.data,69,\Float4;
        PackRawBytes TCPIP_current_pos_2.extax.eax_b,raw_message.data,73,\Float4;
        PackRawBytes TCPIP_current_pos_2.extax.eax_c,raw_message.data,77,\Float4;

        !robot 3
        PackRawBytes TCPIP_current_pos_3.trans.x,raw_message.data,81,\Float4;
        PackRawBytes TCPIP_current_pos_3.trans.y,raw_message.data,85,\Float4;
        PackRawBytes TCPIP_current_pos_3.trans.z,raw_message.data,89,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q1,raw_message.data,93,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q2,raw_message.data,97,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q3,raw_message.data,101,\Float4;
        PackRawBytes TCPIP_current_pos_3.rot.q4,raw_message.data,105,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_3.extax.eax_a,raw_message.data,109,\Float4;
        PackRawBytes TCPIP_current_pos_3.extax.eax_b,raw_message.data,113,\Float4;
        PackRawBytes TCPIP_current_pos_3.extax.eax_c,raw_message.data,117,\Float4;

        !robot 4
        PackRawBytes TCPIP_current_pos_4.trans.x,raw_message.data,121,\Float4;
        PackRawBytes TCPIP_current_pos_4.trans.y,raw_message.data,125,\Float4;
        PackRawBytes TCPIP_current_pos_4.trans.z,raw_message.data,129,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q1,raw_message.data,133,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q2,raw_message.data,137,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q3,raw_message.data,141,\Float4;
        PackRawBytes TCPIP_current_pos_4.rot.q4,raw_message.data,145,\Float4;
        !added - stefana
        PackRawBytes TCPIP_current_pos_4.extax.eax_a,raw_message.data,149,\Float4;
        PackRawBytes TCPIP_current_pos_4.extax.eax_b,raw_message.data,153,\Float4;
        PackRawBytes TCPIP_current_pos_4.extax.eax_c,raw_message.data,157,\Float4;

        TCPIP_send_msg client_socket,raw_message;

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    PROC TCPIP_send_msg_cp_joint(VAR socketdev client_socket)
        !send the current joint position in rad to the server
        VAR TCPIP_MSG_RAW raw_message;
        VAR jointtarget TCPIP_jointtarget_1;
        VAR jointtarget TCPIP_jointtarget_2;
        VAR jointtarget TCPIP_jointtarget_3;
        VAR jointtarget TCPIP_jointtarget_4;
        VAR robjoint TCPIP_joints_rad_1;
        VAR robjoint TCPIP_joints_rad_2;
        VAR robjoint TCPIP_joints_rad_3;
        VAR robjoint TCPIP_joints_rad_4;

        !* TCPIP_jointtarget_1:=CJointT(\TaskRef:=T_ROB11Id);
        !* TCPIP_jointtarget_2:=CJointT(\TaskRef:=T_ROB12Id);
        TCPIP_jointtarget_3:=CJointT(\TaskRef:=T_ROB21Id);
        TCPIP_jointtarget_4:=CJointT(\TaskRef:=T_ROB22Id);

        !Convert data from ABB units to ROS standard units
        TCPIP_joints_rad_1:=deg2rad_robjoint(TCPIP_jointtarget_1.robax);
        TCPIP_joints_rad_2:=deg2rad_robjoint(TCPIP_jointtarget_2.robax);
        TCPIP_joints_rad_3:=deg2rad_robjoint(TCPIP_jointtarget_3.robax);
        TCPIP_joints_rad_4:=deg2rad_robjoint(TCPIP_jointtarget_4.robax);

        !Force message header to the correct values
        raw_message.msg_type:=MSG_CURRENT_POSE_JOINT;

        !Pack data into message
        !Robot1
        PackRawBytes TCPIP_joints_rad_1.rax_1,raw_message.data,1,\Float4;
        PackRawBytes TCPIP_joints_rad_1.rax_2,raw_message.data,5,\Float4;
        PackRawBytes TCPIP_joints_rad_1.rax_3,raw_message.data,9,\Float4;
        PackRawBytes TCPIP_joints_rad_1.rax_4,raw_message.data,13,\Float4;
        PackRawBytes TCPIP_joints_rad_1.rax_5,raw_message.data,17,\Float4;
        PackRawBytes TCPIP_joints_rad_1.rax_6,raw_message.data,21,\Float4;
        !added - stefana
        PackRawBytes TCPIP_jointtarget_1.extax.eax_a,raw_message.data,25,\Float4;
        PackRawBytes TCPIP_jointtarget_1.extax.eax_b,raw_message.data,29,\Float4;
        PackRawBytes TCPIP_jointtarget_1.extax.eax_c,raw_message.data,33,\Float4;

        !Robot2
        PackRawBytes TCPIP_joints_rad_2.rax_1,raw_message.data,37,\Float4;
        PackRawBytes TCPIP_joints_rad_2.rax_2,raw_message.data,41,\Float4;
        PackRawBytes TCPIP_joints_rad_2.rax_3,raw_message.data,45,\Float4;
        PackRawBytes TCPIP_joints_rad_2.rax_4,raw_message.data,49,\Float4;
        PackRawBytes TCPIP_joints_rad_2.rax_5,raw_message.data,53,\Float4;
        PackRawBytes TCPIP_joints_rad_2.rax_6,raw_message.data,57,\Float4;
        !added - stefana
        PackRawBytes TCPIP_jointtarget_2.extax.eax_a,raw_message.data,61,\Float4;
        PackRawBytes TCPIP_jointtarget_2.extax.eax_b,raw_message.data,65,\Float4;
        PackRawBytes TCPIP_jointtarget_2.extax.eax_c,raw_message.data,69,\Float4;

        !Robot3
        PackRawBytes TCPIP_joints_rad_3.rax_1,raw_message.data,73,\Float4;
        PackRawBytes TCPIP_joints_rad_3.rax_2,raw_message.data,77,\Float4;
        PackRawBytes TCPIP_joints_rad_3.rax_3,raw_message.data,81,\Float4;
        PackRawBytes TCPIP_joints_rad_3.rax_4,raw_message.data,85,\Float4;
        PackRawBytes TCPIP_joints_rad_3.rax_5,raw_message.data,89,\Float4;
        PackRawBytes TCPIP_joints_rad_3.rax_6,raw_message.data,93,\Float4;
        !added - stefana
        PackRawBytes TCPIP_jointtarget_3.extax.eax_a,raw_message.data,97,\Float4;
        PackRawBytes TCPIP_jointtarget_3.extax.eax_b,raw_message.data,101,\Float4;
        PackRawBytes TCPIP_jointtarget_3.extax.eax_c,raw_message.data,105,\Float4;

        !Robot4
        PackRawBytes TCPIP_joints_rad_4.rax_1,raw_message.data,109,\Float4;
        PackRawBytes TCPIP_joints_rad_4.rax_2,raw_message.data,113,\Float4;
        PackRawBytes TCPIP_joints_rad_4.rax_3,raw_message.data,117,\Float4;
        PackRawBytes TCPIP_joints_rad_4.rax_4,raw_message.data,121,\Float4;
        PackRawBytes TCPIP_joints_rad_4.rax_5,raw_message.data,125,\Float4;
        PackRawBytes TCPIP_joints_rad_4.rax_6,raw_message.data,129,\Float4;
        !added - stefana
        PackRawBytes TCPIP_jointtarget_4.extax.eax_a,raw_message.data,133,\Float4;
        PackRawBytes TCPIP_jointtarget_4.extax.eax_b,raw_message.data,137,\Float4;
        PackRawBytes TCPIP_jointtarget_4.extax.eax_c,raw_message.data,141,\Float4;

        TCPIP_send_msg client_socket,raw_message;


        !TPWrite "Message sent: "+ValToStr(raw_message.data);

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC


    !---------------------------------------------------------------------------------------------------------------------------------
    !Functions for receiving messages 
    !--------------------------------------------------------------------------------------------------------------------------------- 
    PROC TCPIP_receive_msg(VAR socketdev client_socket,VAR TCPIP_MSG_RAW_RECEIVER message)
        VAR rawbytes buffer;
        VAR num time_val:=WAIT_MAX;
        !default to wait-forever
        VAR num bytes_rcvd;
        VAR num msg_length;

        ClearRawBytes buffer;

        !TBD: need to determine whether this handles split/merged messages correctly

        !Read prefix INT (total message length)
        SocketReceive client_socket,\RawData:=buffer,\ReadNoOfBytes:=8,\Time:=time_val;
        UnpackRawBytes buffer,1,msg_length,\IntX:=ULINT;
        !msg length = msg_data_langth + msg_header_length, without the length of the message type(which is 8byte)
        !TPWrite "message length: "+ValToStr(msg_length);

        !Read remaining message bytes
        SocketReceive client_socket,\RawData:=buffer,\ReadNoOfBytes:=(msg_length+8),\NoRecBytes:=bytes_rcvd,\Time:=time_val;
        IF (bytes_rcvd<>(msg_length+8)) THEN
            ErrWrite\W,"ROS Socket Recv Failed","Did not receive expected # of bytes.",
                     \RL2:="Expected: "+ValToStr(msg_length+8),
                     \RL3:="Received: "+ValToStr(bytes_rcvd);
            RETURN ;
        ENDIF

        !Unpack message header/data
        UnpackRawBytes buffer,1,message.msg_type,\IntX:=ULINT;

        UnpackRawBytes buffer,9,message.msg_counter,\IntX:=UDINT;
        UnpackRawBytes buffer,13,message.timestamp_sec,\IntX:=UDINT;
        UnpackRawBytes buffer,17,message.timestamp_nanosec,\IntX:=UDINT;

        !If message is bigger then 4 bytes,copy raw message into buffer
        IF msg_length>20 THEN
            CopyRawBytes buffer,21,message.data,1;
            !TPWrite "RAWBYTESLENGTH: " + ValToStr(RawBytesLen(message.data));
        ELSE
            ClearRawBytes message.data;
        ENDIF

        !count received messages
        !counter:=counter + 1;
        !TPWrite "received_message " + ValToStr(counter);

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    PROC TCPIP_receive_msg_command(VAR TCPIP_MSG_RAW_RECEIVER message_raw,VAR TCPIP_MSG_COMMAND message_command)

        !TPWrite "RAWBYTESLENGTH: " + ValToStr(RawBytesLen(message_raw.data));

        !Integrity Check: Data Size
        !IF (RawBytesLen(raw_message.data) < 52) THEN
        !   ErrWrite \W,"ROS Socket Missing Data","Insufficient data for joint_trajectory_pt",
        !           \RL2:="expected: 52",
        !           \RL3:="received: " + ValToStr(RawBytesLen(raw_message.data));
        !   RAISE ERR_OUTOFBND;  !TBD: define specific error code
        !ENDIF

        !Unpack data fields
        UnpackRawBytes message_raw.data,1,message_command.cmd_type,\IntX:=UDINT;

        UnpackRawBytes message_raw.data,5,message_command.val1,\Float4;
        UnpackRawBytes message_raw.data,9,message_command.val2,\Float4;
        UnpackRawBytes message_raw.data,13,message_command.val3,\Float4;
        UnpackRawBytes message_raw.data,17,message_command.val4,\Float4;
        UnpackRawBytes message_raw.data,21,message_command.val5,\Float4;
        UnpackRawBytes message_raw.data,25,message_command.val6,\Float4;
        UnpackRawBytes message_raw.data,29,message_command.val7,\Float4;

        ! added - stefana
        UnpackRawBytes message_raw.data,33,message_command.val8,\Float4;
        UnpackRawBytes message_raw.data,37,message_command.val9,\Float4;
        UnpackRawBytes message_raw.data,41,message_command.val10,\Float4;

        !changed - stefana
        UnpackRawBytes message_raw.data,45,message_command.velocity,\IntX:=UDINT;
        UnpackRawBytes message_raw.data,49,message_command.duration,\Float4;
        UnpackRawBytes message_raw.data,53,message_command.zone,\IntX:=UDINT;
        UnpackRawBytes message_raw.data,57,message_command.tool,\IntX:=UDINT;
        UnpackRawBytes message_raw.data,61,message_command.arbitrary,\Float4;
        UnpackRawBytes message_raw.data,65,message_command.wobj,\IntX:=UDINT;


        !TPWrite "received " + ValToStr(message_command.waypoint_counter) + " waypoint";

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    !--------------------------------------------------------------------------------------------------------------------------------- !

    !--------------------------------------------------------------------------------------------------------------------------------- !
    !Functions for calculating radian/degree conversions ----------------------------------------------------------------------------- !
    !--------------------------------------------------------------------------------------------------------------------------------- !
    LOCAL FUNC num deg2rad(num deg)
        RETURN deg*pi/180;
    ENDFUNC

    LOCAL FUNC robjoint deg2rad_robjoint(robjoint deg)
        VAR robjoint rad;
        rad.rax_1:=deg2rad(deg.rax_1);
        rad.rax_2:=deg2rad(deg.rax_2);
        rad.rax_3:=deg2rad(deg.rax_3);
        rad.rax_4:=deg2rad(deg.rax_4);
        rad.rax_5:=deg2rad(deg.rax_5);
        rad.rax_6:=deg2rad(deg.rax_6);

        RETURN rad;
    ENDFUNC

    LOCAL FUNC num rad2deg(num rad)
        RETURN rad*180/pi;
    ENDFUNC

    LOCAL FUNC robjoint rad2deg_robjoint(robjoint rad)
        VAR robjoint deg;
        deg.rax_1:=rad2deg(rad.rax_1);
        deg.rax_2:=rad2deg(rad.rax_2);
        deg.rax_3:=rad2deg(rad.rax_3);
        deg.rax_4:=rad2deg(rad.rax_4);
        deg.rax_5:=rad2deg(rad.rax_5);
        deg.rax_6:=rad2deg(rad.rax_6);

        RETURN deg;
    ENDFUNC

    !--------------------------------------------------------------------------------------------------------------------------------- !

    !************************************************
    !
    ! Code from   :     Modul tcpip_msgs End
    !    
    !************************************************

    !************************************************
    !
    ! Code from   :     Modul tcpip_socket Start
    !    
    !************************************************



    PROC connect_to_server(VAR socketdev socket,VAR string message)
        !connect to server and send back the client-identifier

        TPWrite "create connection";
        SocketCreate socket;
        SocketConnect socket,address,port_receiver;

        !connection established
        TPWrite "connection established";

    ENDPROC

    PROC init_socket(VAR socketdev server_socket,num port)
        IF (SocketGetStatus(server_socket)=SOCKET_CLOSED) SocketCreate server_socket;
        IF (SocketGetStatus(server_socket)=SOCKET_CREATED) SocketBind server_socket,address,port;
        IF (SocketGetStatus(server_socket)=SOCKET_BOUND) SocketListen server_socket;

    ERROR
        RAISE ;
        !raise errors to calling code
    ENDPROC

    PROC wait_for_client(VAR socketdev server_socket,VAR socketdev client_socket,\num wait_time)
        VAR string client_ip;
        VAR num time_val:=WAIT_MAX;
        !default to wait-forever
        VAR bool conn_state:=FALSE;

        IF Present(wait_time) time_val:=wait_time;

        IF (SocketGetStatus(client_socket)<>SOCKET_CLOSED) SocketClose client_socket;
        WaitUntil(SocketGetStatus(client_socket)=SOCKET_CLOSED);

        WHILE (SocketGetStatus(client_socket)<>SOCKET_CONNECTED) DO

            SocketAccept server_socket,client_socket,\ClientAddress:=client_ip,\Time:=time_val;
            WaitTime 0.1;

        ENDWHILE
        TPWrite "Client at "+client_ip+" connected.";

    ERROR
        !IF ERRNO=ERR_SOCK_TIMEOUT THEN
        IF (ERRNO=ERR_SOCK_TIMEOUT) OR (ERRNO=ERR_SOCK_CLOSED) THEN
            SkipWarn;
            !TBD: include this error data in the message logged below?
            TRYNEXT;
        ENDIF
    ENDPROC

    PROC close_sockets(VAR socketdev socket1,VAR socketdev socket2)
        !close socket
        SocketClose socket1;
        SocketClose socket2;

        TPWrite "sockets closed";
    ENDPROC

    !************************************************
    !
    ! Code from   :     Modul tcpip_msgs End
    !    
    !************************************************


ENDMODULE