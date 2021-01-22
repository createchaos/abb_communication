MODULE ETH_Jobs_Ma
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
    ! FUNCTION    :  Job Routines for ETH Master
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
    ! Function    :     Master Main Routine for Project A009
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rMainA009()
        !
        WaitSyncTask idMainA009Sta,tlAll;
        !
        ! Temp Msg for Operator
        TPWrite "Master in rMainA009";
        !
        ! Main Code for Master from Project A009
        ! Free to define form Project user
        ! 
        WaitSyncTask idMainA009End,tlAll;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Master Main Routine for Project A011
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.12.19
    ! **************** ETH Zürich *******************
    !
    PROC rMainA011()
        !
        WaitSyncTask idMainA011Sta,tlAll;
        !
        ! Temp Msg for Operator
        TPWrite "Master in rMainA011";
        !
        ! Main Code for Master from Project A019
        ! Free to define form Project user
        ! 
        WaitSyncTask idMainA011End,tlAll;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Master rExample Routine form ABB
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rExample()
        !
        WaitSyncTask idABB_ExampleSta,tlAll;
        !
        ! Temp Msg for Operator
        TPWrite "Master in ABB Example";
        !
        ! Placeholder for Master Code 
        ! 
        WaitSyncTask idABB_ExampleEnd,tlAll;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Master rExample Routine form ABB
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rMoveToBreakCheckPos()
        !
        WaitSyncTask idABB_BreakCheckStart,tlAll;
        !
        ! Placeholder for Master Code 
        ! 
        WaitSyncTask idABB_BreakCheckEnd,tlAll;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Master rMoveToCalibPos Routine form ABB
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rMoveToCalibPos()
        !
        WaitSyncTask idABB_CalibPosSta,tlAll;
        !
        ! Temp Msg for Operator
        TPWrite "Master in ABB Move to Calibration position";
        !
        ! Placeholder for Master Code 
        ! 
        WaitSyncTask idABB_CalibPosEnd,tlAll;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Master Main Routine for Project MAS
    ! Programmer  :     Stefana Parascho
    ! Date        :     2017.02.20
    ! **************** ETH Zürich *******************
    !
    PROC rMainAxxx()
        !
        WaitSyncTask idMainAxxxSta,tlAll;
        !
        ! Temp Msg for Operator
        TPWrite "Master in rMainMAS";
        !
        ! Main Code for Master from Project A019
        ! Free to define form Project user
        ! 
        WaitSyncTask idMainAxxxEnd,tlAll;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
ENDMODULE