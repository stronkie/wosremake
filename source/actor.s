;======================================================================
;  actor.s - the people (and rabbits): walking with path finding over
;            the room's walk mask, animations, talking
;======================================================================

act_ptr                             ; d0 = actor -> a0
        move.w  d0,a0
        move.l  d0,-(sp)
        move.w  a0,d0
        mulu    #A_SIZE,d0
        lea     actors,a0
        add.l   d0,a0
        move.l  (sp)+,d0
        rts

;----------------------------------------------------------------------
;  the walk mask: 80 x 42 cells of 4 x 4 pixels, a bit each
;----------------------------------------------------------------------
cell_free                           ; d0 = cx, d1 = cy -> Z=0 free
        movem.l d0-d2/a0,-(sp)
        cmp.w   #WALK_W,d0
        bhs     .no
        cmp.w   #WALK_H,d1
        bhs     .no
        move.l  walk_mask,d2
        beq     .no
        move.l  d2,a0
        mulu    #WALK_W/8,d1
        add.w   d1,a0
        move.w  d0,d1
        lsr.w   #3,d1
        add.w   d1,a0
        not.b   d0
        and.w   #7,d0
        btst    d0,(a0)
        movem.l (sp)+,d0-d2/a0
        rts
.no     movem.l (sp)+,d0-d2/a0
        moveq   #0,d2               ; (Z=1)
        rts

nearest_free                        ; d0 = cx, d1 = cy -> the nearest free cell
        bsr     cell_free
        bne     .x
        moveq   #1,d4               ; rings of growing size
.ring   move.w  d4,d5
        neg.w   d5                  ; dy -r..r
.dy     move.w  d4,d6
        neg.w   d6
.dx     move.w  d5,d2
        bpl     .a1
        neg.w   d2
.a1     move.w  d6,d3
        bpl     .a2
        neg.w   d3
.a2     cmp.w   d2,d3
        bge     .m
        move.w  d2,d3
.m      cmp.w   d4,d3               ; only the ring itself
        bne     .nx
        movem.w d0-d1,-(sp)
        add.w   d6,d0
        add.w   d5,d1
        bsr     cell_free
        beq     .no
        addq.l  #4,sp
        rts
.no     movem.w (sp)+,d0-d1
.nx     addq.w  #1,d6
        cmp.w   d4,d6
        ble     .dx
        addq.w  #1,d5
        cmp.w   d4,d5
        ble     .dy
        addq.w  #1,d4
        cmp.w   #WALK_W,d4
        blo     .ring
.x      rts

;----------------------------------------------------------------------
;  path finding: breadth first over the cells, then the corners only
;----------------------------------------------------------------------
find_path                           ; a2 = actor, d0/d1 = target x/y (pixels) -> path in the actor
        movem.l d2-d7/a3-a6,-(sp)
        clr.w   A_NPATH(a2)
        clr.w   A_PATHI(a2)
        lsr.w   #2,d0               ; target cell
        lsr.w   #2,d1
        bsr     nearest_free
        move.w  d0,pf_tx
        move.w  d1,pf_ty
        move.w  A_X(a2),d0          ; start cell
        move.w  A_Y(a2),d1
        lsr.w   #2,d0
        lsr.w   #2,d1
        bsr     nearest_free
        move.w  d0,pf_sx
        move.w  d1,pf_sy
        lea     pf_from,a3          ; -1: not reached
        move.w  #WALK_W*WALK_H-1,d2
.cl     move.w  #-1,(a3)+
        dbf     d2,.cl
        lea     pf_from,a3
        lea     pf_queue,a4
        move.w  pf_sy,d2
        mulu    #WALK_W,d2
        add.w   pf_sx,d2
        add.w   d2,d2
        move.w  d2,d3
        lsr.w   #1,d3
        move.w  d3,(a3,d2.w)        ; the start comes from itself
        move.w  d3,(a4)
        moveq   #0,d6               ; queue read
        moveq   #1,d7               ; queue write
        move.w  pf_ty,d5
        mulu    #WALK_W,d5
        add.w   pf_tx,d5            ; target cell number
.bfs    cmp.w   d7,d6
        bhs     .done
        move.w  d6,d2
        add.w   d2,d2
        move.w  (a4,d2.w),d4        ; cell
        addq.w  #1,d6
        cmp.w   d5,d4
        beq     .done
        moveq   #0,d0
        move.w  d4,d0
        divu    #WALK_W,d0
        move.w  d0,d1               ; cy
        swap    d0                  ; cx
        lea     pf_dirs,a5
        moveq   #7,d3
.nb     movem.w d0-d1,-(sp)
        add.w   (a5)+,d0
        add.w   (a5)+,d1
        bsr     cell_free
        beq     .skip
        move.w  d1,d2
        mulu    #WALK_W,d2
        add.w   d0,d2
        add.w   d2,d2
        tst.w   (a3,d2.w)
        bpl     .skip
        move.w  d4,(a3,d2.w)
        lsr.w   #1,d2
        move.w  d7,d0
        add.w   d0,d0
        move.w  d2,(a4,d0.w)
        addq.w  #1,d7
.skip   movem.w (sp)+,d0-d1
        dbf     d3,.nb
        bra     .bfs
.done   move.w  d5,d2               ; reached the target? (else: the nearest is the start)
        add.w   d2,d2
        tst.w   (a3,d2.w)
        bpl     .back
        move.w  pf_sy,d5
        mulu    #WALK_W,d5
        add.w   pf_sx,d5
.back   lea     pf_queue,a4         ; the cells back to the start (reversed)
        moveq   #0,d7
        move.w  d5,d4
.bk     move.w  d4,(a4)+
        addq.w  #1,d7
        move.w  d4,d2
        add.w   d2,d2
        move.w  (a3,d2.w),d2
        cmp.w   d2,d4
        beq     .bkd
        move.w  d2,d4
        cmp.w   #WALK_W*WALK_H,d7
        blo     .bk
.bkd    ; pf_queue: target ... start (d7 cells). Keep only the turning points:
        ; walk from the start, and from each kept point take the farthest
        ; cell that can be seen in a straight line.
        lea     pf_queue,a4
        move.w  d7,d6
        subq.w  #1,d6               ; index of the start
        lea     A_PATH(a2),a5
        moveq   #0,d5               ; path points
.sp     tst.w   d6
        beq     .last
        moveq   #0,d4               ; try from the target end towards here
.try    cmp.w   d6,d4
        bhs     .step
        move.w  d6,d2
        add.w   d2,d2
        move.w  (a4,d2.w),d0
        move.w  d4,d2
        add.w   d2,d2
        move.w  (a4,d2.w),d1
        bsr     line_free           ; cells d0 -> d1 all free?
        bne     .take
        addq.w  #1,d4
        bra     .try
.step   move.w  d6,d4
        subq.w  #1,d4
.take   move.w  d4,d6
        move.w  d6,d2
        add.w   d2,d2
        move.w  (a4,d2.w),d0
        bsr     .point
        bra     .sp
.last   ; the exact target pixel when its cell is the target cell
        move.w  pf_tx,d0
        lsl.w   #2,d0
        addq.w  #2,d0
        move.w  pf_ty,d1
        lsl.w   #2,d1
        addq.w  #2,d1
        move.w  pf_x,d2
        lsr.w   #2,d2
        cmp.w   pf_tx,d2
        bne     .lx
        move.w  pf_y,d2
        lsr.w   #2,d2
        cmp.w   pf_ty,d2
        bne     .lx
        move.w  pf_x,d0
        move.w  pf_y,d1
.lx     tst.w   d5
        beq     .add
        move.w  -4(a5),d2           ; replace the last point by the exact one
        lsr.w   #2,d2
        cmp.w   pf_tx,d2
        bne     .add
        move.w  -2(a5),d2
        lsr.w   #2,d2
        cmp.w   pf_ty,d2
        bne     .add
        subq.w  #1,d5
        subq.l  #4,a5
.add    cmp.w   #MAXPATH,d5
        bhs     .full
        move.w  d0,(a5)+
        move.w  d1,(a5)+
        addq.w  #1,d5
.full   move.w  d5,A_NPATH(a2)
        clr.w   A_PATHI(a2)
        movem.l (sp)+,d2-d7/a3-a6
        rts
.point  cmp.w   #MAXPATH-1,d5       ; d0 = cell -> a path point (its middle)
        bhs     .px
        moveq   #0,d1
        move.w  d0,d1
        divu    #WALK_W,d1
        move.w  d1,d2
        swap    d1
        lsl.w   #2,d1
        addq.w  #2,d1
        lsl.w   #2,d2
        addq.w  #2,d2
        move.w  d1,(a5)+
        move.w  d2,(a5)+
        addq.w  #1,d5
.px     rts

line_free                           ; d0, d1 = cell numbers -> Z=0 if the straight line is free
        movem.l d0-d7,-(sp)
        moveq   #0,d2
        move.w  d0,d2
        divu    #WALK_W,d2
        move.w  d2,d3               ; y0
        swap    d2                  ; x0
        moveq   #0,d4
        move.w  d1,d4
        divu    #WALK_W,d4
        move.w  d4,d5               ; y1
        swap    d4                  ; x1
        sub.w   d2,d4               ; dx
        sub.w   d3,d5               ; dy
        move.w  d4,d6
        bpl     .a
        neg.w   d6
.a      move.w  d5,d7
        bpl     .b
        neg.w   d7
.b      cmp.w   d6,d7
        ble     .c
        move.w  d7,d6
.c      moveq   #0,d7               ; step i = 1..n: x0 + dx*i/n
.lp     addq.w  #1,d7
        cmp.w   d6,d7
        bgt     .yes
        move.w  d4,d0
        muls    d7,d0
        divs    d6,d0
        add.w   d2,d0
        move.w  d5,d1
        muls    d7,d1
        divs    d6,d1
        add.w   d3,d1
        bsr     cell_free
        bne     .lp
        moveq   #0,d0               ; Z=1: blocked
        movem.l (sp)+,d0-d7
        rts
.yes    moveq   #1,d0               ; Z=0: free
        movem.l (sp)+,d0-d7
        rts

;----------------------------------------------------------------------
;  moving the actors, one tick
;----------------------------------------------------------------------
actors_tick
        moveq   #0,d7
.lp     move.w  d7,d0
        bsr     act_ptr
        move.l  a0,a2
        tst.w   A_ROOM(a2)
        beq     .nx
        tst.l   A_COST(a2)
        beq     .nx
        bsr     actor_move
        bsr     actor_animate
.nx     addq.w  #1,d7
        cmp.w   #MAXACT,d7
        blo     .lp
        rts

walk_actor                          ; d0 = actor, d1/d2 = x/y
        bsr     act_ptr
        move.l  a0,a2
        move.w  d1,pf_x
        move.w  d2,pf_y
        move.w  d1,d0
        move.w  d2,d1
        move.w  A_ROOM(a2),d2
        cmp.w   cur_room,d2
        bne     .jump               ; not in this room: just put it there
        tst.l   walk_mask
        beq     .jump
        bsr     find_path
        move.w  A_NPATH(a2),d0
        beq     .stop
        move.w  #1,A_MODE(a2)
        rts
.jump   move.w  pf_x,A_X(a2)
        move.w  pf_y,A_Y(a2)
.stop   clr.w   A_NPATH(a2)
        clr.w   A_MODE(a2)
        rts

actor_move                          ; a2 = actor
        cmp.w   #1,A_MODE(a2)
        bne     .x
        move.w  A_PATHI(a2),d0
        cmp.w   A_NPATH(a2),d0
        bhs     .arrive
        add.w   d0,d0
        add.w   d0,d0
        move.w  A_PATH(a2,d0.w),d1  ; waypoint
        move.w  A_PATH+2(a2,d0.w),d2
        sub.w   A_X(a2),d1          ; dx
        sub.w   A_Y(a2),d2          ; dy
        move.w  d1,d3
        bpl     .a
        neg.w   d3
.a      move.w  d2,d4
        bpl     .b
        neg.w   d4
.b      cmp.w   d4,d3               ; face the way of the bigger move
        blt     .vert
        moveq   #0,d5
        tst.w   d1
        bpl     .dir
        moveq   #1,d5
        bra     .dir
.vert   moveq   #2,d5
        tst.w   d2
        bpl     .dir
        moveq   #3,d5
.dir    move.w  d5,A_DIR(a2)
        ; step: up to 3 pixels sideways, 2 up/down, along the line
        moveq   #3,d5
        moveq   #2,d6
        cmp.w   d5,d3
        bgt     .sx
        move.w  d3,d5
.sx     cmp.w   d6,d4
        bgt     .sy
        move.w  d4,d6
.sy     tst.w   d3                  ; keep the direction: scale the smaller one
        beq     .mv
        tst.w   d4
        beq     .mv
        cmp.w   d3,d4
        bgt     .ybig
        move.w  d4,d6               ; dy*sx/|dx|
        mulu    d5,d6
        divu    d3,d6
        tst.w   d6
        bne     .mv
        moveq   #1,d6
        bra     .mv
.ybig   move.w  d3,d5
        mulu    d6,d5
        divu    d4,d5
        tst.w   d5
        bne     .mv
        moveq   #1,d5
.mv     tst.w   d1
        bpl     .px
        neg.w   d5
.px     tst.w   d2
        bpl     .py
        neg.w   d6
.py     add.w   d5,A_X(a2)
        add.w   d6,A_Y(a2)
        cmp.w   d5,d1
        bne     .x
        cmp.w   d6,d2
        bne     .x
        addq.w  #1,A_PATHI(a2)      ; at the waypoint
.x      rts
.arrive clr.w   A_MODE(a2)
        clr.w   A_NPATH(a2)
        move.w  #1,A_CNT(a2)
        rts

actor_animate                       ; a2 = actor
        move.l  A_COST(a2),a3
        add.l   dat,a3
        move.w  A_DIR(a2),d1
        and.w   #3,d1               ; (always one of the four)
        add.w   d1,d1
        move.w  A_MODE(a2),d0
        cmp.w   #1,d0
        beq     .walk
        cmp.w   #3,d0
        beq     .spec
        tst.w   A_TALKING(a2)
        bne     .talk
        move.w  C_STAND(a3,d1.w),A_FRAME(a2)
        rts
.talk   subq.w  #1,A_CNT(a2)
        bgt     .x
        move.w  #3,A_CNT(a2)
        move.w  A_POS(a2),d0        ; (left over from walking: only 0 or 1 here)
        eor.w   #1,d0
        and.w   #1,d0
        move.w  d0,A_POS(a2)
        add.w   d1,d1               ; dir*4
        add.w   d0,d0
        add.w   d0,d1
        move.w  C_TALK(a3,d1.w),A_FRAME(a2)
.x      rts
.walk   move.w  C_WALKN(a3),d2      ; frames per direction
        beq     .x
        move.w  A_POS(a2),d0
        addq.w  #1,d0
        cmp.w   d2,d0
        blo     .w1
        moveq   #0,d0
.w1     move.w  d0,A_POS(a2)
        lsl.w   #3,d1               ; dir*16 (8 words per direction)
        add.w   d0,d0
        add.w   d0,d1
        move.w  C_WALK(a3,d1.w),A_FRAME(a2)
        rts
.spec   move.l  A_SPEC(a2),a4       ; .w count, .w delay, .w frames...
        subq.w  #1,A_CNT(a2)
        bgt     .x
        move.w  2(a4),A_CNT(a2)
        move.w  A_POS(a2),d0
        cmp.w   (a4),d0
        blo     .sf
        subq.w  #1,A_LOOP(a2)       ; the end of the animation
        bgt     .again
        bmi     .again              ; (-1: forever)
        clr.w   A_MODE(a2)
        clr.w   A_POS(a2)
        rts
.again  moveq   #0,d0
.sf     add.w   d0,d0
        move.w  4(a4,d0.w),A_FRAME(a2)
        lsr.w   #1,d0
        addq.w  #1,d0
        move.w  d0,A_POS(a2)
        rts

start_special                       ; d0 = actor, d1 = special number, d2 = loops (-1 forever)
        bsr     act_ptr
        move.l  A_COST(a0),a1
        add.l   dat,a1
        move.l  C_SPEC(a1),a1
        add.l   dat,a1
        add.w   d1,d1
        add.w   d1,d1
        move.l  (a1,d1.w),a1
        add.l   dat,a1
        move.l  a1,A_SPEC(a0)
        move.w  d2,A_LOOP(a0)
        move.w  #3,A_MODE(a0)
        clr.w   A_POS(a0)
        move.w  #1,A_CNT(a0)
        clr.w   A_NPATH(a0)
        rts
