
MODULE A009_Helper_22
    PROC rTeachTool4()
        !wobj
        MoveAbsJ [[-32.8842,-73.6868,-15.1938,198.029,66.3199,-183.305],[18247.9,-4448.72,-2495.07,0,0,0]]\NoEOffs,v1000,fine,tool0;
    ENDPROC

    !************************************************
    ! Function    :     Open Gripper 1
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.30
    ! **************** ETH Z�rich *******************
    !
    PROC rGr4Open()
        !SetDO doU1Gr1Close,0;
        !SetDO doU1Gr1Open,1;
        WaitTime 1;
    ENDPROC

    !************************************************
    ! Function    :     Close Gripper 1
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.30
    ! **************** ETH Z�rich *******************
    !
    PROC rGr4Close()
        !SetDO doU1Gr1Open,0;
        !SetDO doU1Gr1Close,1;
        WaitTime 1;
    ENDPROC

    !************************************************
    ! Function    :     Open Clamp 1 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.30
    ! **************** ETH Z�rich *******************
    !
    PROC rClamp4Open()
        !SetDO doU3Clamp1Close,0;
        !SetDO doU3Clamp1Open,1;
        WaitTime 1;
    ENDPROC

    !************************************************
    ! Function    :     Close Clamp 1 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.30
    ! **************** ETH Z�rich *******************
    !
    PROC rClamp4Close()
        !SetDO doU3Clamp1Open,0;
        !SetDO doU3Clamp1Close,1;
        WaitTime 1;
    ENDPROC

ENDMODULE