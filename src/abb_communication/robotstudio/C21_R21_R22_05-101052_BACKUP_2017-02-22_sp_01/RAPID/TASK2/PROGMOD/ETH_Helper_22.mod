MODULE ETH_Helper_22
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
    ! FUNCTION    :  Helper Routines for ETH
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2016.08.09 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Stor current position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.16
    ! **************** ETH Zürich *******************
    !
    PROC rStorePos()
        !
        ! Check that the robot is not in motion
        WaitRob\ZeroSpeed;
        !
        ! When robot in safepos z then not store
        IF fCompJPos(jpSafePosZ,1\bCheckZAxis:=TRUE\nLimMM:=1) THEN
            !
            ! Robot in SafePosZ => not stred
        ELSE
            ! Robot not in SafePosZ => stred
            !
            ! Store current position
            pStore:=CRobT(\Tool:=tool0\WObj:=wobj0);
            !
            ! Store current jointvalues
            jpStore:=CJointT();
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Current position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.21
    ! **************** ETH Zürich *******************
    !
    PROC rCurrentPos()
        !
        ! Check that the robot is not in motion
        WaitRob\ZeroSpeed;
        !
        ! Store current position
        pCurrent:=CRobT(\Tool:=tool0\WObj:=wobj0);
        !
        ! Store current jointvalues
        jpCurrent:=CJointT();
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Move back to stored position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.16
    ! **************** ETH Zürich *******************
    !
    PROC rRestorePos()
        VAR bool bConfJOff;
        !
        ! Read and store configuration state
        IF C_MOTSET.conf.jsup=FALSE bConfJOff:=TRUE;
        !
        ! Activate configuration
        ConfJ\On;
        !
        ! Move to stored position
        MoveJ pStore,vRestorPos,fine,tool0\WObj:=wobj0;
        !
        ! When the configuration was deactivated restor the state
        IF bConfJOff=TRUE ConfJ\Off;
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Move Robot to safe position on top with Z-Axis
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.03.02
    ! **************** ETH Zürich *******************
    !
    PROC rMoveToSafePosZ()
        !
        ! Wait for Robot in position or zero speed
        WaitRob\ZeroSpeed;
        !
        ! Read current position
        jpTemp:=CJointT();
        !
        ! Move Z-Axis in safty position on top
        jpTemp.extax.eax_c:=nSafePosZ;
        MoveAbsJ jpTemp,vSafePosMed,z100,tool0;
        !
        ! Overwrite RobPos, X-Axis and Y-Axis 
        jpSafePosZ.extax.eax_a:=jpTemp.extax.eax_a;
        jpSafePosZ.extax.eax_b:=jpTemp.extax.eax_b;
        ! 
        ! Move to safty position on top
        MoveAbsJ jpSafePosZ,vSafePosMax,z100,tool0;
        !
        RETURN ;
    ENDPROC

    !************************************************
    ! Function    :     Move Z-Axis to top position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.12.20
    ! **************** ETH Zürich *******************
    !
    PROC rMoveZAxToTop()
        !
        ! Wait for Robot in position or zero speed
        WaitRob\ZeroSpeed;
        !
        ! Read current position
        jpTemp:=CJointT();
        !
        ! Move Z-Axis in safty position on top
        jpTemp.extax.eax_c:=nTopPosZ;
        MoveAbsJ jpTemp,vSafePosMed,z100,tool0;
        !
        RETURN ;
    ENDPROC
    
    !************************************************
    ! Function    :     Test Relativ Task X-, Y-, Z-Axis 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.17
    ! **************** ETH Zürich *******************
    ! Code example:
    ! IF fCheckAchsPos(jpRoStop,1) THEN
    !
    FUNC bool fCompJPos(
        jointtarget jpCompare,
        num nLimDec,
        \bool bCheckXAxis,
        \bool bCheckYAxis,
        \bool bCheckZAxis,
        \num nLimMM)
        !
        ! Input Parameter:
        ! Jointarget to compare
        ! Limt [°] for comparability test
        ! opt. compare X-Axis
        ! opt. compare Y-Axis
        ! opt. compare Z-Axis
        ! Limt [mm] for comparability test
        !
        !  Return Parameter: 
        ! comparability test true or false
        VAR bool bRes:=TRUE;
        ! 
        ! Intern Declaration
        VAR jointtarget jpCurrent;
        !
        ! Start Function
        !
        ! Wait for Robo
        WaitRob\ZeroSpeed;
        !
        ! Read current jonttarget
        jpCurrent:=CJointT();
        !
        ! Compare Roboter Joints
        !
        ! If the values are too high, bRes go to "FALSE"
        IF Abs(jpCompare.robax.rax_1-jpCurrent.robax.rax_1)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_2-jpCurrent.robax.rax_2)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_3-jpCurrent.robax.rax_3)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_4-jpCurrent.robax.rax_4)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_5-jpCurrent.robax.rax_5)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_6-jpCurrent.robax.rax_6)>=nLimDec bRes:=FALSE;
        !
        ! Compare X-Axis
        IF Present(bCheckXAxis) AND bCheckXAxis=TRUE THEN
            IF Abs(jpCompare.extax.eax_a-jpCurrent.extax.eax_a)>=nLimMM bRes:=FALSE;
        ENDIF
        !
        ! Compare Y-Axis
        IF Present(bCheckYAxis) AND bCheckYAxis=TRUE THEN
            IF Abs(jpCompare.extax.eax_b-jpCurrent.extax.eax_b)>=nLimMM bRes:=FALSE;
        ENDIF
        !
        ! Compare Z-Axis
        IF Present(bCheckZAxis) AND bCheckZAxis=TRUE THEN
            TPWrite ""\Num:=Abs(jpCompare.extax.eax_c-jpCurrent.extax.eax_c);
            IF Abs(jpCompare.extax.eax_c-jpCurrent.extax.eax_c)>=nLimMM bRes:=FALSE;
        ENDIF
        RETURN bRes;
    ENDFUNC
	PROC rSysChangePos()
		MoveAbsJ [[3.9317E-05,-0.0027027,-0.000318808,0.000392166,-0.000155956,-0.000593919],[21577.5,-5150,-4515,0,0,0]]\NoEOffs, v1000, z50, tool0;
	ENDPROC

ENDMODULE