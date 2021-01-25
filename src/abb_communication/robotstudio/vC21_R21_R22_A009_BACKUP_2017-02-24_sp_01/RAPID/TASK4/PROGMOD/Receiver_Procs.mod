MODULE Receiver_Procs

    !for client
    VAR num retry_no:=0;

    VAR socketdev receiver_socket;

    VAR socketdev socket_server;
    VAR socketdev socket_client;

    PROC init()

        !initialize robot
        TPWrite "Initialization Receiver Client";

        msg_lock:=FALSE;

        msg_rec_counter:=0;

        BUFFER_LENGTH_R1:=0;
        READ_PTR_R1:=1;
        WRITE_PTR_R1:=1;

        BUFFER_LENGTH_R2:=0;
        READ_PTR_R2:=1;
        WRITE_PTR_R2:=1;

        BUFFER_LENGTH_R3:=0;
        READ_PTR_R3:=1;
        WRITE_PTR_R3:=1;

        BUFFER_LENGTH_R4:=0;
        READ_PTR_R4:=1;
        WRITE_PTR_R4:=1;


        TPWrite "Write pointer:"+ValToStr(WRITE_PTR_R1);
        TPWrite "Write pointer:"+ValToStr(WRITE_PTR_R2);
        TPWrite "Write pointer:"+ValToStr(WRITE_PTR_R3);
        TPWrite "Write pointer:"+ValToStr(WRITE_PTR_R4);

        msg_send_counter_lock:=FALSE;

    ENDPROC

    PROC reset_after_connection_stop()

        TPWrite "CONNECTION ERROR, pp will be moved to main, vars are reset";

        msg_lock:=FALSE;
        msg_send_counter_lock:=FALSE;

        msg_rec_counter:=0;
        cmd_exec_counter:=0;

        BUFFER_LENGTH_R1:=0;
        READ_PTR_R1:=1;
        WRITE_PTR_R1:=1;

        BUFFER_LENGTH_R2:=0;
        READ_PTR_R2:=1;
        WRITE_PTR_R2:=1;

        BUFFER_LENGTH_R3:=0;
        READ_PTR_R3:=1;
        WRITE_PTR_R3:=1;

        BUFFER_LENGTH_R4:=0;
        READ_PTR_R4:=1;
        WRITE_PTR_R4:=1;

        reset_to_main:=TRUE;

        !StopMove;
        !ClearPath;
        !StopMoveReset;
        !StartMove;

    ENDPROC

    PROC write_to_buffer(VAR TCPIP_MSG_COMMAND act_message_command)

        !VAR num intval := act_message_command.arbitrary;

        TPWrite ValToStr(act_message_command.arbitrary);

        TEST act_message_command.arbitrary

        CASE 1:
            WaitTestAndSet msg_lock;
            !acquire data-lock
            tcpip_message_command_buffer_r1{WRITE_PTR_R1}:=act_message_command;
            BUFFER_LENGTH_R1:=BUFFER_LENGTH_R1+1;
            WRITE_PTR_R1:=(WRITE_PTR_R1 MOD MAX_BUFFER_SIZE)+1;
            msg_lock:=FALSE;
        CASE 2:
            WaitTestAndSet msg_lock;
            !acquire data-lock
            tcpip_message_command_buffer_r2{WRITE_PTR_R2}:=act_message_command;
            BUFFER_LENGTH_R2:=BUFFER_LENGTH_R2+1;
            WRITE_PTR_R2:=(WRITE_PTR_R2 MOD MAX_BUFFER_SIZE)+1;
            msg_lock:=FALSE;
        CASE 3:
            WaitTestAndSet msg_lock;
            !acquire data-lock
            tcpip_message_command_buffer_r3{WRITE_PTR_R3}:=act_message_command;
            BUFFER_LENGTH_R3:=BUFFER_LENGTH_R3+1;
            WRITE_PTR_R3:=(WRITE_PTR_R3 MOD MAX_BUFFER_SIZE)+1;
            msg_lock:=FALSE;
        CASE 4:
            WaitTestAndSet msg_lock;
            !acquire data-lock
            tcpip_message_command_buffer_r4{WRITE_PTR_R4}:=act_message_command;
            BUFFER_LENGTH_R4:=BUFFER_LENGTH_R4+1;
            WRITE_PTR_R4:=(WRITE_PTR_R4 MOD MAX_BUFFER_SIZE)+1;
            msg_lock:=FALSE;
        DEFAULT:
            TPWrite "WRONG ROBOTNUMBER";
        ENDTEST


    ENDPROC



ENDMODULE