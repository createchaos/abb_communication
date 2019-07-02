MODULE A011_igps_communication_21
    
    ! ************************************************
    ! Messages used for TCP/IP communication:
    ! 0: INVALID
    ! 1: EMPTY
    ! 2: RFL_CALIB_POSE
    ! 3: RFL_CALIB_JOINTS
    ! 4: RFL_CALIB_POSE_FEEDBACK
    ! ************************************************
    
    ! Message header
    RECORD MSG_HEADER
        num msg_type;
        num msg_counter;
        num timestamp_sec;
        num timestamp_nsec;
    ENDRECORD
    
    ! Message RFLCalibJoints (Type = 3)
    RECORD MSG_RFL_CALIB_JOINTS
        MSG_HEADER header;
        jointtarget rfl_calib_joints;
    ENDRECORD
    
    ! Message RFLCalibPoseFeedback (Type = 4)
    RECORD MSG_RFL_CALIB_POSE_FEEDBACK
        MSG_HEADER header;
        pose end_effector_world;
        pose end_effector_base;
    ENDRECORD
    
    ! Clock
    VAR clock igps_comm_clock;
    
    ! Set up a TCP/IP client
    PROC SetupTCPIPClient(VAR socketdev socket_dev, string adress, num port)
        IF (SocketGetStatus(socket_dev) = SOCKET_CREATED)
            SocketClose socket_dev;
        SocketCreate socket_dev;
        
        WHILE (SocketGetStatus(socket_dev) <> SOCKET_CONNECTED) DO
            SocketConnect socket_dev, adress, port, \Time:=3;
        ENDWHILE
        
        ERROR
        IF ERRNO = ERR_SOCK_TIMEOUT THEN
            SkipWarn;
            TRYNEXT;
        ENDIF
    ENDPROC
    
    ! Close TCP/IP client socket
    PROC CloseTCPIPClient(VAR socketdev socket_dev)
        SocketClose socket_dev;
    ENDPROC
        
    ! Receive message
    PROC ReceiveMessage(VAR socketdev socket_dev, VAR num msg_type, VAR rawbytes raw_data, \num timeout)
        VAR num timeout_default := WAIT_MAX;
        VAR num recv_bytes;
        VAR num msg_length;
        
        IF Present(timeout) timeout_default := timeout;                
        SocketReceive socket_dev, \RawData:=raw_data , \NoRecBytes:=recv_bytes, \Time:=timeout_default;
        
        UnpackRawBytes raw_data, 1, msg_length, \IntX:=ULINT;
        UnpackRawBytes raw_data, 9, msg_type, \IntX:=ULINT;
        
        ! Sanity check on received bytes
        ! Sent message length does not include length of message length [8 bytes] and message type [8 bytes]
        IF (recv_bytes <> (msg_length + 8 + 8)) THEN
            ErrWrite\W,"iGPS communication receive failed","Did not receive expected # of bytes.",
                     \RL2:="Expected: " + ValToStr(msg_length + 8 + 8),
                     \RL3:="Received: " + ValToStr(recv_bytes);
            msg_type := -1;
        ENDIF
    ENDPROC
    
    ! Send message
    PROC SendMessage(VAR socketdev socket_dev, VAR rawbytes raw_data, \num timeout)              
        SocketSend socket_dev, \RawData:=raw_data;
    ENDPROC
    
    ! Unpack message RFL_CALIB_JOINTS (length: 64 bytes)
    PROC UnpackMSGRFLCalibJoints(VAR rawbytes raw_message, VAR MSG_RFL_CALIB_JOINTS rfl_calib_joints_msg)     
        rfl_calib_joints_msg.header := UnpackHeader(raw_message, 9);
        IF NOT CheckMessageType(3, rfl_calib_joints_msg.header.msg_type, "UnpackMSGRFLCalibJoints") THEN
            RETURN;
        ENDIF
        rfl_calib_joints_msg.rfl_calib_joints := UnpackJointtarget(raw_message, 29);
    ENDPROC
    
    ! Pack message RFL_CALIB_POSE_FEEDBACK (length: 84 bytes)
    PROC PackMSGRFLCalibPoseFeedback(MSG_RFL_CALIB_POSE_FEEDBACK rfl_calib_pose_feedback_msg, num calib_target_num, VAR rawbytes raw_message)
        VAR num message_length := 84 - 16; ! Message length does not include length of message length [8 bytes] and message type [8 bytes]

        rfl_calib_pose_feedback_msg.header.msg_type := 4;
        rfl_calib_pose_feedback_msg.header.msg_counter := calib_target_num;
        CreateTimestamp rfl_calib_pose_feedback_msg.header;
        
        PackRawBytes message_length, raw_message, 1, \IntX:=ULINT;
        PackHeader rfl_calib_pose_feedback_msg.header, 9, raw_message;
        PackPose rfl_calib_pose_feedback_msg.end_effector_world, 29, raw_message;
        PackPose rfl_calib_pose_feedback_msg.end_effector_base, 57, raw_message;        
    ENDPROC
    
    ! Unpack header (length: 20 bytes)
    LOCAL FUNC MSG_HEADER UnpackHeader(VAR rawbytes raw_message, num start_index)
        VAR MSG_HEADER header_msg;
        
        UnpackRawBytes raw_message, start_index, header_msg.msg_type, \IntX:=ULINT;
        UnpackRawBytes raw_message, start_index + 8, header_msg.msg_counter, \IntX:=UDINT;
        UnpackRawBytes raw_message, start_index + 12, header_msg.timestamp_sec, \IntX:=UDINT;
        UnpackRawBytes raw_message, start_index + 16, header_msg.timestamp_nsec, \IntX:=UDINT;
        
        RETURN header_msg;
    ENDFUNC
    
    ! Unpack robjoint (length: 24 bytes)
    LOCAL FUNC robjoint UnpackRobjoint(VAR rawbytes raw_message, num start_index)
        VAR robjoint joints;
        
        UnpackRawBytes raw_message, start_index, joints.rax_1, \Float4;
        UnpackRawBytes raw_message, start_index + 4, joints.rax_2, \Float4;
        UnpackRawBytes raw_message, start_index + 8, joints.rax_3, \Float4;
        UnpackRawBytes raw_message, start_index + 12, joints.rax_4, \Float4;
        UnpackRawBytes raw_message, start_index + 16, joints.rax_5, \Float4;
        UnpackRawBytes raw_message, start_index + 20, joints.rax_6, \Float4;
        
        RETURN RadToDegRJ(joints);
    ENDFUNC
    
    ! Unpack extjoint (length: 12 bytes)
    LOCAL FUNC extjoint UnpackExjoint(VAR rawbytes raw_message, num start_index)
        VAR extjoint ext;
        
        UnpackRawBytes raw_message, start_index, ext.eax_a, \Float4;
        UnpackRawBytes raw_message, start_index + 4, ext.eax_b, \Float4;
        UnpackRawBytes raw_message, start_index + 8, ext.eax_c, \Float4;
        
        RETURN MToMMEJ(ext);
    ENDFUNC
    
    ! Unpack pos (length: 12 bytes)
    LOCAL FUNC pos UnpackPos(VAR rawbytes raw_message, num start_index)
        VAR pos position;
        
        UnpackRawBytes raw_message, start_index, position.x, \Float4;
        UnpackRawBytes raw_message, start_index + 4, position.y, \Float4;
        UnpackRawBytes raw_message, start_index + 8, position.z, \Float4;
        
        RETURN MToMMP(position);
    ENDFUNC
    
    ! Unpack orient (length: 16 bytes)
    LOCAL FUNC orient UnpackOrient(VAR rawbytes raw_message, num start_index)
        VAR orient rotation;
        
        UnpackRawBytes raw_message, start_index, rotation.q1, \Float4;
        UnpackRawBytes raw_message, start_index, rotation.q2, \Float4;
        UnpackRawBytes raw_message, start_index, rotation.q3, \Float4;
        UnpackRawBytes raw_message, start_index, rotation.q4, \Float4;
        
        RETURN rotation;
    ENDFUNC
    
    
    ! Unpack jointtarget (length: 36 bytes)
    LOCAL FUNC jointtarget UnpackJointtarget(VAR rawbytes raw_message, num start_index)
        VAR jointtarget joint_target;
        
        joint_target.robax := UnpackRobjoint(raw_message, start_index);
        joint_target.extax := UnpackExjoint(raw_message, start_index + 24);
        
        RETURN joint_target;
    ENDFUNC
    
    ! Unpack pose (length: 28 bytes)
    LOCAL FUNC pose UnpackPose(VAR rawbytes raw_message, num start_index)
        VAR pose pose_var;
        
        pose_var.trans := UnpackPos(raw_message, start_index);
        pose_var.rot := UnpackOrient(raw_message, start_index + 12);
        
        RETURN pose_var;
    ENDFUNC
    
    ! Unpack robtarget (length: 40 bytes)
    LOCAL FUNC robtarget UnpackRobtarget(VAR rawbytes raw_message, num start_index)
        VAR robtarget rob_target;
        
        rob_target.trans := UnpackPos(raw_message, start_index);
        rob_target.rot := UnpackOrient(raw_message, start_index + 12);
        rob_target.extax := UnpackExjoint(raw_message, start_index + 28);
        
        RETURN rob_target;
    ENDFUNC
    
    ! Pack header (length: 20 bytes)
    LOCAL PROC PackHeader(MSG_HEADER header_msg, num start_index, VAR rawbytes raw_message)    
        PackRawBytes header_msg.msg_type, raw_message, start_index, \IntX:=ULINT;
        PackRawBytes header_msg.msg_counter, raw_message, start_index + 8, \IntX:=UDINT;
        PackRawBytes header_msg.timestamp_sec, raw_message, start_index + 12, \IntX:=UDINT;
        PackRawBytes header_msg.timestamp_nsec, raw_message, start_index + 16,  \IntX:=UDINT;
    ENDPROC
    
    ! Pack robjoint (length: 24 bytes)
    LOCAL PROC PackRobjoint(robjoint rob_joint_abb, num start_index, VAR rawbytes raw_message)
        VAR robjoint rob_joint_si;
        rob_joint_si := DegToRadRJ(rob_joint_abb);
        
        PackRawBytes rob_joint_si.rax_1, raw_message, start_index, \Float4;
        PackRawBytes rob_joint_si.rax_2, raw_message, start_index + 4, \Float4;
        PackRawBytes rob_joint_si.rax_3, raw_message, start_index + 8, \Float4;
        PackRawBytes rob_joint_si.rax_4, raw_message, start_index + 12, \Float4;
        PackRawBytes rob_joint_si.rax_5, raw_message, start_index + 16, \Float4;
        PackRawBytes rob_joint_si.rax_6, raw_message, start_index + 20, \Float4;
    ENDPROC
    
    ! Pack extjoint (length: 12 bytes)
    LOCAL PROC PackExtjoint(extjoint ext_joint_abb, num start_index, VAR rawbytes raw_message)
        VAR extjoint ext_joint_si;
        ext_joint_si := MMToMEJ(ext_joint_abb);
        
        PackRawBytes ext_joint_si.eax_a, raw_message, start_index, \Float4;
        PackRawBytes ext_joint_si.eax_b, raw_message, start_index + 4, \Float4;
        PackRawBytes ext_joint_si.eax_c, raw_message, start_index + 8, \Float4;
    ENDPROC
    
    ! Pack pos (length: 12 bytes)
    LOCAL PROC PackPos(pos position_abb, num start_index, VAR rawbytes raw_message)
        VAR pos position_si;
        position_si := MMToMP(position_abb);
        
        PackRawBytes position_si.x, raw_message, start_index, \Float4;
        PackRawBytes position_si.y, raw_message, start_index + 4, \Float4;
        PackRawBytes position_si.z, raw_message, start_index + 8, \Float4;        
    ENDPROC
    
    ! Pack orient (length: 16 bytes)
    LOCAL PROC PackOrient(orient rotation, num start_index, VAR rawbytes raw_message)
        PackRawBytes rotation.q1, raw_message, start_index, \Float4;
        PackRawBytes rotation.q2, raw_message, start_index + 4, \Float4;
        PackRawBytes rotation.q3, raw_message, start_index + 8, \Float4;
        PackRawBytes rotation.q4, raw_message, start_index + 12, \Float4;
    ENDPROC
    
    ! Pack jointtarget (length: 36 bytes)
    LOCAL PROC PackJointtarget(jointtarget joint_target, num start_index, VAR rawbytes raw_message)
        PackRobjoint joint_target.robax, start_index, raw_message;
        PackExtjoint joint_target.extax, start_index + 24, raw_message;
    ENDPROC    
    
    ! Pack pose (length: 28 bytes)
    LOCAL PROC PackPose(pose pose_var, num start_index, VAR rawbytes raw_message)
        PackPos pose_var.trans, start_index, raw_message;
        PackOrient pose_var.rot, start_index + 12, raw_message;
    ENDPROC
    
    ! Pack robtarget (length: 40 bytes)
    LOCAL PROC PackRobtarget(robtarget rob_target, num start_index, VAR rawbytes raw_message)
        PackPos rob_target.trans, start_index, raw_message;
        PackOrient rob_target.rot, start_index + 12, raw_message;
        PackExtjoint rob_target.extax, start_index + 28, raw_message;
    ENDPROC
    
    ! Check message type
    LOCAL FUNC bool CheckMessageType(num expected_type, num received_type, string call_func_name) 
        IF (expected_type <> received_type) THEN
            ErrWrite\W,"iGPS communication - ","Wrong message type in " + call_func_name + "!",
                \RL2:="Expected: " + ValToStr(expected_type),
                \RL3:="Received: " + ValToStr(received_type);
            RETURN FALSE;
        ELSE
            RETURN TRUE;
        ENDIF
    ENDFUNC
    
    ! Create timestamp
    LOCAL PROC CreateTimestamp(MSG_HEADER header)
        VAR num time_sync;
        
        time_sync:=ClkRead(igps_comm_clock);
        header.timestamp_sec := Trunc(time_sync);
        header.timestamp_nsec := Trunc((time_sync - header.timestamp_sec) * 1000);
    ENDPROC
    
ENDMODULE