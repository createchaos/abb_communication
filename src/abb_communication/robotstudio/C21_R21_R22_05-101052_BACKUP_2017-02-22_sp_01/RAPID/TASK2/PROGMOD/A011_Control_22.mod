MODULE A011_Control_22
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIB C13 / Stefano-Franscini-Platz 1 
    ! CH-8093 Z�rich
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
    ! Copyright   :  ETH Z�rich (CH) 2017
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Start Project specific Code
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.01.18
    ! **************** ETH Z�rich *******************
    !
    PROC rMainA011()
        ! Project Start
        WaitSyncTask idMainA011Sta,tlAll;
        TPWrite "A011 Start";

        ! Cose Lukas (Main)
        ! ...
        Stop;
        
        
        ! Project End
        WaitSyncTask idMainA011End,tlAll;
        TPWrite "A011 End";
        ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE