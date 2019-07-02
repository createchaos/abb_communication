MODULE ETH_FatDataMa
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
    ! FUNCTION    :  Includ all specific Data's for Factory acceptance tests
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
    !
    !************************************************
    ! Notes      :     
    !
    ! Fat = Factory acceptance test
    !
    !************************************************

    !
    !************************************************
    ! Declaration :     bool
    !************************************************
    !
    PERS bool bFatMaOn:=TRUE;
    PERS bool bFatRefPointOn:=FALSE;
    PERS bool bNoJobROB11:=TRUE;
    PERS bool bNoJobROB12:=TRUE;
    PERS bool bNoJobROB21:=TRUE;
    PERS bool bNoJobROB22:=TRUE;

    
    !
    !************************************************
    ! Declaration :     num
    !************************************************
    !
    PERS num nRefPointZOffs:=1000;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    PERS string stJobFat:="rRelativ";

    CONST string stMsgChoRobRefPoint{5}:=["Wich Robot shold go to the RefPoint?"," "," "," "," "];



    !************************************************
    ! Declaration :     btnres
    !************************************************
    !


    !************************************************
    ! Declaration :     listitem
    !************************************************
    !
    CONST listitem liFacAccTestHome{8}:=[["","1. Test: Relativ"],["","2. Test: Workspace"],["","3. Test: Repeatability"],["","4. Test: World Coordinates"],["","5. Test: MultiMove"],["","6. Test: Workobject"],["","7. Test: Pick & Place"],["","8. Test: Path"]];

    !************************************************
    ! Declaration :     syncident
    !************************************************
    !
    ! Main
    VAR syncident idETH_FatSta;
    VAR syncident idETH_FatEnd;
    !
    ! Test 1
    VAR syncident idETH_FatUserDecision;
    VAR syncident idETH_FatExeEnd;
    ! Test 2 (Safepos)
    VAR syncident idETH_FatSafePosR11;
    VAR syncident idETH_FatSafePosR12;
    VAR syncident idETH_FatSafePosR21;
    VAR syncident idETH_FatSafePosR22;
    !
    ! Test 2 (Z-Axis)
    VAR syncident idETH_FatMoveMinMaxDoneZ11;
    VAR syncident idETH_FatMoveMinMaxDoneZ12;
    VAR syncident idETH_FatMoveMinMaxDoneZ21;
    VAR syncident idETH_FatMoveMinMaxDoneZ22;
    !
    ! Test 2 (Y-Axis)
    VAR syncident idETH_FatMoveMinDoneY11;
    VAR syncident idETH_FatMoveMinDoneY12;
    VAR syncident idETH_FatMoveMinDoneY21;
    VAR syncident idETH_FatMoveMinDoneY22;
    VAR syncident idETH_FatMoveMaxDoneY12;
    VAR syncident idETH_FatMoveMaxDoneY11;
    VAR syncident idETH_FatMoveMaxDoneY22;
    VAR syncident idETH_FatMoveMaxDoneY21;
    !
    ! Test 2 (X-Axis)
    VAR syncident idETH_FatMoveMinDoneX11;
    VAR syncident idETH_FatMoveMinDoneX21;
    VAR syncident idETH_FatMoveMaxDoneX21;
    VAR syncident idETH_FatMoveMaxDoneX22;
    !
    ! Test 3
    VAR syncident idETH_Fat3UserDecision;
    VAR syncident idETH_Fat3ExeEnd;
    !
    ! Test 5 
    VAR syncident idETH_Fat5MMPrePos;
    VAR syncident idETH_Fat5MMPosR11;
    VAR syncident idETH_Fat5MMPosR12;
    VAR syncident idETH_Fat5MMPosR21;
    VAR syncident idETH_Fat5MMPosR22;
    VAR syncident idETH_Fat5MMStart;
    VAR syncident idETH_Fat5MMEnd;

    !************************************************
    ! Declaration :     speeddata
    !************************************************
    !
    PERS speeddata vFatRel:=[800,50,800,50];

    !************************************************
    ! Declaration :     clock
    !************************************************
    !

ENDMODULE