;======================================================================
;  sys.s - the operating system around the game: display take-over,
;          input handler (keys and mouse), vertical blank interrupt
;======================================================================

video_on
        move.l  gfxbase,a6
        tst.b   load_on             ; (the loading screen saved it)
        bne     .saved
        move.l  34(a6),old_view     ; gb_ActiView
.saved  clr.b   load_on
        sub.l   a1,a1
        jsr     _LVOLoadView(a6)
        jsr     _LVOWaitTOF(a6)
        jsr     _LVOWaitTOF(a6)
        jsr     _LVOOwnBlitter(a6)
        jsr     _LVOWaitBlit(a6)
        st      blit_owned
        move.l  mytask,a0
        move.l  184(a0),old_winptr  ; pr_WindowPtr: no DOS requesters
        move.l  #-1,184(a0)
        bsr     make_copper
        lea     CUSTOM,a5
        move.w  DMACONR(a5),old_dma
        move.w  #$8000|$0200|$0100|$0080|$0040|$0020,DMACON(a5)   ; planes, copper, blitter, sprites
        move.l  p_copper,COP1LC(a5)
        rts

video_off
        lea     CUSTOM,a5
        move.w  #$0020,DMACON(a5)   ; sprites off
        move.l  mytask,a0
        move.l  old_winptr,184(a0)
        move.l  gfxbase,a6
        move.l  38(a6),COP1LC(a5)   ; gb_copinit
        move.w  d0,COPJMP1(a5)
        move.w  old_dma,d0
        or.w    #$8000,d0
        move.w  d0,DMACON(a5)
        move.l  old_view,a1
        jsr     _LVOLoadView(a6)
        jsr     _LVOWaitTOF(a6)
        tst.b   blit_owned
        beq     .nb
        jsr     _LVOWaitBlit(a6)
        jsr     _LVODisownBlitter(a6)
        clr.b   blit_owned
.nb     rts

blit_wait
        tst.w   CUSTOM+DMACONR      ; (first read for old Agnus chips)
.w      btst    #6,CUSTOM+DMACONR
        bne     .w
        rts

wait_frame                          ; until the next vertical blank
        move.l  frames,d0
.w      cmp.l   frames,d0
        beq     .w
        rts

wait_frames                         ; d0 = frames
        subq.w  #1,d0
        bmi     .x
.lp     move.w  d0,-(sp)
        bsr     wait_frame
        move.w  (sp)+,d0
        dbf     d0,.lp
.x      rts

;----------------------------------------------------------------------
;  vertical blank: frame counter, the shown buffer, the mouse pointer,
;  sound and music, palette fades
;----------------------------------------------------------------------
vbl_on
        move.l  execbase,a6
        lea     vbl_int,a1
        move.b  #2,8(a1)            ; NT_INTERRUPT
        move.b  #10,9(a1)
        move.l  #vbl_name,10(a1)
        move.l  #vbl_server,18(a1)
        moveq   #INTB_VERTB,d0
        jsr     _LVOAddIntServer(a6)
        rts

vbl_off
        move.l  execbase,a6
        lea     vbl_int,a1
        moveq   #INTB_VERTB,d0
        jsr     _LVORemIntServer(a6)
        rts

vbl_server
        movem.l d2-d7/a2-a6,-(sp)
        addq.l  #1,frames
        tst.l   swap_to             ; a new picture is ready: show it
        beq     .ns
        move.l  swap_to,d0
        clr.l   swap_to
        move.l  p_cop_planes,a0
        moveq   #ROOM_PL-1,d1
.pl     swap    d0
        move.w  d0,2(a0)
        swap    d0
        move.w  d0,6(a0)
        addq.l  #8,a0
        add.l   #40,d0
        dbf     d1,.pl
        st      swapped
.ns     bsr     pointer_tick
        bsr     fade_tick
        bsr     sound_tick
        movem.l (sp)+,d2-d7/a2-a6
        lea     CUSTOM,a0
        moveq   #0,d0
        rts

;----------------------------------------------------------------------
;  the mouse pointer: hardware sprite 0
;----------------------------------------------------------------------
pointer_tick
        move.l  p_pointer,a0
        tst.b   pointer_on
        bne     .on
        clr.l   (a0)                ; off: an empty sprite
        rts
.on     move.w  mouse_x,d0
        move.w  mouse_y,d1
        sub.w   #7,d0               ; the hot spot is the middle of the cross
        sub.w   #7,d1
        add.w   #$81-1,d0           ; screen x -> sprite x
        add.w   #TOP_LINE,d1        ; screen y -> line
        move.w  d1,d2
        add.w   #15,d2              ; last line + 1
        moveq   #0,d3
        move.w  d1,d4
        lsl.w   #8,d4
        move.w  d0,d5
        lsr.w   #1,d5
        move.b  d5,d4               ; SPRxPOS
        move.w  d2,d3
        lsl.w   #8,d3               ; SPRxCTL: stop line
        btst    #8,d1
        beq     .1
        bset    #2,d3
.1      btst    #8,d2
        beq     .2
        bset    #1,d3
.2      btst    #0,d0
        beq     .3
        bset    #0,d3
.3      move.w  d4,(a0)
        move.w  d3,2(a0)
        rts

;----------------------------------------------------------------------
;  input: an input.device handler in front of Intuition takes every event
;----------------------------------------------------------------------
input_on                            ; -> d0 = 0 on failure
        move.l  execbase,a6
        moveq   #-1,d0
        jsr     _LVOAllocSignal(a6)
        move.b  d0,in_port+15       ; mp_SigBit
        bmi     .fail
        lea     in_port,a0
        move.b  #4,8(a0)            ; NT_MSGPORT
        clr.b   14(a0)              ; PA_SIGNAL
        move.l  mytask,16(a0)
        lea     20(a0),a1           ; NewList
        move.l  a1,28(a0)
        addq.l  #4,a1
        clr.l   (a1)
        move.l  a1,20(a0)
        lea     in_req,a1
        move.b  #5,8(a1)            ; NT_MESSAGE
        move.l  #in_port,14(a1)     ; mn_ReplyPort
        move.w  #48,18(a1)
        lea     inputname,a0
        moveq   #0,d0
        moveq   #0,d1
        jsr     _LVOOpenDevice(a6)
        tst.l   d0
        bne     .fail
        lea     in_int,a0
        move.b  #2,8(a0)
        move.b  #100,9(a0)          ; before Intuition (50)
        move.l  #vbl_name,10(a0)
        move.l  #input_handler,18(a0)
        lea     in_req,a1
        move.w  #9,28(a1)           ; IND_ADDHANDLER
        move.l  #in_int,40(a1)
        jsr     _LVODoIO(a6)
        moveq   #1,d0
        rts
.fail   moveq   #0,d0
        rts

input_off
        move.l  execbase,a6
        lea     in_req,a1
        move.w  #10,28(a1)          ; IND_REMHANDLER
        move.l  #in_int,40(a1)
        jsr     _LVODoIO(a6)
        lea     in_req,a1
        jsr     _LVOCloseDevice(a6)
        moveq   #0,d0
        move.b  in_port+15,d0
        jsr     _LVOFreeSignal(a6)
        rts

input_handler                       ; a0 = event list -> d0 = events left (none)
        movem.l d2/a2,-(sp)
        move.l  a0,d1
.lp     beq     .done
        move.l  d1,a2
        move.b  4(a2),d0            ; ie_Class
        cmp.b   #1,d0               ; IECLASS_RAWKEY
        bne     .mouse
        move.w  6(a2),d0
        cmp.w   #$80,d0             ; key released
        bhs     .nx
        cmp.w   #$60,d0             ; shift and other qualifiers alone
        bhs     .nx
        cmp.w   #$4c,d0             ; cursor keys move the pointer
        blo     .key
        cmp.w   #$4f,d0
        bhi     .key
        bsr     key_pointer
        bra     .nx
.key    cmp.w   #$44,d0             ; RETURN / ENTER: the left button
        beq     .lb
        cmp.w   #$43,d0
        beq     .lb
        cmp.w   #$46,d0             ; DEL: the right button
        beq     .rb
        bsr     push_key
        bra     .nx
.mouse  cmp.b   #2,d0               ; IECLASS_RAWMOUSE
        bne     .nx
        move.w  10(a2),d0           ; ie_X, ie_Y: movement
        add.w   d0,mouse_x
        move.w  12(a2),d0
        add.w   d0,mouse_y
        bsr     clamp_mouse
        move.w  6(a2),d0            ; ie_Code
        cmp.w   #$68,d0             ; IECODE_LBUTTON
        bne     .r
.lb     move.w  #$100+1,d0          ; "key" 1 + $100: left button
        bsr     push_key
        bra     .nx
.r      cmp.w   #$69,d0             ; IECODE_RBUTTON
        bne     .nx
.rb     move.w  #$100+2,d0
        bsr     push_key
.nx     move.l  (a2),d1
        bra     .lp
.done   movem.l (sp)+,d2/a2
        moveq   #0,d0
        rts

key_pointer                         ; d0 = $4c..$4f (up, down, right, left), a2 = the event
        moveq   #6,d1               ; 6 pixels, 1 with SHIFT
        move.w  8(a2),d2            ; ie_Qualifier
        and.w   #3,d2
        beq     .s
        moveq   #1,d1
.s      sub.w   #$4c,d0
        bne     .dn
        sub.w   d1,mouse_y
        bra     clamp_mouse
.dn     subq.w  #1,d0
        bne     .rt
        add.w   d1,mouse_y
        bra     clamp_mouse
.rt     subq.w  #1,d0
        bne     .lt
        add.w   d1,mouse_x
        bra     clamp_mouse
.lt     sub.w   d1,mouse_x

clamp_mouse
        tst.w   mouse_x
        bpl     .x0
        clr.w   mouse_x
.x0     cmp.w   #319,mouse_x
        ble     .x1
        move.w  #319,mouse_x
.x1     tst.w   mouse_y
        bpl     .y0
        clr.w   mouse_y
.y0     cmp.w   #ROOM_H+PANEL_H,mouse_y
        blt     .y1
        move.w  #ROOM_H+PANEL_H,mouse_y
.y1     rts

push_key                            ; d0.w = raw key code ($100+n: mouse button n)
        move.w  key_w,d1
        lea     key_buf,a1
        add.w   d1,d1
        move.w  d0,(a1,d1.w)
        move.w  key_w,d1
        addq.w  #1,d1
        and.w   #31,d1
        cmp.w   key_r,d1
        beq     .full
        move.w  d1,key_w
.full   rts

get_key                             ; -> d0.w = key, Z=1 if none
        moveq   #0,d0
        move.w  key_r,d1
        cmp.w   key_w,d1
        beq     .none
        lea     key_buf,a0
        add.w   d1,d1
        move.w  (a0,d1.w),d0
        move.w  key_r,d1
        addq.w  #1,d1
        and.w   #31,d1
        move.w  d1,key_r
        tst.w   d0
.none   rts

flush_keys
        move.w  key_w,key_r
        rts

;----------------------------------------------------------------------
;  the loading screen (320 x 256, 32 colours) with its progress bar,
;  in the first screen buffers while the data files load (the system
;  still runs: the floppy needs it, and its blitter)
;----------------------------------------------------------------------
loading_show
        lea     loadpic,a0
        move.l  p_buf0,a1
        bsr     unzx
        move.l  gfxbase,a6
        move.l  34(a6),old_view     ; gb_ActiView
        sub.l   a1,a1
        jsr     _LVOLoadView(a6)
        jsr     _LVOWaitTOF(a6)
        jsr     _LVOWaitTOF(a6)
        move.l  p_copper,a0
        move.l  #$01005200,(a0)+    ; 5 planes
        move.l  #$01020000,(a0)+
        move.l  #$01040000,(a0)+
        move.l  #$008e2c81,(a0)+
        move.l  #$00902cc1,(a0)+    ; 256 lines
        move.l  #$00920038,(a0)+
        move.l  #$009400d0,(a0)+
        move.l  #$010800a0,(a0)+    ; modulo 160: interleaved
        move.l  #$010a00a0,(a0)+
        move.l  p_buf0,d0
        move.w  #BPL1PT,d2
        moveq   #4,d1
.pl     move.w  d2,(a0)+
        swap    d0
        move.w  d0,(a0)+
        addq.w  #2,d2
        move.w  d2,(a0)+
        swap    d0
        move.w  d0,(a0)+
        addq.w  #2,d2
        add.l   #40,d0
        dbf     d1,.pl
        move.l  p_nullspr,d0        ; no sprites
        move.w  #SPR0PT,d2
        moveq   #7,d1
.sp     move.w  d2,(a0)+
        swap    d0
        move.w  d0,(a0)+
        addq.w  #2,d2
        move.w  d2,(a0)+
        swap    d0
        move.w  d0,(a0)+
        addq.w  #2,d2
        dbf     d1,.sp
        lea     loadpal,a1
        move.w  #COLOR00,d2
        moveq   #31,d1
.c      move.w  d2,(a0)+
        move.w  (a1)+,(a0)+
        addq.w  #2,d2
        dbf     d1,.c
        move.l  #$fffffffe,(a0)+
        lea     CUSTOM,a5
        move.l  p_copper,COP1LC(a5)
        move.w  #$8000|$0200|$0100|$0080,DMACON(a5)
        st      load_on
        clr.l   loaded
        rts

loading_bar                         ; the bar shows 'loaded' of LOAD_TOTAL bytes
        movem.l d0-d2/a0-a1,-(sp)
        move.l  loaded,d0
        lsr.l   #8,d0
        mulu    #BAR_BYTES,d0
        divu    #(LOAD_TOTAL>>8)+1,d0
        cmp.w   #BAR_BYTES,d0
        bls     .ok
        moveq   #BAR_BYTES,d0
.ok     subq.w  #1,d0
        bmi     .x
        lea     barstrip+BAR_COL,a0
        move.l  p_buf0,a1
        add.l   #BAR_ROW*ROOM_ROW+BAR_COL,a1
        moveq   #BAR_LINES*ROOM_PL-1,d2
.ln     move.w  d0,d1
.b      move.b  (a0,d1.w),(a1,d1.w)
        dbf     d1,.b
        lea     40(a0),a0
        lea     40(a1),a1
        dbf     d2,.ln
.x      movem.l (sp)+,d0-d2/a0-a1
        rts

loading_close                       ; (only when the game does not start)
        tst.b   load_on
        beq     .x
        clr.b   load_on
        lea     CUSTOM,a5
        move.l  gfxbase,a6
        move.l  38(a6),COP1LC(a5)   ; gb_copinit
        move.l  old_view,a1
        jsr     _LVOLoadView(a6)
        jsr     _LVOWaitTOF(a6)
.x      rts
