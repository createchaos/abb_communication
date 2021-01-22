MODULE ETH_Helper_21_old
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
    ! Function    :     Move Robot to safe position on top
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.03.02
    ! **************** ETH Zürich *******************
    !
    PROC rMoveToSafePosOnTop()
        !
        ! Wait for Robot in position or zero speed
        WaitRob\ZeroSpeed;
        !
        ! Read current position
        jpCurrent:=CJointT();
        !
        ! Us Safepos as base
        jpNext:=jpSafePosOnTop;
        !
        ! Overwrite RobPos, X-Axis and Y-Axis 
        jpNext.robax:=jpCurrent.robax;
        jpNext.extax.eax_a:=jpCurrent.extax.eax_a;
        jpNext.extax.eax_b:=jpCurrent.extax.eax_b;
        jpNext.robax:=jpSafePosOnTop.robax;
        ! 
        ! Move to top position
        MoveAbsJ jpNext,vGuedelMin,fine,tool0;
        !
        RETURN ;
    ENDPROC
	PROC Routine3()
		AccSet 30, 30;
		MoveAbsJ [[0.000258156,-72.9558,72.9592,0.000258228,-0.00155605,0.00412452],[39000,-0.0257801,-4609.8,0,0,0]]\NoEOffs, v1000, z50, tool0;
	ENDPROC
	PROC rBund()
		AccSet 50, 50;
		!MoveAbsJ [[0.0032195,-72.9987,72.9937,-0.00294612,-0.0112526,0.0501216],[26596.5,-4212.46,-4302.71,0,0,0]]\NoEOffs, v1000, z50, tool0;
		MoveAbsJ [[39.1751,36.7984,-3.23967,0.000258228,4.16719E-06,-4.50984E-05],[20000,-3443.8,-3000,0,0,0]]\NoEOffs, v1000, fine, tool0;
	ENDPROC






ENDMODULE