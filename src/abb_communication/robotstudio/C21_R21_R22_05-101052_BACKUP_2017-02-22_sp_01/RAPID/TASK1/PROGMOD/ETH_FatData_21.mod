MODULE ETH_FatData_21
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

    !************************************************
    ! Declaration :     bool
    !************************************************
    !
    PERS bool bFatMaOn:=TRUE;
    PERS bool bFatRefPointOn:=FALSE;
    !
    TASK PERS bool bFatTaOn:=TRUE;

    PERS bool bNoJobROB11:=TRUE;
    PERS bool bNoJobROB12:=TRUE;
    PERS bool bNoJobROB21:=TRUE;
    PERS bool bNoJobROB22:=TRUE;
    !
    !************************************************
    ! Declaration :     num
    !************************************************
    !
    PERS num nAccRamp:=100;
    PERS num nInPosWindowForXAxis:=1;
    PERS num nRefPointZOffs:=1000;
    !
    TASK PERS num nTempRelValue:=4000;


    !************************************************
    ! Declaration :     string
    !************************************************
    !
    PERS string stJobFat:="rRelativ";


    !************************************************
    ! Declaration :     btnres
    !************************************************
    !

    !************************************************
    ! Declaration :     listitem
    !************************************************
    !
    CONST listitem liFacAccTestRel{3}:=[["","X-Axis"],["","Y-Axis"],["","Z-Axis"]];

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
    !
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
    PERS speeddata vFatWorSpa:=[1000,500,1000,500];
    !
    PERS speeddata vWordPointMin:=[2000,100,250,500];
    PERS speeddata vWordPointMed:=[2000,100,250,500];
    PERS speeddata vWordPointMax:=[2000,500,1000,1000];
    !
    PERS speeddata vMultiMoveMin:=[2000,100,250,500];
    PERS speeddata vMultiMoveMed:=[2000,100,250,500];
    PERS speeddata vMultiMoveMax:=[2000,500,1000,1000];
    
    !************************************************
    ! Declaration :     clock
    !************************************************
    !
    VAR clock clkRob11;

    !************************************************
    ! Declaration :     tooldata
    !************************************************
    !
    TASK PERS tooldata tTeachTip:=[TRUE,[[0.309402,-0.337782,206.826],[1,0,0,0]],[0.001,[0,0,0.001],[1,0,0,0],0,0,0]];

    !************************************************
    ! Declaration :     wobjdata
    !************************************************
    !
    TASK PERS wobjdata obROB11:=[FALSE,FALSE,"ROB_1",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];

    !************************************************
    ! Declaration :     jointtarget
    !************************************************
    !
    CONST jointtarget jpSafePosWorSpa:=[[180,90,-30,0,0,0],[0,9E9,9E9,9E9,9E9,9E9]];

    !************************************************
    ! Declaration :     robtarget
    !************************************************
    !
    CONST robtarget pPreWorldPoint:=[[24053.83,100.34,800.30],[1.54257E-06,-0.991445,2.02762E-06,-0.130528],[0,0,-1,5],[24170.3,0,-3000,0,0,0]];
    CONST robtarget pWorldPoint:=[[19902.52,6118.49,1650.01],[0.652571,-0.272304,-0.652572,-0.272306],[0,0,-1,0],[21500,-4400,-3500,0,0,0]];
    CONST robtarget pPReMultMove:=[[19972.86,6047.41,1650.01],[0.652571,-0.272304,-0.652572,-0.272306],[0,-1,0,0],[21500,-4400,-3500,0,0,0]];
    CONST robtarget pMultMove:=[[0.31,-0.34,206.82],[0.708952,0.705257,-1.34168E-06,8.49215E-07],[0,-1,0,0],[21500,-4400,-3500,0,0,0]];

ENDMODULE