MODULE A011_static_correction_21

    ! RFL Static Correction
    PROC static_correction()    
        CONST num kiGPSSCPort := 20003;
        CONST speeddata igps_sc_speed := v300;
        
        VAR socketdev tcpip_socket;
        
        VAR num recv_msg_type;
        VAR rawbytes recv_raw_message;
        VAR rawbytes send_raw_message;
        VAR MSG_RFL_CALIB_POSE rfl_calib_POSE_msg;
        VAR MSG_RFL_CALIB_POSE_FEEDBACK rfl_calib_pose_feedback_msg;
        
        AccSet 50, 20 \FinePointRamp:=20;
        
        TPErase;
        TPWrite "**************************************";
        TPWrite "**************************************";
        TPWrite "***                                ***";
        TPWrite "***     RFL Static Correction      ***";
        TPWrite "***     - Static Correction -      ***";
        TPWrite "***                                ***";
        TPWrite "**************************************";
        TPWrite "**************************************";
        
        ! Setting up a TCP/IP client to communicate with server
        TPWrite "Configured Server: " + kiGPSServerIP + ":" + ValToStr(kiGPSSCPort);
        TPWrite "Connecting to server"  + "...";
        SetupTCPIPClient tcpip_socket, kiGPSServerIP, kiGPSSCPort;
        TPWrite " Connection established.";
        TPWrite "Waiting for target...";
        
        WHILE TRUE DO
            ! Receive calibration target message from server
            ReceiveMessage tcpip_socket, recv_msg_type, recv_raw_message;
            
            IF (recv_msg_type = 2) THEN
                ! Unpack RFLCalibPose message 
                UnpackMSGRFLCalibPose recv_raw_message, rfl_calib_pose_msg;
                TPWrite "**************************************";
                TPWrite " Received target"; 
                
                ! Move robot to target
                TPWrite "Moving to target...";
                ConfJ \off;
                MoveJ rfl_calib_pose_msg.rob_target, igps_sc_speed, fine, tool0;
                
                ! Get current end effector pose relative to world and robot base   
                TPWrite "Getting and sending robot feedback..."; 
                WaitTime 1;
                
                rfl_calib_pose_feedback_msg.end_effector_world := CPoseT(tool0, wobj0);
                rfl_calib_pose_feedback_msg.end_effector_base := CPoseT(tool0, wobj_base_21);
                
                ! Pack RFLCalibPoseFeedback message.
                PackMSGRFLCalibPoseFeedback rfl_calib_pose_feedback_msg, 1, send_raw_message;
                
                ! Send back current end effector pose relative to world and robot base
                SendMessage tcpip_socket, send_raw_message;
                TPWrite " Feedback sent.";
                TPWrite "Waiting for target...";
            ENDIF
        ENDWHILE
        
        ! Close TCP/IP client
        CloseTCPIPClient tcpip_socket;
        TPWrite "TCP/IP socket closed.";
    ENDPROC
    
ENDMODULE