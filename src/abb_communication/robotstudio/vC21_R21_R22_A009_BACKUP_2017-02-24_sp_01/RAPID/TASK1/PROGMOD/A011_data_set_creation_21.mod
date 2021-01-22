MODULE A011_data_set_creation_21
    
    PERS wobjdata wobj_base_21 := [FALSE, FALSE, "Gantry21", [[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]]; 
    CONST string kiGPSServerIP := "192.168.50.216";

    ! RFL Static Correction: Data Set Creation
    PROC data_set_creation()    
        CONST num kiGPSDSCPort := 20003;
        CONST speeddata igps_dsc_speed := v300;
        
        VAR socketdev tcpip_socket;
        
        VAR num recv_msg_type;
        VAR num recv_calib_target_num;
        VAR rawbytes recv_raw_message;
        VAR rawbytes send_raw_message;
        VAR MSG_RFL_CALIB_JOINTS rfl_calib_joints_msg;
        VAR MSG_RFL_CALIB_POSE_FEEDBACK rfl_calib_pose_feedback_msg;
        
        AccSet 50, 20 \FinePointRamp:=20;
        
        TPErase;
        TPWrite "**************************************";
        TPWrite "**************************************";
        TPWrite "***                                ***";
        TPWrite "***     RFL Static Correction      ***";
        TPWrite "***     - Data Set Creation -      ***";
        TPWrite "***                                ***";
        TPWrite "**************************************";
        TPWrite "**************************************";
        
        ! Setting up a TCP/IP client to communicate with server
        TPWrite "Configured Server: " + kiGPSServerIP + ":" + ValToStr(kiGPSDSCPort);
        TPWrite "Connecting to server"  + "...";
        SetupTCPIPClient tcpip_socket, kiGPSServerIP, kiGPSDSCPort;
        TPWrite " Connection established.";
        TPWrite "Waiting for calibration target...";
        
        WHILE TRUE DO
            ! Receive calibration target message from server
            ReceiveMessage tcpip_socket, recv_msg_type, recv_raw_message;
            
            IF (recv_msg_type = 3) THEN
                ! Unpack RFLCalibJoints message 
                UnpackMSGRFLCalibJoints recv_raw_message, rfl_calib_joints_msg;
                recv_calib_target_num := rfl_calib_joints_msg.header.msg_counter;
                TPWrite "**************************************";
                TPWrite " Received calibration target " + ValToStr(recv_calib_target_num); 
                
                ! Move robot to calibration target
                TPWrite "Moving to calibration target...";
                MoveAbsJ rfl_calib_joints_msg.rfl_calib_joints, igps_dsc_speed, fine, tool0;
                
                ! Get current end effector pose relative to world and robot base   
                TPWrite "Getting and sending robot feedback..."; 
                WaitTime 1;
                
                rfl_calib_pose_feedback_msg.end_effector_world := CPoseT(tool0, wobj0);
                rfl_calib_pose_feedback_msg.end_effector_base := CPoseT(tool0, wobj_base_21);
                
                ! Pack RFLCalibPoseFeedback message.
                PackMSGRFLCalibPoseFeedback rfl_calib_pose_feedback_msg, recv_calib_target_num, send_raw_message;
                
                ! Send back current end effector pose relative to world and robot base
                SendMessage tcpip_socket, send_raw_message;
                TPWrite " Feedback sent.";
                TPWrite "Waiting for calibration target...";
            ENDIF
        ENDWHILE
        
        ! Close TCP/IP client
        CloseTCPIPClient tcpip_socket;
        TPWrite "TCP/IP socket closed.";
    ENDPROC
    
ENDMODULE