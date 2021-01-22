MODULE A011_unit_conversion_utils_21
    
    ! Degree to radian
    FUNC num DegToRad(num deg)
        RETURN deg * pi / 180;
    ENDFUNC
        
    ! Degree to radian robjoint
    FUNC robjoint DegToRadRJ(robjoint deg)
        VAR robjoint rad;
        rad.rax_1 := DegToRad(deg.rax_1);
        rad.rax_2 := DegToRad(deg.rax_2);
        rad.rax_3 := DegToRad(deg.rax_3);
        rad.rax_4 := DegToRad(deg.rax_4);
        rad.rax_5 := DegToRad(deg.rax_5);
        rad.rax_6 := DegToRad(deg.rax_6);
        RETURN rad;
    ENDFUNC

    ! Radian to degree
    FUNC num RadToDeg(num rad)
        RETURN rad * 180 / pi;
    ENDFUNC
        
    ! Radian to degree robjoint
    FUNC robjoint RadToDegRJ(robjoint rad)
        VAR robjoint deg;
        deg.rax_1 := RadToDeg(rad.rax_1);
        deg.rax_2 := RadToDeg(rad.rax_2);
        deg.rax_3 := RadToDeg(rad.rax_3);
        deg.rax_4 := RadToDeg(rad.rax_4);
        deg.rax_5 := RadToDeg(rad.rax_5);
        deg.rax_6 := RadToDeg(rad.rax_6);
        RETURN deg;
    ENDFUNC
    
    ! Meter to millimeter
    FUNC num MToMM(num m)
        RETURN m * 1000;
    ENDFUNC
    
    ! Meter to millimeter pos
    FUNC pos MToMMP(pos m)
        VAR pos mm;
        mm.x := MToMM(m.x);
        mm.y := MToMM(m.y);
        mm.z := MToMM(m.z);
        RETURN mm;
    ENDFUNC
    
    ! Meter to millimeter extjoint
    FUNC extjoint MToMMEJ(extjoint m)
        VAR extjoint mm;
        mm.eax_a := MToMM(m.eax_a);
        mm.eax_b := MToMM(m.eax_b);
        mm.eax_c := MToMM(m.eax_c);
        RETURN mm;
    ENDFUNC
    
    ! Millimeter to meter
    FUNC num MMToM(num mm)
        RETURN mm / 1000;
    ENDFUNC
    
    ! Millimeter to meter pos
    FUNC pos MMToMP(pos mm)
        VAR pos m;
        m.x := MMToM(mm.x);
        m.y := MMToM(mm.y);
        m.z := MMToM(mm.z);
        RETURN m;
    ENDFUNC
    
    ! Millimeter to meter extjoint
    FUNC extjoint MMToMEJ(extjoint mm)
        VAR extjoint m;
        m.eax_a := MMToM(mm.eax_a);
        m.eax_b := MMToM(mm.eax_b);
        m.eax_c := MMToM(mm.eax_c);
        RETURN m;
    ENDFUNC
    
    ! ABB units to SI units jointtarget
    FUNC jointtarget ABBToSIJT(jointtarget abb)
        VAR jointtarget si;
        si.robax := DegToRadRJ(abb.robax);
        si.extax := MMToMEJ(abb.extax);
        RETURN si;
    ENDFUNC
    
    ! SI units to ABB units jointtarget
    FUNC jointtarget  SIToABBJT(jointtarget si)
        VAR jointtarget abb;
        abb.robax := RadToDegRJ(si.robax);
        abb.extax := MToMMEJ(si.extax);
        RETURN abb;
    ENDFUNC
    
    ! ABB units to SI units robtarget
    FUNC robtarget ABBToSIRT(robtarget abb)
        VAR robtarget si;
        si.trans := MMToMP(abb.trans);
        si.rot := abb.rot;
        si.extax := MMToMEJ(abb.extax);
        RETURN si;
    ENDFUNC
    
    ! SI units to ABB units robtarget
    FUNC robtarget SIToABBRT(robtarget si)
        VAR robtarget abb;
        abb.trans := MToMMP(si.trans);
        abb.rot := si.rot;
        abb.extax := MToMMEJ(si.extax);
        RETURN abb;
    ENDFUNC
    
ENDMODULE