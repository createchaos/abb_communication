MODULE A009_Motion_Procs_22

    VAR TCPIP_MSG_COMMAND act_tcpip_message_command;
    !STRUC command

    CONST speeddata fast:=v1000;
    CONST speeddata mid:=v100;
    CONST speeddata slow:=v20;
    CONST speeddata superslow:=[0.5,1,0.5,1];

    CONST num acc_max:=10;
    CONST num dec_max:=10;

    VAR speeddata current_speed_data_r4:=slow;
    VAR zonedata current_zone_data_r4:=z10;
    PERS wobjdata current_wobj_r4;
    PERS tooldata current_tool_r4;

    !for robtarget moves
    VAR robtarget current_pos;
    VAR bool joint_reach;

    !for joint moves
    VAR jointtarget current_jointpos;
    VAR errnum errnum_jointpos;

    !general
    VAR robtarget init_pos;

    !reset with variable
    VAR intnum rtm_interrupt;


    PROC init()

        !initialize robot
        TPWrite "initialization";
    
        current_tool_r4:=tool0;
        current_wobj_r4:=wobj_base_r4;
        
        current_pos:=CRobT(\Tool:=current_tool_r4\WObj:=current_wobj_r4);
        init_pos:=CRobT(\Tool:=current_tool_r4\WObj:=current_wobj_r4);
        current_jointpos:=CJointT();

        joint_reach:=TRUE;

        cmd_exec_counter:=0;
        !waypoint_counter_exec:=0; !waypoint counter of executed commands


        ! limit path acceleration for every move command but the move joints command sent with duration
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        SingArea\Wrist;

        !reset (connected to persistent)
        reset_to_main:=FALSE;
        CONNECT rtm_interrupt WITH reset_after_connection_stop;
        IPers reset_to_main,rtm_interrupt;



    ENDPROC

    !reset trap (connected to persistent)
    TRAP reset_after_connection_stop

        IF reset_to_main=TRUE THEN

            TPWrite "INTERRUPT IN MOTION, PP is moved to main";

            Idelete rtm_interrupt;
            reset_to_main:=FALSE;

            ExitCycle;

        ENDIF

    ENDTRAP




    !reset restart event (connected to persistent and restart)
    PROC reset_after_connection_stop_evt()

        IF reset_to_main=TRUE THEN

            TPWrite "RESTART EVENT: RESET IN MOTION, PP is moved to main";

            Idelete rtm_interrupt;
            reset_to_main:=FALSE;

            ExitCycle;

        ENDIF

    ENDPROC

    PROC execute_from_buffer()

        act_tcpip_message_command:=tcpip_message_command_buffer_r4{READ_PTR_R4};
        TPWrite "EXECUTE FROM BUFFER"+ValToStr(act_tcpip_message_command.cmd_type);

        set_tool;
        set_zone_data;
        set_wobj;

        TEST act_tcpip_message_command.cmd_type

        CASE CMD_GO_TO_JOINTTARGET_ABS:
            read_jointtarget_values_abs;
            move_from_buffer_joint;
        CASE CMD_GO_TO_JOINTTARGET_REL:
            read_jointtarget_values_rel;
            move_from_buffer_joint;
        CASE CMD_GO_TO_TASKTARGET:
            set_speed;
            read_robtarget_values;
            move_from_buffer_robtarget;
        CASE CMD_GO_TO_TASKTARGET_JOINTS:
            set_speed;
            read_robtarget_values;
            move_from_buffer_robtarget_joint;
        CASE CMD_OPEN_GRIPPER:
            open_gripper;
        CASE CMD_CLOSE_GRIPPER:
            close_gripper;
        CASE CMD_PICK_ROD:
            set_speed;
            read_robtarget_values;
            pick_rod_from_feed;
        CASE CMD_MILL_ROD_START:
            set_speed;
            read_robtarget_values;
            mill_rod_start;
        CASE CMD_MILL_ROD_END:
            set_speed;
            read_robtarget_values;
            mill_rod_end;
        CASE CMD_REGRIP_PLACE:
            set_speed;
            read_robtarget_values;
            regrip_place;
        CASE CMD_REGRIP_PICK:
            set_speed;
            read_robtarget_values;
            regrip_pick;
        CASE CMD_SAFE_POS:
            set_speed;
            read_jointtarget_values_abs;
            move_to_safe_pos;
        CASE CMD_OPEN_CLAMP:
            open_clamp;
        CASE CMD_CLOSE_CLAMP:
            close_clamp;
        CASE CMD_MAS_PICK:
            set_speed;
            read_robtarget_values;
            mas_pick;
        CASE CMD_MAS_PLACE:
            set_speed;
            read_robtarget_values;
            mas_place;
        DEFAULT:
            TPWRITE "Wrong Procedure Number";
        ENDTEST

        WaitTestAndSet msg_lock;
        READ_PTR_R4:=(READ_PTR_R4 MOD MAX_BUFFER_SIZE)+1;
        BUFFER_LENGTH_R4:=BUFFER_LENGTH_R4-1;
        msg_lock:=FALSE;

    ENDPROC


    LOCAL PROC set_tool()
        !assign toolnumber
        TEST act_tcpip_message_command.tool
        CASE 0:
            current_tool_r4:=tool0;
        CASE 1:
            current_tool_r4:=tool0;
        CASE 2:
            current_tool_r4:=tool0;
        DEFAULT:
            TPWrite "WRONG TOOLNUMBER";
            current_tool_r4:=tool0;
        ENDTEST
    ENDPROC

    LOCAL PROC set_speed()
        !assign speedvalue
        TEST act_tcpip_message_command.velocity
        CASE 0:
            current_speed_data_r4:=slow;
        CASE 1:
            current_speed_data_r4:=mid;
        CASE 2:
            current_speed_data_r4:=fast;
        CASE 3:
            current_speed_data_r4:=superslow;
        DEFAULT:
            TPWrite "WRONG SPEEDNUMBER";
            current_speed_data_r4:=slow;
        ENDTEST
    ENDPROC

    LOCAL PROC set_zone_data()
        !assign speedvalue
        TEST act_tcpip_message_command.zone
        CASE 0:
            current_zone_data_r4:=fine;
        DEFAULT:
            current_zone_data_r4:=[FALSE,act_tcpip_message_command.zone,1.5*act_tcpip_message_command.zone,1.5*act_tcpip_message_command.zone,0.15*act_tcpip_message_command.zone,1.5*act_tcpip_message_command.zone,0.15*act_tcpip_message_command.zone];
        ENDTEST
    ENDPROC

    LOCAL PROC set_wobj()
        !assign workobject
        TEST act_tcpip_message_command.wobj
        CASE 0:
            current_wobj_r4:=wobj0;
        CASE 1:
            current_wobj_r4:=wobj0;
        CASE 2:
            current_wobj_r4:=wobj_base_r4;
        DEFAULT:
            current_wobj_r4:=wobj0;
        ENDTEST
    ENDPROC

    LOCAL PROC read_robtarget_values()
        !read cartesian coordinates
        current_pos.trans.x:=act_tcpip_message_command.val1;
        current_pos.trans.y:=act_tcpip_message_command.val2;
        current_pos.trans.z:=act_tcpip_message_command.val3;
        current_pos.rot.q1:=act_tcpip_message_command.val4;
        current_pos.rot.q2:=act_tcpip_message_command.val5;
        current_pos.rot.q3:=act_tcpip_message_command.val6;
        current_pos.rot.q4:=act_tcpip_message_command.val7;
        !added - stefana
        current_pos.extax.eax_a:=act_tcpip_message_command.val8;
        current_pos.extax.eax_b:=act_tcpip_message_command.val9;
        current_pos.extax.eax_c:=act_tcpip_message_command.val10;

    ENDPROC

    LOCAL PROC read_jointtarget_values_rel()
        !read jointtarget and add to current jointposition
        current_jointpos:=CJointT();
        current_jointpos.robax.rax_1:=current_jointpos.robax.rax_1+act_tcpip_message_command.val1;
        current_jointpos.robax.rax_2:=current_jointpos.robax.rax_2+act_tcpip_message_command.val2;
        current_jointpos.robax.rax_3:=current_jointpos.robax.rax_3+act_tcpip_message_command.val3;
        current_jointpos.robax.rax_4:=current_jointpos.robax.rax_4+act_tcpip_message_command.val4;
        current_jointpos.robax.rax_5:=current_jointpos.robax.rax_5+act_tcpip_message_command.val5;
        current_jointpos.robax.rax_6:=current_jointpos.robax.rax_6+act_tcpip_message_command.val6;
        !added - stefana
        current_jointpos.extax.eax_a:=current_jointpos.extax.eax_a+act_tcpip_message_command.val7;
        current_jointpos.extax.eax_b:=current_jointpos.extax.eax_b+act_tcpip_message_command.val8;
        current_jointpos.extax.eax_c:=current_jointpos.extax.eax_c+act_tcpip_message_command.val9;
    ENDPROC

    LOCAL PROC read_jointtarget_values_abs()
        current_jointpos.robax.rax_1:=act_tcpip_message_command.val1;
        current_jointpos.robax.rax_2:=act_tcpip_message_command.val2;
        current_jointpos.robax.rax_3:=act_tcpip_message_command.val3;
        current_jointpos.robax.rax_4:=act_tcpip_message_command.val4;
        current_jointpos.robax.rax_5:=act_tcpip_message_command.val5;
        current_jointpos.robax.rax_6:=act_tcpip_message_command.val6;
        !added - stefana
        current_jointpos.extax.eax_a:=act_tcpip_message_command.val7;
        current_jointpos.extax.eax_b:=act_tcpip_message_command.val8;
        current_jointpos.extax.eax_c:=act_tcpip_message_command.val9;
    ENDPROC


    PROC move_from_buffer_joint()

        !TPWrite "=> Start moving to pos from buffer. buflen: " + ValToStr(BUFFER_LENGTH);

        TEST act_tcpip_message_command.duration
        CASE 0:
            set_speed;
            PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

            IF BUFFER_LENGTH_R4>1 THEN
                MoveAbsJ current_jointpos,current_speed_data_r4,current_zone_data_r4,tool0;
                !!!no send command executed ! to fix!
            ELSE
                MoveAbsJ current_jointpos,current_speed_data_r4,fine,tool0;
                send_command_executed;
            ENDIF

        DEFAULT:
            IF BUFFER_LENGTH_R4>1 THEN
                PathAccLim FALSE,FALSE;
                MoveAbsJ current_jointpos,current_speed_data_r4\T:=act_tcpip_message_command.duration,current_zone_data_r4,tool0;
                PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;
                !!!no send command executed ! to fix!
            ELSE
                MoveAbsJ current_jointpos,current_speed_data_r4\T:=act_tcpip_message_command.duration,current_zone_data_r4,tool0;
                send_command_executed;
            ENDIF
        ENDTEST


    ENDPROC

    PROC move_from_buffer_robtarget_joint()

        TPWrite "=> Start moving to pos from buffer. buflen: "+ValToStr(BUFFER_LENGTH_R4);

        !joint_reach:=calc_joint_reach(current_pos); !calc reachability

        SingArea\Wrist;
        ConfJ\Off;
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        joint_reach:=TRUE;
        !Be careful to check, if this does not cause problems!!

        IF joint_reach=TRUE THEN
            IF BUFFER_LENGTH_R4>1 THEN
                MoveJSync current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4,"send_command_executed";
                TPWrite "point inbetween";
            ELSE
                MoveJ current_pos,current_speed_data_r4,fine,current_tool_r4,\WObj:=current_wobj_r4;
                TPWrite "last point";
                send_command_executed;
            ENDIF
            TPWrite "FINAL PLANE REACHED";
        ELSE
            send_command_executed;
        ENDIF

    ENDPROC

    PROC move_from_buffer_robtarget()

        TPWrite "=> Start moving to pos from buffer. buflen: "+ValToStr(BUFFER_LENGTH_R4);

        !joint_reach:=calc_joint_reach(current_pos); !calc reachability

        SingArea\Wrist;
        ConfJ\Off;
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        joint_reach:=TRUE;
        !Be careful to check, if this does not cause problems!!

        IF joint_reach=TRUE THEN
            IF BUFFER_LENGTH_R4>1 THEN
                MoveLSync current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4,"send_command_executed";
                TPWrite "point inbetween";
            ELSE
                MoveL current_pos,current_speed_data_r4,fine,current_tool_r4,\WObj:=current_wobj_r4;
                TPWrite "last point";
                send_command_executed;
            ENDIF
            TPWrite "FINAL PLANE REACHED";
        ELSE
            send_command_executed;
        ENDIF

    ENDPROC

    PROC pick_rod_from_feed()

        VAR robtarget cpose1;
        VAR robtarget cpose2;

        !set_speed;
        SingArea\Wrist;
        ConfL\Off;
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        open_gripper;
        cpose1:=current_pos;
        MoveL RelTool(current_pos,0,0,-200),current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        MoveL current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        WaitTime(2);
        close_gripper;
        cpose1.trans.z:=cpose1.trans.z+500;
        WaitTime 0.5;
        MoveL cpose1,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        MoveL RelTool(cpose1,0,0,0,\Rz:=60),current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;


        send_command_executed;

    ENDPROC

    PROC mill_rod_start()


        VAR robtarget cpose1;
        TPWrite "Pose start mill "+ValToStr(current_pos.trans.z);
        cpose1:=current_pos;

        ConfL\Off;
        MoveL current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;

        WaitTime(2);

        send_command_executed;

    ENDPROC

    PROC mill_rod_end()

        VAR robtarget cpose1;
        VAR speeddata speed1:=[0.7,1,0.7,1];
        VAR robtarget cpose2;

        TPWrite "Pose end mill "+ValToStr(current_pos.trans.z);

        ConfL\Off;
        MoveL current_pos,speed1,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;

        MoveL RelTool(current_pos,0,-10,0),current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;

        cpose1:=current_pos;
        cpose1.trans.z:=current_pos.trans.z+600;

        MoveL cpose1,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        cpose2:=cpose1;
        cpose2.trans.y:=cpose2.trans.y+500;
        MoveL cpose2,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;

        send_command_executed;

    ENDPROC


    PROC open_gripper()
        
        WaitRob\InPos;
        rGr4Open;
        WaitRob\InPos;
        !SetDO DO10_1, 1;
        !WaitTime 0.5;
        send_command_executed;
        
    ENDPROC

    PROC close_gripper()
        
        WaitRob\InPos;
        rGr4Close;
        WaitRob\InPos;
        !SetDO DO10_1, 0;
        !WaitTime 0.5;
        send_command_executed;
        
    ENDPROC

    PROC open_clamp()

        WaitRob\InPos;
        rClamp4Open;
        WaitRob\InPos;

    ENDPROC

    PROC close_clamp()

        WaitRob\InPos;
        rClamp4Close;
        WaitRob\InPos;

    ENDPROC

    PROC regrip_place()

        VAR robtarget cpose1;

        !WaitRob \InPos;
        !rClamp1Open;
        !WaitRob \InPos;

        ConfL\Off;
        SingArea \Wrist;

        cpose1:=current_pos;
        cpose1.trans.z:=cpose1.trans.z+150;

        MoveL RelTool(cpose1,0,-5,0),current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        cpose1.trans.z:=cpose1.trans.z-150;
        MoveL cpose1,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;

        WaitRob\InPos;
        rClamp4Close;
        WaitRob\InPos;
        open_gripper;
        WaitRob\InPos;

        MoveL RelTool(cpose1,0,0,-300),current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        send_command_executed;

    ENDPROC

    PROC regrip_pick()

        VAR robtarget cpose1;

        ConfL\Off;
        SingArea \Wrist;

        MoveL RelTool(current_pos,0,0,-300),current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        MoveL current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;

        WaitRob\InPos;
        close_gripper;
        WaitRob\InPos;
        rClamp4Open;
        WaitRob\InPos;

        cpose1:=current_pos;
        cpose1.trans.z:=cpose1.trans.z+400;

        MoveL cpose1,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=current_wobj_r4;
        send_command_executed;

    ENDPROC

    PROC move_to_safe_pos()

        ConfJ \Off;
        PathAccLim TRUE\AccMax:=acc_max,TRUE\DecelMax:=dec_max;

        IF BUFFER_LENGTH_R4>1 THEN
            MoveAbsJ current_jointpos,current_speed_data_r4,current_zone_data_r4,tool0;
        ELSE
            MoveAbsJ current_jointpos,current_speed_data_r4,fine,tool0;
        ENDIF

    ENDPROC

    PROC send_command_executed()
        !after the movement is finished,send back the execute command
        send_msg_cmd_exec:=TRUE;
        TPWrite "send command executed";
    ENDPROC


    FUNC bool calc_joint_reach(VAR robtarget current_p1)
        !calculate if the next point is reachable
        VAR bool j_reach:=TRUE;
        current_jointpos:=CalcJointT(current_p1,current_tool_r4\WObj:=current_wobj_r4);
        RETURN j_reach;

    ERROR
        IF ERRNO=ERR_ROBLIMIT THEN
            SkipWarn;
            TPWrite "Joint current_p1 can not be reached.";
            j_reach:=FALSE;
            RETURN j_reach;
        ENDIF
    ENDFUNC


    PROC go_to_init_pos()
        TPWrite "Move to init pos.";
        MoveL init_pos,mid,fine,current_tool_r4,\WObj:=current_wobj_r4;
    ENDPROC


    PROC pick_up_brick_from_pose()
        VAR bool dist;
        VAR bool vacuum;

        VAR robtarget hit_dist;
        VAR robtarget hit_vac;

        !drive to brickpose + 50 in z
        current_pos.trans.z:=current_pos.trans.z+100;
        MoveL current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=wobj0;

        !drive down until distance sensor kicks in
        current_pos.trans.z:=current_pos.trans.z-100;
        !SearchL \PStop,DI_DISTANCE,hit_dist,current_pos,v10,current_tool;

        hit_dist.trans.z:=hit_dist.trans.z-18;

        !turn on vakuum pump
        !SetDO DO_VACPUMP,1;
        WaitTime 2;
        !SetDO DO_VALVE2,1;

        !drive down until vacuum sensor kicks in
        !SearchL \PStop,DI_VACUUM,hit_vac,hit_dist,v10,current_tool;

        current_pos.trans.z:=current_pos.trans.z+200;

        IF BUFFER_LENGTH_R4>1 THEN
            MoveLSync current_pos,current_speed_data_r4,current_zone_data_r4,current_tool_r4,\WObj:=wobj0,"send_command_executed";
        ELSE
            MoveL current_pos,current_speed_data_r4,fine,current_tool_r4,\WObj:=wobj0;
            send_command_executed;
        ENDIF
    ENDPROC


ENDMODULE