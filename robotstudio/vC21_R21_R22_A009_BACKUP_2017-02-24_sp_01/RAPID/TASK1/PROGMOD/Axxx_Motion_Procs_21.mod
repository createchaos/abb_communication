MODULE Axxx_Motion_Procs_21
    
    PROC mas_pick()

        TPWrite "=> Start moving to pos from buffer mas. buflen: "+ValToStr(BUFFER_LENGTH_R3);

        !joint_reach:=calc_joint_reach(current_pos); !calc reachability

        SingArea\Wrist;
        ConfJ\Off;
        ConfL\Off;
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        joint_reach:=TRUE;
        !Be careful to check, if this does not cause problems!!
        !open gripper
        Stop;
        MoveL RelTool(current_pos, 0, 0, -100), current_speed_data_r3,fine,current_tool_r3,\WObj:=current_wobj_r3;
        MoveL current_pos,v20,fine,current_tool_r3,\WObj:=current_wobj_r3;
        !close gripper
        Stop;
        MoveL RelTool(current_pos, 0, 0, -100), v20,fine,current_tool_r3,\WObj:=current_wobj_r3;
        send_command_executed;
            
        TPWrite "PICK DONE";

    ENDPROC
    
    PROC mas_place()

        TPWrite "=> Start moving to pos from buffer mas. buflen: "+ValToStr(BUFFER_LENGTH_R3);

        !joint_reach:=calc_joint_reach(current_pos); !calc reachability

        SingArea\Wrist;
        ConfJ\Off;
        ConfL\Off;
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        joint_reach:=TRUE;
        !Be careful to check, if this does not cause problems!!
        
        MoveL RelTool(current_pos, 0, 0, -100), current_speed_data_r3,fine,current_tool_r3,\WObj:=current_wobj_r3;
        MoveL current_pos,v20,fine,current_tool_r3,\WObj:=current_wobj_r3;
        !open gripper
        Stop;
        MoveL RelTool(current_pos, 0, 0, -100), v20,fine,current_tool_r3,\WObj:=current_wobj_r3;
        send_command_executed;
            
        TPWrite "PICK DONE";

    ENDPROC
    
ENDMODULE