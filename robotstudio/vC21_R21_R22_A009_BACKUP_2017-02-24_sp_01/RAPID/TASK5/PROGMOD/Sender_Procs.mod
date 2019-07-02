MODULE Sender_Procs
    
   !for client
    VAR num retry_no:=0;
    
    VAR socketdev sender_socket;
    
    VAR socketdev socket_server;
    VAR socketdev socket_client;
    
    !for trap routines
    VAR intnum pers_i_1;
    VAR intnum pers_i_2;
    
    PROC init()
        !initialize robot
        TPWrite "Initialization Sender Client";
        
        !trap routines
        send_msg_cmd_exec:=FALSE;
        send_msg_cmd_rcv:=FALSE;
        sender_socket_lock:=FALSE;
        
        !added stefana
        cmd_exec_lock:=FALSE;
        
        ClkReset tcpip_clock;
        ClkStart tcpip_clock;

        msg_send_counter:=0;
        msg_send_counter_lock:=FALSE;

    ENDPROC
    
    PROC connect_trap_routines()
        
        CONNECT pers_i_1 WITH i_send_msg_cmd_exec;
        IPers send_msg_cmd_exec, pers_i_1;
        
        CONNECT pers_i_2 WITH i_send_msg_cmd_rcv;
        IPers send_msg_cmd_rcv, pers_i_2;

    ENDPROC
    
    TRAP i_send_msg_cmd_exec
        IF send_msg_cmd_exec = TRUE THEN
            TPWrite "Send command executed started";
            WaitTestAndSet cmd_exec_lock;  !acquire data-lock
                Incr cmd_exec_counter;
            cmd_exec_lock:=FALSE;
            
            TPWrite "exec: " + ValToStr(cmd_exec_counter);
            TCPIP_send_msg_command_executed socket_client;
            send_msg_cmd_exec:=FALSE;
        ENDIF
        WaitTime 0.005;
    ENDTRAP
    
    TRAP i_send_msg_cmd_rcv
        IF send_msg_cmd_rcv = TRUE THEN
            !TPWrite "Send command received";
            TPWrite "rec: " + ValToStr(msg_rec_counter);
            TCPIP_send_msg_command_received socket_client;
            send_msg_cmd_rcv:=FALSE;
        ENDIF
        WaitTime 0.005;
    ENDTRAP
    
ENDMODULE