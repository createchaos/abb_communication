MODULE A011_Control_21
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIB C13 / Stefano-Franscini-Platz 1 
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A011_RFL/iGPS
    !
    ! FUNCTION    :  Control Routines for iGPS
    !
    ! AUTHOR      :  Philippe Fleischmann / Lukas Stadelmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2017.01.18 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2017
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Start Project specific Code
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.01.18
    ! **************** ETH Zürich *******************
    !
    PROC rMainA011()
        ! Project Start
        WaitSyncTask idMainA011Sta,tlAll;
        TPWrite "A011 Start";

        ! Run data set creation
        data_set_creation;        
        Stop;
        
        
        ! Project End
        WaitSyncTask idMainA011End,tlAll;
        TPWrite "A011 End";
        ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE