MODULE ETH_Helper_22_old
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
		MoveAbsJ [[0.00175604,-79.9994,70.0002,0.00222322,10.0063,-0.00160446],[25000,-9000,-4514.99,0,0,0]]\NoEOffs, v1000, z50, tool0;
	ENDPROC
	PROC rBund()
		AccSet 50, 50;
		!MoveAbsJ [[0.00111227,-72.9968,73.0009,0.0120194,-0.00406334,-0.00144351],[26596.5,-8254.79,-4514.8,0,0,0]]\NoEOffs, v1000, z50, tool0;
		MoveAbsJ [[-23.7061,-31.8878,0.00247276,0.000117508,-0.00054601,0.000267211],[20000,-11247,-3000,0,0,0]]\NoEOffs, v1000, fine, tool0;
	ENDPROC






ENDMODULE