
MODULE A009_Motion_22

    VAR robtarget home_pos;
    
    PROC rMainA009()
        
        ! Insert from 15.9.16pf
        WaitSyncTask idMainA009Sta,tlAll;
        TPWrite "A009 Start";

        init;

        TPWrite "Motion: Start waiting for positions in buffer and move accordingly";

        WHILE (TRUE) DO
            IF BUFFER_LENGTH_R4 > 0 THEN
                IF msg_lock=FALSE THEN
                    execute_from_buffer;
                ENDIF
            ENDIF
            WaitTime 0.05;
        ENDWHILE

        ! Insert from 15.9.16pf
        WaitSyncTask idMainA009End,tlAll;
        TPWrite "A009 End";

    ENDPROC

ENDMODULE