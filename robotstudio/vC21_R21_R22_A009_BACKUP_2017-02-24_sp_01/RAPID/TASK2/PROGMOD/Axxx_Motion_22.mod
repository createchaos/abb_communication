MODULE Axxx_Motion_22
    
    !VAR robtarget home_pos;

    PROC rMainAxxx()

        ! Insert from 15.9.16pf
        WaitSyncTask idMainAxxxSta,tlAll;
        TPWrite "Axxx Start";

        init;

        TPWrite "Motion: Start waiting for positions in buffer and move accordingly";

        WHILE (TRUE) DO
            IF BUFFER_LENGTH_R4>0 THEN
                IF msg_lock=FALSE THEN
                    execute_from_buffer;
                ENDIF
            ENDIF
            WaitTime 0.05;
        ENDWHILE

        ! Insert from 15.9.16pf
        WaitSyncTask idMainAxxxEnd,tlAll;
        TPWrite "Axxx End";

    ENDPROC
    
ENDMODULE