MODULE ETH_FatMa
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
    ! FUNCTION    :  Routines for ETH Factary acceptance test
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2016.11.14 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Master rFacAccTest Routine form ETH
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.14
    ! **************** ETH Zürich *******************
    !
    PROC rFacAccTest()
        !
        ! Activate FAT Loop
        bFatMaOn:=TRUE;
        ! 
        ! Started Job from Master 
        WaitSyncTask idETH_FatSta,tlAll;
        !
        ! Loop for specific FAT's 
        WHILE bFatMaOn=TRUE DO
            !
            ! Choose the test mode
            rUIFacAccWindow;
            !
            ! Sync the user decision
            WaitSyncTask idETH_FatUserDecision,tlAll;
            !
            ! Check for Job
            IF bFatMaOn=TRUE THEN
                !
                ! 
                ! Exectue the Job
                %stJobFat %;
                !
                ! Wait for executing end
                WaitSyncTask idETH_FatExeEnd,tlAll;
            ENDIF
        ENDWHILE
        !
        ! Specific Job is finish
        WaitSyncTask idETH_FatEnd,tlAll;
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     User Interface Factory acceptance tests
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC rUIFacAccWindow()
        ! 
        ! User window for Fat 
        nUiListItem:=UIListView(
                    \Result:=btnAnswer
                    \Header:="Factory acceptance tests",
                    liFacAccTestHome
                    \Buttons:=btnOKCancel
                    \Icon:=iconInfo
                    \DefaultIndex:=1);

        IF btnAnswer=resOK THEN
            !
            ! User selct a item
            !
            ! Check selected item
            TEST nUiListItem
            CASE 1:
                ! Item 1. Test: Relativ
                stJobFat:="rRelativ";
                !
            CASE 2:
                ! Item 2. Test: Workspace
                stJobFat:="rWorkspace";
                !
            CASE 3:
                ! Item 3. Test: Repeatability
                stJobFat:="rRefPoint";
                !
                ! Activate RefPoint Loop
                bFatRefPointOn:=TRUE;
                !
            CASE 4:
                ! Item 4. Test: World Coordinates
                stJobFat:="rWorldCoordinates";
                !
            CASE 5:
                ! Item 5. Test: MultiMove
                stJobFat:="rMultiMove";
                !
            CASE 6:
                ! Item 6. Test: Workobject
                Stop;
            CASE 7:
                ! Item 7. Test: Pick & Place
                Stop;
            CASE 8:
                ! Item 8. Test: Path
                Stop;
            DEFAULT:
                ! Undefined Item 
                rProgError;
            ENDTEST
            !
        ELSE
            ! Cancel was selcted
            !
            ! Deactivate Fat loop
            bFatMaOn:=FALSE;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Test Relativ Task X-, Y-, Z-Axis 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.14
    ! **************** ETH Zürich *******************
    !
    PROC rRelativ()
        !
        ! Placehoder for Code
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Test Workspace 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.14
    ! **************** ETH Zürich *******************
    !
    PROC rWorkspace()
        !
        ! Test 2 (Safepos)
        WaitSyncTask idETH_FatSafePosR11,tlAll;
        WaitSyncTask idETH_FatSafePosR12,tlAll;
        WaitSyncTask idETH_FatSafePosR21,tlAll;
        WaitSyncTask idETH_FatSafePosR22,tlAll;
        !
        ! Test 2 (Z-Axis)
        WaitSyncTask idETH_FatMoveMinMaxDoneZ11,tlAll;
        WaitSyncTask idETH_FatMoveMinMaxDoneZ12,tlAll;
        WaitSyncTask idETH_FatMoveMinMaxDoneZ21,tlAll;
        WaitSyncTask idETH_FatMoveMinMaxDoneZ22,tlAll;
        !
        ! Test 2 (Y-Axis)
        WaitSyncTask idETH_FatMoveMaxDoneY11,tlAll;
        WaitSyncTask idETH_FatMoveMaxDoneY12,tlAll;
        WaitSyncTask idETH_FatMoveMaxDoneY21,tlAll;
        WaitSyncTask idETH_FatMoveMaxDoneY22,tlAll;
        WaitSyncTask idETH_FatMoveMinDoneY12,tlAll;
        WaitSyncTask idETH_FatMoveMinDoneY11,tlAll;
        WaitSyncTask idETH_FatMoveMinDoneY22,tlAll;
        WaitSyncTask idETH_FatMoveMinDoneY21,tlAll;
        !
        ! Test 2 (X-Axis)
        WaitSyncTask idETH_FatMoveMinDoneX11,tlAll;
        WaitSyncTask idETH_FatMoveMinDoneX21,tlAll;
        WaitSyncTask idETH_FatMoveMaxDoneX21,tlAll;
        WaitSyncTask idETH_FatMoveMaxDoneX22,tlAll;

        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Test Repeatability Move to RefPoint  
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.14
    ! **************** ETH Zürich *******************
    !
    PROC rRefPoint()
        !
        !
        ! Loop for RefPoint FAT's 
        WHILE bFatRefPointOn=TRUE DO
            !
            ! Set variables
            bNoJobROB11:=TRUE;
            bNoJobROB12:=TRUE;
            bNoJobROB21:=TRUE;
            bNoJobROB22:=TRUE;
            !
            ! User choos wich robot shold move to RefPoint
            btnAnswer:=UIMessageBox(
                \Header:="RefPoint"
                \MsgArray:=stMsgChoRobRefPoint
                \BtnArray:=stBtnRobTasks
                \Icon:=iconInfo);
            IF btnAnswer=1 THEN
                ! T_ROB11
                !
                bNoJobROB11:=FALSE;
                !
            ELSEIF btnAnswer=2 THEN
                ! T_ROB12
                !
                bNoJobROB12:=FALSE;
                !
            ELSEIF btnAnswer=3 THEN
                ! T_ROB21
                !
                bNoJobROB21:=FALSE;
                !
            ELSEIF btnAnswer=4 THEN
                ! T_ROB22
                !
                bNoJobROB22:=FALSE;
                !
            ELSEIF btnAnswer=5 THEN
                ! Exit
                !
                bFatRefPointOn:=FALSE;
            ELSE
                ! No such case defined
            ENDIF
            !
            ! Sync user decision
            WaitSyncTask idETH_Fat3UserDecision,tlAll;
            ! Wait for the end
            WaitSyncTask idETH_Fat3ExeEnd,tlAll;

        ENDWHILE

        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Test World Coordinates 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.18
    ! **************** ETH Zürich *******************
    !
    PROC rWorldCoordinates()
        !
        ! Placehoder for Code
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Test MultiMove 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.22
    ! **************** ETH Zürich *******************
    !
    PROC rMultiMove()
        !
        ! Wait for all Robots
        WaitSyncTask idETH_Fat5MMPrePos,tlAll;
        !
        ! Wait for all Robots in start position
        WaitSyncTask idETH_Fat5MMPosR11,tlAll;
        WaitSyncTask idETH_Fat5MMPosR12,tlAll;
        WaitSyncTask idETH_Fat5MMPosR21,tlAll;
        WaitSyncTask idETH_Fat5MMPosR22,tlAll;
        !
        ! Wait for all Robots in start position
        
        ! Placehoder for Code
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
ENDMODULE