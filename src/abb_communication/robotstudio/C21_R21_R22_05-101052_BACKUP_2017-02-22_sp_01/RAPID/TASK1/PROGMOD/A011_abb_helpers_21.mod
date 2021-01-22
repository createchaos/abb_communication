MODULE A011_abb_helpers_21
    
    FUNC pose CPoseT(\string TaskName, PERS tooldata Tool, PERS wobjdata WObj)
        VAR pose pose_var;
        VAR robtarget rob_target;
        
        IF Present(TaskName) THEN
            rob_target := CRobT(\TaskName := TaskName, \Tool := Tool, \WObj := WObj);
        ELSE
            rob_target := CRobT(\Tool := Tool, \WObj := WObj);
        ENDIF
        
        pose_var.trans := rob_target.trans;
        pose_var.rot := rob_target.rot;
        
        RETURN pose_var;
    ENDFUNC
    
ENDMODULE