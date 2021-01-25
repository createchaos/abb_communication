MODULE ETH_HMI_Ma
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
    ! Function    :     User Interface Master Window
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rUIMasterWindow()
        ! 
        nUiListItem:=UIListView(
                    \Result:=btnAnswer
                    \Header:="ETH Zürich Digital Fabrication",
                    liMaWinHome
                    \Buttons:=btnOKCancel
                    \Icon:=iconInfo
                    \DefaultIndex:=1);

        IF btnAnswer=resOK THEN


            TEST nUiListItem
            CASE 1:
                ! Item ABB Example
                stJobFrmMa:="rExample";
                !
            CASE 2:
                ! Item ABB Calibration
                stJobFrmMa:="rMoveToCalibPos";
                !
            CASE 3:
                ! Item ABB Move to BreakCheckPos
                stJobFrmMa:="rMoveToBreakCheckPos";
                !
            CASE 4:
                ! Item ETH Factory acceptance test
                stJobFrmMa:="rFacAccTest";
                !
            CASE 5:
                ! Item A009 Stefana
                stJobFrmMa:="rMainA009";
                !
            CASE 6:
                ! Item A011 iGPS
                stJobFrmMa:="rMainA011";
                !
            !added sp 170220
            CASE 7:
                ! Item AXXX MAS
                stJobFrmMa:="rMainAxxx";
            !
            DEFAULT:
                ! Undefined Item 
                rProgError;
            ENDTEST
            !
            ! Master have a Job
            bWaitForJob:=FALSE;
        ELSE
            ! User has select Cancel
        ENDIF

        ! Start Job for Tasks

    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE