MODULE Sender
    
    
    PROC main()
        
        init; !Set all variables       
        connect_trap_routines; !Connect all routines

        TPWrite "Sender Server: Waiting for connection.";
	    init_socket socket_server,port_sender; !create server and wait for incoming connections
        wait_for_client socket_server,socket_client \wait_time:=1.0; !wait_for_client socket_server,socket_client;
        
        WHILE ( TRUE ) DO
            TCPIP_send_msg_cp_joint socket_client;
            WaitTime 0.1;            !TPWrite "SEND CARTESIAN"; 
            TCPIP_send_msg_cp_cartesian socket_client;
            WaitTime 0.1;            !TPWrite "SEND CARTESIAN";
            TCPIP_send_msg_cp_cartesian_base socket_client;
            WaitTime 0.1;            !TPWrite "SEND CARTESIAN";

        ENDWHILE 
        
        Idelete pers_i_1;
        Idelete pers_i_2;

        ERROR (ERR_SOCK_CLOSED)
        	IF (ERRNO=ERR_SOCK_CLOSED) THEN
                SkipWarn;  !TBD: include this error data in the message logged below?
                ErrWrite \W,"SANS Sender disconnect","Connection lost.  Waiting for new connection.";
                
                Idelete pers_i_1;
                Idelete pers_i_2;
                
                ExitCycle; !restart program
        	ELSE
        		TRYNEXT;
        	ENDIF
        UNDO   
    ENDPROC
    
ENDMODULE