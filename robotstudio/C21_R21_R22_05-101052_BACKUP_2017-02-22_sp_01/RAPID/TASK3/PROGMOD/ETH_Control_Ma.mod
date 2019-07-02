MODULE ETH_Control_Ma
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIP CO 11.1 / Gustave-Naville-Weg 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A011_RFL
    !
    ! FUNCTION    :  Control Routines for ETH
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2016.08.11 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Main
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC main()
        !
        ! Initalisation 
        rInitTask;
        !
        ! Work process
        WHILE bRun=TRUE DO
            !
            ! Idle Loop
            WHILE bWaitForJob DO
                !
                ! User Interface
                rUIMasterWindow;
                ! 
                ! Short waittime
                WaitTime 0.1;
            ENDWHILE
            !
            ! Execute  Job from Master
            rExecuteJobFrmMa;
        ENDWHILE
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Task
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rInitTask()
        ! 
        WaitSyncTask idInitTaskSta,tlAll;
        !
        ! Clear TP Window
        TPErase;
        !
        ! Variables
        rInitVar;
        !
        WaitSyncTask idInitTaskEnd,tlAll;
        ! 
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rInitVar()
        ! 
        bWaitForJob:=TRUE;

        stJobFrmMa:="InitVar";


    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Execute Job from Master
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rExecuteJobFrmMa()
        !
        WaitSyncTask idExeJobFrmMaSta,tlAll;
        !
        %stJobFrmMa %;
        !
        WaitSyncTask idExeJobFrmMaEnd,tlAll;
        ! 
        ! Job finish
        bWaitForJob:=TRUE;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     ProgError
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rProgError()
        ! 
        ! User Info
        TPWrite "Program Error";
        !
        ! Stop Program
        Stop;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE