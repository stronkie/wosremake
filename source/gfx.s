;======================================================================
;  gfx.s - copper list, double buffered room screen, blitter objects
;          (actors, texts), room pictures, palettes and fades, the
;          proportional font, text over the actors' heads
;======================================================================

TXT_MAXW  = 300             ; text over a head: up to 300 pixels wide
TXT_WW    = 20              ; 19 words + 1 for the shift
TXT_MAXL  = 5               ; lines
TXT_H     = TXT_MAXL*9+3
TXT_BYTES = TXT_WW*2*(ROOM_PL+1)*TXT_H   ; planes, then the mask (one line per row)

; ---- the copper list -----------------------------------------------------
make_copper
        move.l  p_copper,a0
        move.l  #$01005200,(a0)+    ; 5 planes
        move.l  #$01020000,(a0)+
        move.l  #$01040024,(a0)+    ; sprites in front
        move.l  #$008e2c81,(a0)+
        move.l  #$009025c1,(a0)+    ; to line $125
        move.l  #$00920038,(a0)+
        move.l  #$009400d0,(a0)+
        move.w  #BPL1MOD,(a0)+
        move.w  #ROOM_ROW-40,(a0)+
        move.w  #BPL2MOD,(a0)+
        move.w  #ROOM_ROW-40,(a0)+
        move.l  a0,p_cop_planes
        move.l  p_buf0,d0
        moveq   #ROOM_PL-1,d1
        move.w  #BPL1PT,d2
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
        move.l  p_pointer,d0        ; sprite 0: the pointer, 1-7: nothing
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
        move.l  p_nullspr,d0
        dbf     d1,.sp
        move.l  a0,p_cop_room_pal
        move.w  #COLOR00,d2
        moveq   #31,d1
.c1     move.w  d2,(a0)+
        clr.w   (a0)+
        addq.w  #2,d2
        dbf     d1,.c1
        move.w  #((PANEL_LINE-1)<<8)|$07,(a0)+    ; the line between room and panel
        move.w  #$fffe,(a0)+
        move.l  #$01000200,(a0)+    ; no planes
        move.l  p_panel,d0
        moveq   #PANEL_PL-1,d1
        move.w  #BPL1PT,d2
.pp     move.w  d2,(a0)+
        swap    d0
        move.w  d0,(a0)+
        addq.w  #2,d2
        move.w  d2,(a0)+
        swap    d0
        move.w  d0,(a0)+
        addq.w  #2,d2
        add.l   #40,d0
        dbf     d1,.pp
        move.w  #BPL1MOD,(a0)+
        move.w  #PANEL_ROW-40,(a0)+
        move.w  #BPL2MOD,(a0)+
        move.w  #PANEL_ROW-40,(a0)+
        move.l  a0,p_cop_panel_pal
        move.w  #COLOR00,d2
        moveq   #15,d1
.c2     move.w  d2,(a0)+
        clr.w   (a0)+
        addq.w  #2,d2
        dbf     d1,.c2
        move.w  #(PANEL_LINE<<8)|$07,(a0)+
        move.w  #$fffe,(a0)+
        move.l  #$01004200,(a0)+    ; 4 planes
        move.l  #$fffffffe,(a0)+
        rts

;----------------------------------------------------------------------
;  palettes: cur_pal (32 room/actor colours) and panel_pal (16), faded
;  by fade_level 0 (black) - 16 (full) into the copper list
;----------------------------------------------------------------------
fade_to                             ; d0 = target level 0-16 (the VBL steps there)
        move.w  d0,fade_target
        rts

fade_wait                           ; until the fade is done
.w      move.w  fade_level,d0
        cmp.w   fade_target,d0
        beq     .x
        bsr     wait_frame
        bra     .w
.x      rts

fade_tick
        bsr     cycle_tick
        move.w  fade_level,d0
        cmp.w   fade_target,d0
        beq     .same
        blt     .up
        subq.w  #1,d0
        bra     .set
.up     addq.w  #1,d0
.set    move.w  d0,fade_level
        st      pal_dirty
.same   tst.b   pal_dirty
        beq     .x
        clr.b   pal_dirty
        move.w  fade_level,d7
        lea     cur_pal,a1
        move.l  p_cop_room_pal,a0
        moveq   #31,d6
.r      move.w  (a1)+,d0
        bsr     fade_col
        move.w  d0,2(a0)
        addq.l  #4,a0
        dbf     d6,.r
        lea     panel_pal,a1
        move.l  p_cop_panel_pal,a0
        moveq   #15,d6
        tst.b   panel_dark          ; a cutscene: the panel is dark
        beq     .p
        moveq   #0,d7
.p      move.w  (a1)+,d0
        bsr     fade_col
        move.w  d0,2(a0)
        addq.l  #4,a0
        dbf     d6,.p
.x      rts

fade_col                            ; d0 = $0rgb, d7 = level 0-16 -> d0
        cmp.w   #16,d7
        beq     .x
        move.w  d0,d1
        lsr.w   #8,d1
        and.w   #15,d1
        mulu    d7,d1
        lsr.w   #4,d1
        move.w  d0,d2
        lsr.w   #4,d2
        and.w   #15,d2
        mulu    d7,d2
        lsr.w   #4,d2
        and.w   #15,d0
        mulu    d7,d0
        lsr.w   #4,d0
        lsl.w   #8,d1
        lsl.w   #4,d2
        or.w    d1,d0
        or.w    d2,d0
.x      rts

cycle_tick                          ; the room's colour cycles (water, fire, stars...)
        tst.w   cur_room
        beq     .x
        move.l  cur_room_ptr,a0
        move.l  R_CYC(a0),d0
        beq     .x
        add.l   dat,d0
        move.l  d0,a0
        move.w  (a0)+,d6
        subq.w  #1,d6
        bmi     .x
        lea     cur_pal,a1
.lp     move.w  (a0)+,d1            ; register
        move.w  (a0)+,d2            ; frames per step
        move.w  (a0)+,d3            ; colours
        move.l  frames,d0
        and.l   #$7fff,d0
        divu    d2,d0
        and.l   #$ffff,d0
        divu    d3,d0
        swap    d0                  ; (frames / step) mod colours
        add.w   d0,d0
        move.w  (a0,d0.w),d0
        add.w   d1,d1
        cmp.w   (a1,d1.w),d0
        beq     .same
        move.w  d0,(a1,d1.w)
        st      pal_dirty
.same   add.w   d3,d3
        add.w   d3,a0
        dbf     d6,.lp
.x      rts

;----------------------------------------------------------------------
;  room pictures
;----------------------------------------------------------------------
show_room_picture                   ; a0 = room -> background, both screens, palette
        move.l  a0,a2
        move.l  R_PIC(a2),d0
        bpl     .indat
        cmp.l   pic_cached,d0       ; the picture comes from the stream file (kept for redraws)
        beq     .have
        move.l  #-1,pic_cached
        move.l  room_buf,a1
        move.l  #STR_ROOM_MAX,d1
        bsr     stream_read
        tst.l   d0
        beq     .pal
        move.l  R_PIC(a2),pic_cached
.have   move.l  room_buf,a0
        bra     .unpack
.indat  move.l  d0,a0
        add.l   dat,a0
.unpack move.l  p_bg,a1
        bsr     unzx
.pal
        lea     R_PAL(a2),a0        ; colours 0-15 from the room
        lea     cur_pal,a1
        moveq   #15,d0
.c      move.w  (a0)+,(a1)+
        dbf     d0,.c
        st      pal_dirty
        bsr     draw_object_images  ; objects with pictures (open doors...)
        bra     bg_to_screens

bg_to_screens                       ; the background -> both screens
        move.l  p_bg,a0
        move.l  p_buf0,a1
        bsr     .copy
        move.l  p_bg,a0
        move.l  p_buf1,a1
        bsr     .copy
        clr.w   ndirty0
        clr.w   ndirty1
        rts
.copy   bsr     blit_wait
        lea     CUSTOM,a5
        move.l  #$09f00000,BLTCON0(a5)
        move.l  #$ffffffff,BLTAFWM(a5)
        clr.l   BLTAMOD(a5)         ; A and D modulo 0
        move.l  a0,BLTAPT(a5)
        move.l  a1,BLTDPT(a5)
        move.w  #((ROOM_H*ROOM_PL)<<6)|20,BLTSIZE(a5)
        rts

draw_object_images                  ; every object of the room with ST_IMAGE
        move.l  cur_room_ptr,a2
        move.l  R_OBJS(a2),d0
        beq     .x
        move.l  dat,a3
        add.l   d0,a3
.lp     move.w  (a3)+,d0            ; object number
        bmi     .x
        lea     obj_state,a0
        btst    #1,(a0,d0.w)        ; ST_IMAGE
        beq     .lp
        bsr     obj_ptr             ; -> a0
        move.l  O_IMAGE(a0),d1
        beq     .lp
        move.w  O_IX(a0),d0
        move.w  O_IY(a0),d2
        move.l  dat,a0
        add.l   d1,a0               ; frame
        move.w  d2,d1
        move.l  p_bg,a1
        bsr     draw_bob_nohot
        bra     .lp
.x      rts

;----------------------------------------------------------------------
;  the frame cache: the people and object pictures live in any memory
;  (WOS2.GFX); a frame is copied to a ring of chip memory when it is drawn
;  and stays there until the ring comes round again
;----------------------------------------------------------------------
FC_N      = 64                      ; frames remembered
frame_chip                          ; a2 = F_DATA, d2 = words, d3 = lines -> a2 = chip
        move.l  a2,d4
        bmi     .abs
        movem.l d0-d1/d5-d7/a0-a1/a3,-(sp)
        lea     fc_tab,a0           ; off.l, addr.l, end.l
        moveq   #FC_N-1,d0
.find   cmp.l   (a0),d4
        beq     .hit
        lea     12(a0),a0
        dbf     d0,.find
        move.w  d2,d5               ; not there: bytes = words*2*lines*(planes+mask)
        mulu    d3,d5
        mulu    #2*(ROOM_PL+1),d5
        move.l  fc_head,d6
        move.l  d6,d0
        add.l   d5,d0
        cmp.l   #FC_SIZE,d0
        bls     .fits
        moveq   #0,d6               ; round the ring
        move.l  d5,d0
.fits   move.l  d0,fc_head
        add.l   p_fcache,d6         ; d6..d0 the new place
        add.l   p_fcache,d0
        lea     fc_tab,a0           ; forget what was there
        moveq   #FC_N-1,d1
.old    cmp.l   4(a0),d0
        bls     .keep
        cmp.l   8(a0),d6
        bhs     .keep
        moveq   #-1,d7
        move.l  d7,(a0)
        clr.l   8(a0)
.keep   lea     12(a0),a0
        dbf     d1,.old
        move.w  fc_next,d1          ; the next slot
        addq.w  #1,d1
        and.w   #FC_N-1,d1
        move.w  d1,fc_next
        mulu    #12,d1
        lea     fc_tab,a0
        add.l   d1,a0
        move.l  d4,(a0)
        move.l  d6,4(a0)
        move.l  d0,8(a0)
        bsr     blit_wait           ; (the blitter may still read the old frame there)
        move.l  gfx,a1
        add.l   d4,a1
        move.l  d6,a3
        lsr.l   #2,d5
        subq.l  #1,d5
.cp     move.l  (a1)+,(a3)+
        subq.l  #1,d5
        bpl     .cp
.hit    move.l  4(a0),a2
        movem.l (sp)+,d0-d1/d5-d7/a0-a1/a3
        rts
.abs    bclr    #31,d4
        move.l  d4,a2
        rts

fc_reset
        lea     fc_tab,a0
        moveq   #FC_N-1,d0
.l      move.l  #-1,(a0)+
        clr.l   (a0)+
        clr.l   (a0)+
        dbf     d0,.l
        clr.l   fc_head
        clr.w   fc_next
        rts

;----------------------------------------------------------------------
;  blitter objects: a frame (interleaved planes, then the same size of
;  mask) drawn with the cookie cut, and the dirty rectangles to restore
;----------------------------------------------------------------------
draw_bob                            ; a0 = frame, d0/d1 = x/y of the hot spot, a1 = screen
        sub.w   F_HX(a0),d0
        sub.w   F_HY(a0),d1
draw_bob_nohot                      ; d0/d1 = top left. -> d0-d3 = rect (word x, y, words, h)
        movem.l d4-d7/a2-a5,-(sp)
        move.w  F_H(a0),d3          ; clip at the top and the bottom of the room
        move.w  F_WW(a0),d2
        move.l  F_DATA(a0),a2
        bsr     frame_chip          ; planes, in chip memory
        move.w  d2,d4
        add.w   d4,d4
        mulu    d3,d4
        mulu    #ROOM_PL,d4
        lea     (a2,d4.l),a3        ; mask
        tst.w   d1
        bpl     .top
        add.w   d1,d3               ; cut the lines above the room
        ble     .none
        neg.w   d1
        move.w  d2,d4
        add.w   d4,d4
        mulu    #ROOM_PL,d4
        mulu    d1,d4
        add.l   d4,a2
        move.w  d2,d4
        add.w   d4,d4
        mulu    d1,d4
        add.l   d4,a3
        moveq   #0,d1
.top    move.w  d1,d4
        add.w   d3,d4
        sub.w   #ROOM_H,d4
        ble     .bot
        sub.w   d4,d3
        ble     .none
.bot    tst.w   d0                  ; keep inside the screen sideways
        bpl     .l
        moveq   #0,d0
.l      move.w  d2,d4
        lsl.w   #4,d4
        add.w   d0,d4
        cmp.w   #SCR_W+16,d4
        ble     .r
        move.w  #SCR_W+16,d0
        move.w  d2,d4
        lsl.w   #4,d4
        sub.w   d4,d0
.r      move.w  d0,d5
        and.w   #15,d5              ; shift
        ror.w   #4,d5
        move.w  d0,d4
        asr.w   #4,d4               ; word column
        move.w  d4,d0
        move.w  d1,d6
        mulu    #ROOM_ROW,d6
        add.l   d6,a1
        add.w   d4,a1
        add.w   d4,a1
        movem.w d0/d1,bob_rect
        move.w  d3,d7
        lsl.w   #6,d7
        or.w    d2,d7               ; d7 = blit size of one plane
        moveq   #40,d6
        sub.w   d2,d6
        sub.w   d2,d6
        move.w  d2,d4
        add.w   d4,d4
        mulu    #ROOM_PL-1,d4       ; B skips the other planes
        or.w    #$0fca,d5
        lea     CUSTOM,a5
        moveq   #ROOM_PL-1,d1
        move.l  a1,a4
.pl     bsr     blit_wait
        move.w  d5,BLTCON0(a5)
        move.w  d5,d0
        and.w   #$f000,d0
        move.w  d0,BLTCON1(a5)
        move.l  #$ffff0000,BLTAFWM(a5)
        clr.w   BLTAMOD(a5)
        move.w  d4,BLTBMOD(a5)
        move.w  d6,d0
        add.w   #ROOM_ROW-40,d0
        move.w  d0,BLTCMOD(a5)
        move.w  d0,BLTDMOD(a5)
        move.l  a3,BLTAPT(a5)
        move.l  a2,BLTBPT(a5)
        move.l  a4,BLTCPT(a5)
        move.l  a4,BLTDPT(a5)
        move.w  d7,BLTSIZE(a5)
        add.w   d2,a2
        add.w   d2,a2
        lea     40(a4),a4
        dbf     d1,.pl
        movem.w bob_rect,d0/d1
        movem.l (sp)+,d4-d7/a2-a5
        rts
.none   moveq   #0,d3
        movem.l (sp)+,d4-d7/a2-a5
        rts

restore_rect                        ; d0 = word column, d1 = y, d2 = words, d3 = lines, a1 = screen
        tst.w   d3
        beq     .x
        move.w  d1,d4
        mulu    #ROOM_ROW,d4
        add.w   d0,d4
        add.w   d0,d4
        move.l  p_bg,a0
        add.l   d4,a0
        add.l   d4,a1
        bsr     blit_wait
        lea     CUSTOM,a5
        move.l  #$09f00000,BLTCON0(a5)
        move.l  #$ffffffff,BLTAFWM(a5)
        moveq   #40,d4
        sub.w   d2,d4
        sub.w   d2,d4
        move.w  d4,BLTAMOD(a5)
        move.w  d4,BLTDMOD(a5)
        move.l  a0,BLTAPT(a5)
        move.l  a1,BLTDPT(a5)
        mulu    #ROOM_PL,d3
        lsl.w   #6,d3
        or.w    d2,d3
        move.w  d3,BLTSIZE(a5)
.x      rts

;----------------------------------------------------------------------
;  drawing a frame of the game: the hidden screen gets the actors and
;  texts, then it is shown at the next vertical blank
;----------------------------------------------------------------------
render
.wsw    tst.l   swap_to             ; the last picture is not shown yet
        bne     .wsw
        move.l  p_buf0,a4           ; a4 = hidden screen, a3 = its dirty list
        lea     dirty0,a3
        lea     ndirty0,a2
        move.l  shown,d0
        cmp.l   a4,d0
        bne     .b
        move.l  p_buf1,a4
        lea     dirty1,a3
        lea     ndirty1,a2
.b      move.w  (a2),d7             ; restore what was drawn there before
        clr.w   (a2)
        move.l  a3,a6
        bra     .rn
.rl     movem.w (a6)+,d0-d3
        move.l  a4,a1
        bsr     restore_rect
.rn     dbf     d7,.rl
        bsr     sort_actors         ; -> draw_list (actor numbers, back to front)
        lea     draw_list,a6
.al     move.w  (a6)+,d0
        bmi     .texts
        bsr     act_ptr             ; a0 = actor
        move.l  A_COST(a0),a5
        add.l   dat,a5
        move.l  C_FRAMES(a5),a5
        add.l   dat,a5
        move.w  A_FRAME(a0),d1
        mulu    #F_SIZE,d1
        add.l   d1,a5
        move.w  A_X(a0),d0
        move.w  A_Y(a0),d1
        move.l  a5,a0
        move.l  a4,a1
        bsr     draw_bob
        bsr     .note
        bra     .al
.texts  lea     texts,a5
        moveq   #1,d6
.tl     tst.w   T_ON(a5)
        beq     .tn
        lea     T_FRAME(a5),a0
        move.w  T_X(a5),d0
        move.w  T_Y(a5),d1
        move.l  a4,a1
        bsr     draw_bob_nohot
        bsr     .note
.tn     lea     T_SIZE(a5),a5
        dbf     d6,.tl
        bsr     blit_wait
        move.l  a4,shown
        move.l  a4,swap_to
        rts
.note   tst.w   d3                  ; remember the rectangle to restore later
        beq     .nx
        move.w  (a2),d4
        cmp.w   #MAXDIRTY,d4
        bhs     .nx
        lsl.w   #3,d4
        movem.w d0-d3,(a3,d4.w)
        addq.w  #1,(a2)
.nx     rts

sort_actors                         ; the actors in this room, back to front (by y)
        lea     draw_list,a1
        moveq   #0,d7               ; count
        moveq   #0,d0
.lp     bsr     act_ptr
        move.w  A_ROOM(a0),d1
        cmp.w   cur_room,d1
        bne     .nx
        tst.l   A_COST(a0)          ; (no costume: not drawn)
        beq     .nx
        move.w  A_Y(a0),d2
        move.w  d7,d3               ; put at the end, then move it down
        add.w   d3,d3
        move.w  d0,(a1,d3.w)
        move.w  d7,d5
.bub    subq.w  #1,d5
        bmi     .in
        move.w  d5,d3
        add.w   d3,d3
        move.w  (a1,d3.w),d4        ; the one before
        move.l  a0,-(sp)
        move.w  d0,-(sp)
        move.w  d4,d0
        bsr     act_ptr
        move.w  A_Y(a0),d4
        move.w  (sp)+,d0
        move.l  (sp)+,a0
        cmp.w   d2,d4
        ble     .in
        move.w  (a1,d3.w),d4        ; swap the two
        move.w  2(a1,d3.w),(a1,d3.w)
        move.w  d4,2(a1,d3.w)
        bra     .bub
.in     addq.w  #1,d7
.nx     addq.w  #1,d0
        cmp.w   #MAXACT,d0
        blo     .lp
        add.w   d7,d7
        move.w  #-1,(a1,d7.w)
        rts

;----------------------------------------------------------------------
;  the font: 96 glyphs of (.b width, 8 rows); drawn in a chunky buffer
;----------------------------------------------------------------------
text_width                          ; a0 = text (to 0 or 10) -> d0 = pixels
        move.l  font,a1
        moveq   #0,d0
.lp     moveq   #0,d1
        move.b  (a0)+,d1
        beq     .x
        cmp.b   #10,d1
        beq     .x
        sub.b   #32,d1
        bcs     .lp
        mulu    #9,d1
        moveq   #0,d2
        move.b  (a1,d1.w),d2
        add.w   d2,d0
        addq.w  #1,d0
        bra     .lp
.x      rts

chunky_glyph                        ; d0 = char, d1 = x, d2 = y, d3 = colour, a2 = chunky (320 wide)
        movem.l d0-d5/a0-a1,-(sp)
        sub.b   #32,d0
        bcs     .x
        and.w   #$7f,d0
        mulu    #9,d0
        move.l  font,a0
        lea     1(a0,d0.w),a0
        move.w  d2,d4
        mulu    #320,d4
        add.w   d1,d4
        lea     (a2,d4.l),a1
        moveq   #7,d5
.row    move.b  (a0)+,d4
        moveq   #0,d0
.px     add.b   d4,d4
        bcc     .n
        move.b  d3,(a1,d0.w)
.n      addq.w  #1,d0
        tst.b   d4
        bne     .px
        lea     320(a1),a1
        dbf     d5,.row
.x      movem.l (sp)+,d0-d5/a0-a1
        rts

;----------------------------------------------------------------------
;  a text over an actor's head: wrapped, outlined, made into a bob
;----------------------------------------------------------------------
T_ON      = 0               ; .w on
T_ACT     = 2               ; .w actor (-1: a card in the middle)
T_X       = 4
T_Y       = 6
T_TIME    = 8               ; .w ticks left
T_FRAME   = 10              ; a frame (F_SIZE) for draw_bob_nohot
T_SIZE    = T_FRAME+F_SIZE

make_text                           ; a0 = text, d0 = colour, d1 = slot, d2 = actor -> shows it
        movem.l d2-d7/a2-a6,-(sp)
        move.w  d0,txt_col
        move.w  d2,txt_act
        lea     texts,a6
        mulu    #T_SIZE,d1
        add.l   d1,a6
        move.l  a0,a5
        lea     txt_lines,a4        ; wrap: line starts and lengths
        moveq   #0,d6               ; lines
.wrap   move.l  a5,(a4)+
        moveq   #0,d5               ; width so far
        move.l  a5,a3               ; last space
        sub.l   a3,a3
.wc     move.b  (a5),d0
        beq     .eol
        cmp.b   #10,d0
        beq     .nl
        cmp.b   #' ',d0
        bne     .ch
        move.l  a5,a3
.ch     moveq   #0,d1
        move.b  d0,d1
        sub.b   #32,d1
        mulu    #9,d1
        move.l  font,a0
        moveq   #0,d2
        move.b  (a0,d1.w),d2
        addq.w  #1,d2
        add.w   d2,d5
        cmp.w   #TXT_MAXW-4,d5
        bgt     .brk
        addq.l  #1,a5
        bra     .wc
.brk    move.l  a3,d0               ; break at the last space (or here)
        beq     .eol
        move.l  a3,a5
.nl     move.l  a5,(a4)+            ; end of this line
        addq.l  #1,a5               ; skip the space / newline
        addq.w  #1,d6
        cmp.w   #TXT_MAXL,d6
        blo     .wrap
        bra     .wrapped
.eol    move.l  a5,(a4)+
        addq.w  #1,d6
.wrapped
        move.w  d6,txt_nlines
        move.l  txt_chunky,a2       ; clear the chunky buffer
        move.w  #320*TXT_H/4-1,d0
        move.l  a2,a0
.cl     clr.l   (a0)+
        dbf     d0,.cl
        moveq   #0,d7               ; widest line
        lea     txt_lines,a4
        moveq   #0,d4               ; line
.line   cmp.w   d6,d4
        bhs     .drawn
        move.l  (a4)+,a3            ; start
        move.l  (a4)+,a5            ; end
        move.l  a3,a0               ; width of this line
        moveq   #0,d5
.lw     cmp.l   a5,a0
        bhs     .lwd
        moveq   #0,d1
        move.b  (a0)+,d1
        sub.b   #32,d1
        mulu    #9,d1
        move.l  font,a1
        moveq   #0,d2
        move.b  (a1,d1.w),d2
        add.w   d2,d5
        addq.w  #1,d5
        bra     .lw
.lwd    cmp.w   d7,d5
        ble     .nw
        move.w  d5,d7
.nw     move.w  #TXT_MAXW,d1        ; centred in the buffer
        sub.w   d5,d1
        lsr.w   #1,d1
        addq.w  #1,d1
        move.w  d4,d2
        mulu    #9,d2
        addq.w  #1,d2
.gl     cmp.l   a5,a3
        bhs     .gld
        moveq   #0,d0
        move.b  (a3)+,d0
        movem.w d1-d2,-(sp)         ; the outline: the glyph in black 8 times around
        moveq   #16,d3
        subq.w  #1,d1
        subq.w  #1,d2
        bsr     chunky_glyph
        addq.w  #1,d1
        bsr     chunky_glyph
        addq.w  #1,d1
        bsr     chunky_glyph
        addq.w  #1,d2
        bsr     chunky_glyph
        addq.w  #1,d2
        bsr     chunky_glyph
        subq.w  #1,d1
        bsr     chunky_glyph
        subq.w  #1,d1
        bsr     chunky_glyph
        subq.w  #1,d2
        bsr     chunky_glyph
        movem.w (sp)+,d1-d2
        move.w  txt_col,d3
        bsr     chunky_glyph
        moveq   #0,d3               ; next x
        sub.b   #32,d0
        mulu    #9,d0
        move.l  font,a0
        move.b  (a0,d0.w),d3
        add.w   d3,d1
        addq.w  #1,d1
        bra     .gl
.gld    addq.w  #1,d4
        bra     .line
.drawn  ; chunky -> planes + mask (the whole 304 pixel wide buffer)
        move.w  d6,d0
        mulu    #9,d0
        addq.w  #3,d0
        move.w  d0,txt_h
        move.w  d7,txt_w
        bsr     text_to_planes      ; a6 = slot
        ; place it: centred over the actor's head, inside the room
        move.w  #TXT_MAXW,d0
        sub.w   txt_w,d0
        lsr.w   #1,d0               ; empty pixels left in the buffer
        move.w  d0,d5
        move.w  txt_act,d0
        bmi     .card
        bsr     act_ptr
        move.w  A_X(a0),d0
        move.w  A_Y(a0),d1
        move.l  A_COST(a0),a1
        add.l   dat,a1
        move.l  C_FRAMES(a1),a1
        add.l   dat,a1
        sub.w   F_HY(a1),d1         ; the top of the actor
        sub.w   #6,d1
        sub.w   txt_h,d1
        bra     .pos
.card   move.w  #160,d0
        moveq   #6,d1               ; -2: over the radio, at the top
        cmp.w   #-2,txt_act
        beq     .pos
        move.w  #ROOM_H/2,d1
        move.w  txt_h,d2
        lsr.w   #1,d2
        sub.w   d2,d1
.pos    move.w  txt_w,d2            ; left edge of the text, inside 4..316
        lsr.w   #1,d2
        sub.w   d2,d0
        cmp.w   #4,d0
        bge     .p1
        moveq   #4,d0
.p1     move.w  d0,d2
        add.w   txt_w,d2
        cmp.w   #316,d2
        ble     .p2
        move.w  #316,d0
        sub.w   txt_w,d0
.p2     tst.w   d1
        bpl     .p3
        moveq   #0,d1
.p3     sub.w   d5,d0               ; the buffer's left edge
        move.w  d0,T_X(a6)
        move.w  d1,T_Y(a6)
        move.w  txt_act,T_ACT(a6)
        move.w  #1,T_ON(a6)
        movem.l (sp)+,d2-d7/a2-a6
        rts

text_to_planes                      ; txt_chunky (txt_h lines) -> the slot's chip buffer
        lea     T_FRAME(a6),a0
        move.w  #TXT_WW,F_WW(a0)
        move.w  txt_h,F_H(a0)
        clr.l   F_HX(a0)
        move.l  a6,d0
        sub.l   #texts,d0
        divu    #T_SIZE,d0          ; slot
        mulu    #TXT_BYTES,d0
        add.l   p_textbuf,d0
        move.l  d0,a1               ; planes
        bset    #31,d0
        move.l  d0,F_DATA(a0)       ; (bit 31: a chip address, not an offset in the file)
        move.w  txt_h,d0
        mulu    #TXT_WW*2*ROOM_PL,d0
        lea     (a1,d0.l),a3        ; mask
        move.l  txt_chunky,a2
        move.w  txt_h,txt_rows
.row    move.w  #TXT_WW-2,txt_words ; 19 words of 16 pixels
        move.l  a1,a4
        move.l  a3,a5
.word   moveq   #0,d0               ; planes 0-4 in d0-d4, mask in d5
        moveq   #0,d1
        moveq   #0,d2
        moveq   #0,d3
        moveq   #0,d4
        moveq   #0,d5
        moveq   #15,d6
.px     add.w   d5,d5
        add.w   d4,d4
        add.w   d3,d3
        add.w   d2,d2
        add.w   d1,d1
        add.w   d0,d0
        move.b  (a2)+,d7
        beq     .z
        addq.w  #1,d5
        lsr.b   #1,d7
        bcc     .b1
        addq.w  #1,d0
.b1     lsr.b   #1,d7
        bcc     .b2
        addq.w  #1,d1
.b2     lsr.b   #1,d7
        bcc     .b3
        addq.w  #1,d2
.b3     lsr.b   #1,d7
        bcc     .b4
        addq.w  #1,d3
.b4     lsr.b   #1,d7
        bcc     .z
        addq.w  #1,d4
.z      dbf     d6,.px
        move.w  d0,(a4)
        move.w  d1,TXT_WW*2(a4)
        move.w  d2,TXT_WW*4(a4)
        move.w  d3,TXT_WW*6(a4)
        move.w  d4,TXT_WW*8(a4)
        move.w  d5,(a5)
        addq.l  #2,a4
        addq.l  #2,a5
        subq.w  #1,txt_words
        bpl     .word
        moveq   #0,d0               ; the extra word for the shift
        move.w  d0,(a4)
        move.w  d0,TXT_WW*2(a4)
        move.w  d0,TXT_WW*4(a4)
        move.w  d0,TXT_WW*6(a4)
        move.w  d0,TXT_WW*8(a4)
        move.w  d0,(a5)
        lea     320-(TXT_WW-1)*16(a2),a2    ; next chunky line
        lea     TXT_WW*2*ROOM_PL(a1),a1
        lea     TXT_WW*2(a3),a3
        subq.w  #1,txt_rows
        bne     .row
        rts
