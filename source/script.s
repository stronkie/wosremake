;======================================================================
;  script.s - the script machine: four threads (0: the player's
;             actions and cutscenes, 1: the room's background events,
;             2: room timers, 3: entering a room)
;
;  A script is a list of words: an opcode, then its arguments. Jumps
;  and costumes are long offsets from the start of the data file.
;======================================================================

SL_PC    = 0                ; .l address (0: free)
SL_WAIT  = 4                ; .w what it waits for
SL_ARG   = 6
SL_SIZE  = 8

W_NONE   = 0
W_TEXT   = 1                ; a text slot to end
W_WALK   = 2                ; an actor to stop walking
W_TICKS  = 3
W_ANIM   = 4                ; an actor's animation to end
W_DIALOG = 5
W_FADE   = 6
W_KEY    = 7

run_script                          ; d0 = slot, a0 = script (stops what ran there)
        lea     slots,a1
        lsl.w   #3,d0
        move.l  a0,SL_PC(a1,d0.w)
        clr.w   SL_WAIT(a1,d0.w)
        rts

stop_room_scripts                   ; slots 1-3 (when leaving a room)
        lea     slots+SL_SIZE,a1
        clr.l   (a1)
        clr.l   SL_SIZE(a1)
        clr.l   2*SL_SIZE(a1)
        rts

vm_tick
        moveq   #0,d7
.lp     move.w  d7,cur_slot
        lea     slots,a5
        move.w  d7,d0
        lsl.w   #3,d0
        add.w   d0,a5
        tst.l   SL_PC(a5)
        beq     .nx
        bsr     vm_wait             ; still waiting?
        bne     .nx
        bsr     vm_run
.nx     addq.w  #1,d7
        cmp.w   #NSLOTS,d7
        blo     .lp
        lea     slots,a5            ; the player can act when slot 0 is free
        tst.l   SL_PC(a5)
        sne     d0
        ext.w   d0
        move.w  d0,ui_frozen
        rts

vm_wait                             ; a5 = slot -> Z=0 if it still waits
        move.w  SL_WAIT(a5),d0
        beq     .go
        move.w  SL_ARG(a5),d1
        cmp.w   #W_TEXT,d0
        bne     .1
        lea     texts,a0
        mulu    #T_SIZE,d1
        tst.w   T_ON(a0,d1.w)
        bne     .wait
        bra     .go
.1      cmp.w   #W_WALK,d0
        bne     .2
        move.w  d1,d0
        bsr     act_ptr
        cmp.w   #1,A_MODE(a0)
        beq     .wait
        bra     .go
.2      cmp.w   #W_TICKS,d0
        bne     .3
        subq.w  #1,SL_ARG(a5)
        bgt     .wait
        bra     .go
.3      cmp.w   #W_ANIM,d0
        bne     .4
        move.w  d1,d0
        bsr     act_ptr
        cmp.w   #3,A_MODE(a0)
        beq     .wait
        bra     .go
.4      cmp.w   #W_DIALOG,d0
        bne     .5
        tst.b   dlg_on
        bne     .wait
        move.w  dlg_choice,d0       ; jump to the chosen answer
        add.w   d0,d0
        add.w   d0,d0
        lea     dlg_target,a0
        move.l  (a0,d0.w),SL_PC(a5)
        bra     .go
.5      cmp.w   #W_KEY,d0
        bne     .6
        tst.b   key_hit
        beq     .wait
        bra     .go
.6      cmp.w   #W_FADE,d0
        bne     .go
        move.w  fade_level,d0
        cmp.w   fade_target,d0
        bne     .wait
.go     clr.w   SL_WAIT(a5)
        moveq   #0,d0               ; Z=1
        rts
.wait   tst.b   skip_cutscene       ; ESC: cutscenes fly by
        beq     .w2
        cmp.w   #W_TICKS,SL_WAIT(a5)
        beq     .go
.w2     moveq   #1,d0
        rts

;----------------------------------------------------------------------
;  running a thread until it waits or ends
;----------------------------------------------------------------------
vm_run                              ; a5 = slot
        move.l  SL_PC(a5),a4
.op     move.w  (a4)+,d0
        cmp.w   #NOPS,d0
        bhs     .bad
        add.w   d0,d0
        add.w   d0,d0
        lea     op_table,a0
        move.l  (a0,d0.w),a0
        jsr     (a0)                ; -> Z=1: go on, Z=0: wait (a4 saved)
        bne     .stop
        tst.l   SL_PC(a5)           ; (ended / restarted inside)
        beq     .x
        bra     .op
.stop   move.l  a4,SL_PC(a5)
.x      rts
.bad    clr.l   SL_PC(a5)
        rts

GO      macro
        cmp.w   d0,d0
        rts
        endm
WAITFOR macro                       ; \1 = kind, d1 = argument
        move.w  #\1,SL_WAIT(a5)
        move.w  d1,SL_ARG(a5)
        moveq   #1,d0
        rts
        endm

op_table
        dc.l    op_end,op_say,op_saynw,op_walk,op_walknw,op_face,op_put,op_pickup
        dc.l    op_drop,op_setf,op_clrf,op_iff,op_ifnf,op_jmp,op_hide,op_show
        dc.l    op_imgon,op_imgoff,op_room,op_wait,op_sound,op_music,op_dialog,op_cuton
        dc.l    op_cutoff,op_randsay,op_anim,op_animnw,op_card,op_has,op_nothas,op_endgame
        dc.l    op_fade,op_costume,op_ifroom,op_speech,op_cardnw,op_setstate,op_waitkey
        dc.l    op_storyload,op_storydef,op_storysave,op_storyvol
        dc.l    op_randjmp,op_ifhere,op_ifnhere
NOPS    = (*-op_table)/4

op_end  clr.l   SL_PC(a5)
        GO

op_say  bsr     say_common
        WAITFOR W_TEXT
op_saynw
        bsr     say_common
        GO

say_common                          ; (a4) = actor, str -> d1 = text slot
        move.w  (a4)+,d6            ; actor
        move.w  (a4)+,d0            ; string
        bsr     str_ptr             ; a0 = text, d0 = speech
        move.w  d0,d5
        moveq   #0,d1               ; the player's thread uses text slot 0
        tst.w   cur_slot
        beq     .s
        moveq   #1,d1
.s      move.w  d1,-(sp)
        bsr     text_off            ; (its last text)
        move.w  d6,d0
        bsr     act_ptr
        move.w  A_COL(a0),d0
        move.w  d6,d2
        move.w  A_ROOM(a0),d3       ; not here (on the radio): at the top
        cmp.w   cur_room,d3
        beq     .here
        moveq   #-2,d2
.here   move.l  a0,a3
        move.l  txt_src,a0
        move.w  (sp),d1
        bsr     make_text
        move.w  (sp),d1
        lea     texts,a1
        mulu    #T_SIZE,d1
        add.l   d1,a1
        move.l  txt_src,a0          ; time: 2 ticks a letter, at least 2 seconds
        moveq   #0,d0
.ln     tst.b   (a0)+
        beq     .t
        addq.w  #2,d0
        bra     .ln
.t      add.w   #30,d0
        cmp.w   #50,d0
        bhs     .t1
        moveq   #50,d0
.t1     move.w  d0,T_TIME(a1)
        tst.w   d2
        bmi     .nt
        move.w  #1,A_TALKING(a3)
        move.w  #1,A_CNT(a3)
.nt     tst.w   d5                  ; spoken
        beq     .ns
        move.w  d5,d0
        bsr     speech_play
.ns     move.w  (sp)+,d1
        rts

str_ptr                             ; d0 = string -> a0 = text (also txt_src), d0 = speech
        move.l  strings,a0
        lsl.w   #3,d0
        add.w   d0,a0
        move.w  4(a0),d1
        move.l  (a0),a0
        add.l   dat,a0
        move.l  a0,txt_src
        move.w  d1,d0
        rts

text_off                            ; d1 = text slot: its text ends now
        movem.l d0-d1/a0-a1,-(sp)
        lea     texts,a1
        mulu    #T_SIZE,d1
        add.l   d1,a1
        tst.w   T_ON(a1)
        beq     .x
        clr.w   T_ON(a1)
        move.w  T_ACT(a1),d0
        bmi     .x
        bsr     act_ptr
        clr.w   A_TALKING(a0)
.x      movem.l (sp)+,d0-d1/a0-a1
        rts

texts_tick                          ; the texts' time runs out
        moveq   #0,d1
.lp     lea     texts,a1
        move.w  d1,d0
        mulu    #T_SIZE,d0
        add.l   d0,a1
        tst.w   T_ON(a1)
        beq     .nx
        subq.w  #1,T_TIME(a1)
        bgt     .nx
        tst.w   d1                  ; slot 0 waits for its speech too
        bne     .off
        tst.b   speech_on
        beq     .off
        move.w  #1,T_TIME(a1)
        bra     .nx
.off    bsr     text_off
.nx     addq.w  #1,d1
        cmp.w   #2,d1
        blo     .lp
        rts

op_walk move.w  (a4)+,d0
        move.w  (a4)+,d1
        move.w  (a4)+,d2
        move.w  d0,-(sp)
        bsr     walk_actor
        move.w  (sp)+,d1
        WAITFOR W_WALK
op_walknw
        move.w  (a4)+,d0
        move.w  (a4)+,d1
        move.w  (a4)+,d2
        bsr     walk_actor
        GO

op_face move.w  (a4)+,d0
        bsr     act_ptr
        move.w  (a4)+,A_DIR(a0)
        GO

op_put  move.w  (a4)+,d0            ; actor, room, x, y, dir
        bsr     act_ptr
        move.w  (a4)+,A_ROOM(a0)
        move.w  (a4)+,A_X(a0)
        move.w  (a4)+,A_Y(a0)
        move.w  (a4)+,A_DIR(a0)
        clr.w   A_MODE(a0)
        clr.w   A_NPATH(a0)
        GO

op_pickup
        move.w  (a4)+,d0
        lea     obj_state,a0
        bclr    #0,(a0,d0.w)        ; not in the room any more
        btst    #1,(a0,d0.w)        ; its picture goes too
        beq     .n
        bclr    #1,(a0,d0.w)
        move.w  d0,-(sp)
        bsr     redraw_room
        move.w  (sp)+,d0
.n      bsr     inv_add
        moveq   #SND_PICKUP,d0
        bsr     sfx_play
        GO

op_drop move.w  (a4)+,d0
        bsr     inv_remove
        GO

op_setf move.w  (a4)+,d0
        lea     flags,a0
        move.w  d0,d1
        lsr.w   #3,d1
        bset    d0,(a0,d1.w)
        GO
op_clrf move.w  (a4)+,d0
        lea     flags,a0
        move.w  d0,d1
        lsr.w   #3,d1
        bclr    d0,(a0,d1.w)
        GO

test_flag                           ; d0 = flag -> Z=0 if set
        lea     flags,a0
        move.w  d0,d1
        lsr.w   #3,d1
        btst    d0,(a0,d1.w)
        rts

op_iff  move.w  (a4)+,d0
        move.l  (a4)+,d2
        bsr     test_flag
        beq     .no
        bra     jump_d2
.no     GO
op_ifnf move.w  (a4)+,d0
        move.l  (a4)+,d2
        bsr     test_flag
        bne     .no
        bra     jump_d2
.no     GO
op_jmp  move.l  (a4)+,d2
jump_d2 move.l  dat,a4
        add.l   d2,a4
        GO

op_hide move.w  (a4)+,d0
        lea     obj_state,a0
        bclr    #0,(a0,d0.w)
        GO
op_show move.w  (a4)+,d0
        lea     obj_state,a0
        bset    #0,(a0,d0.w)
        GO
op_imgon
        move.w  (a4)+,d0
        lea     obj_state,a0
        bset    #1,(a0,d0.w)
        bsr     redraw_room
        GO
op_imgoff
        move.w  (a4)+,d0
        lea     obj_state,a0
        bclr    #1,(a0,d0.w)
        bsr     redraw_room
        GO
op_setstate                         ; obj, state byte
        move.w  (a4)+,d0
        move.w  (a4)+,d1
        lea     obj_state,a0
        move.b  d1,(a0,d0.w)
        bsr     redraw_room
        GO

op_room move.w  (a4)+,d0            ; room, x, y, dir
        move.w  (a4)+,d1
        move.w  (a4)+,d2
        move.w  (a4)+,d3
        move.l  a4,SL_PC(a5)
        bsr     change_room
        move.l  SL_PC(a5),a4
        GO

op_wait move.w  (a4)+,d1
        WAITFOR W_TICKS

op_sound
        move.w  (a4)+,d0
        bsr     sfx_play
        GO
op_speech
        move.w  (a4)+,d0
        bsr     speech_play
        GO
op_music
        move.w  (a4)+,d0
        move.l  a5,-(sp)            ; (music_play uses a5 for the custom chips)
        bsr     music_play
        move.l  (sp)+,a5
        GO

op_dialog                           ; .w n, n x (.w condition, .w string, .l target)
        move.w  (a4)+,d6
        moveq   #0,d7               ; shown
        lea     dlg_text,a2
        lea     dlg_target,a3
        subq.w  #1,d6
.lp     move.w  (a4)+,d0            ; condition: 0, f (not set), $100+f (set)
        move.w  (a4)+,d4
        move.l  (a4)+,d5
        tst.w   d0
        beq     .show
        btst    #8,d0
        bne     .set
        bsr     test_flag
        bne     .nx
        bra     .show
.set    and.w   #$ff,d0
        bsr     test_flag
        beq     .nx
.show   move.w  d4,d0
        bsr     str_ptr
        move.l  a0,(a2)+
        move.l  dat,d0
        add.l   d5,d0
        move.l  d0,(a3)+
        addq.w  #1,d7
.nx     dbf     d6,.lp
        move.w  d7,dlg_n
        move.w  #-1,dlg_hover
        st      dlg_on
        clr.w   sel_verb
        clr.w   sel_obj1
        bsr     draw_dialog
        moveq   #0,d1
        WAITFOR W_DIALOG

op_cuton
        st      in_cutscene
        st      panel_dark
        clr.b   pointer_on
        st      pal_dirty
        GO
op_cutoff
        clr.b   in_cutscene
        clr.b   skip_cutscene
        clr.b   panel_dark
        st      pointer_on
        st      pal_dirty
        GO

op_randsay                          ; actor, n, strings...
        move.w  (a4),d6
        move.w  2(a4),d1
        bsr     random              ; d0 = 0..d1-1
        move.w  d0,d2
        add.w   d2,d2
        move.w  4(a4,d2.w),d2       ; the string
        move.w  2(a4),d1
        add.w   d1,d1
        lea     4(a4,d1.w),a3       ; after the list
        lea     rs_args,a4
        move.w  d6,(a4)
        move.w  d2,2(a4)
        move.l  a3,-(sp)            ; (say_common uses a3)
        bsr     say_common
        move.l  (sp)+,a4
        WAITFOR W_TEXT

op_anim move.w  (a4)+,d0            ; actor, special, loops
        move.w  (a4)+,d1
        move.w  (a4)+,d2
        move.w  d0,-(sp)
        bsr     start_special
        move.w  (sp)+,d1
        WAITFOR W_ANIM
op_animnw
        move.w  (a4)+,d0
        move.w  (a4)+,d1
        move.w  (a4)+,d2
        bsr     start_special
        GO

op_card bsr     card_common
        WAITFOR W_TEXT
op_cardnw
        bsr     card_common
        GO
card_common
        move.w  (a4)+,d0
        bsr     str_ptr
        move.w  d0,-(sp)            ; spoken?
        moveq   #0,d1
        bsr     text_off
        move.l  txt_src,a0
        moveq   #17,d0              ; white
        moveq   #0,d1
        moveq   #-1,d2              ; in the middle
        bsr     make_text
        lea     texts,a1
        move.l  txt_src,a0
        moveq   #0,d0
.ln     tst.b   (a0)+
        beq     .t
        addq.w  #2,d0
        bra     .ln
.t      add.w   #50,d0
        move.w  d0,T_TIME(a1)
        move.w  (sp)+,d0
        beq     .ns
        bsr     speech_play
.ns     moveq   #0,d1
        rts

op_has  move.w  (a4)+,d0
        move.l  (a4)+,d2
        bsr     has_item
        bne     jump_d2
        GO
op_nothas
        move.w  (a4)+,d0
        move.l  (a4)+,d2
        bsr     has_item
        beq     jump_d2
        GO

op_endgame
        st      game_over
        clr.l   SL_PC(a5)
        GO

op_waitkey
        clr.b   key_hit
        moveq   #0,d1
        WAITFOR W_KEY

op_fade move.w  (a4)+,d0
        bsr     fade_to
        moveq   #0,d1
        WAITFOR W_FADE

op_costume
        move.w  (a4)+,d0
        bsr     act_ptr
        move.l  (a4)+,A_COST(a0)
        GO

op_ifroom
        move.w  (a4)+,d0
        move.l  (a4)+,d2
        cmp.w   cur_room,d0
        beq     jump_d2
        GO

op_randjmp                          ; .w n, n x .l target: one of them, at random
        move.w  (a4)+,d1
        bsr     random
        lsl.w   #2,d0
        move.l  (a4,d0.w),d2
        bra     jump_d2
op_ifhere                           ; .w actor, .l target: if the actor is in this room
        move.w  (a4)+,d0
        move.l  (a4)+,d2
        bsr     act_ptr
        move.w  A_ROOM(a0),d0
        cmp.w   cur_room,d0
        beq     jump_d2
        GO
op_ifnhere
        move.w  (a4)+,d0
        move.l  (a4)+,d2
        bsr     act_ptr
        move.w  A_ROOM(a0),d0
        cmp.w   cur_room,d0
        bne     jump_d2
        GO

random                              ; d1 = n -> d0 = 0..n-1
        move.l  seed,d0
        mulu    #25173,d0
        add.l   #13849,d0
        add.l   frames,d0
        move.l  d0,seed
        swap    d0
        and.l   #$ffff,d0
        divu    d1,d0
        swap    d0
        and.l   #$ffff,d0
        rts

;----------------------------------------------------------------------
;  the story between the chapters: a little file with 128 story flags
;  and 128 story items. storymap (in the data file) says which of this
;  chapter's flags and things they are; flags the chapter doesn't know
;  are kept as they are, for the chapters after it.
;----------------------------------------------------------------------
STORY_SIZE = 4+16+16+4             ; 'WSTY', flags, items, check code

op_storyload                        ; .w 0 (this drawer) / 1 (the last chapter's disk), .w flag (set if it worked)
        move.w  (a4)+,d0
        move.w  (a4)+,d6
        movem.l d6/a4-a5,-(sp)
        bsr     req_off
        move.l  dosbase,a6
        lea     n_story_in,a2
        tst.w   d0
        beq     .one
        lea     n_story_prev,a2     ; a list: try each name
.try    tst.b   (a2)
        beq     .fail
        bsr     .open
        bne     .got
.skip   tst.b   (a2)+
        bne     .skip
        bra     .try
.one    bsr     .open
        beq     .fail
        bra     .got
.open   move.l  a2,d1
        move.l  #MODE_OLDFILE,d2
        jsr     _LVOOpen(a6)
        move.l  d0,d7
        rts
.got
        move.l  d7,d1
        move.l  #story_tmp,d2
        move.l  #STORY_SIZE,d3
        jsr     _LVORead(a6)
        move.l  d0,d5
        move.l  d7,d1
        jsr     _LVOClose(a6)
        cmp.l   #STORY_SIZE,d5
        bne     .fail
        cmp.l   #'WSTY',story_tmp
        bne     .fail
        lea     story_tmp,a0        ; the check code: a story file made or changed by hand is refused
        bsr     story_code
        cmp.l   story_tmp+36,d0
        bne     .fail
        lea     story_tmp,a0
        lea     story_buf,a1
        moveq   #STORY_SIZE-1,d0
.c      move.b  (a0)+,(a1)+
        dbf     d0,.c
        bsr     req_on
        bsr     story_apply
        movem.l (sp)+,d6/a4-a5
        move.w  d6,d0
        bra     set_flag_go
.fail   bsr     req_on
        movem.l (sp)+,d6/a4-a5
        GO

op_storydef                         ; the standard story (no file): from the data file
        movem.l a4-a5,-(sp)
        move.l  story_def,a0
        lea     story_buf,a1
        move.l  #'WSTY',(a1)+
        moveq   #32-1,d0
.c      move.b  (a0)+,(a1)+
        dbf     d0,.c
        bsr     story_apply
        movem.l (sp)+,a4-a5
        GO

op_storysave                        ; .w flag (set if it worked): the story -> the next chapter's file
        move.w  (a4)+,d6
        movem.l d6/a4-a5,-(sp)
        bsr     story_collect
        bsr     req_off
        move.l  dosbase,a6
        move.l  #n_story_out,d1
        move.l  #MODE_NEWFILE,d2
        jsr     _LVOOpen(a6)
        move.l  d0,d7
        beq     .fail
        move.l  d7,d1
        move.l  #story_buf,d2
        move.l  #STORY_SIZE,d3
        jsr     _LVOWrite(a6)
        move.l  d0,d5
        move.l  d7,d1
        jsr     _LVOClose(a6)
        cmp.l   #STORY_SIZE,d5
        bne     .fail
        bsr     req_on
        movem.l (sp)+,d6/a4-a5
        move.w  d6,d0
        bra     set_flag_go
.fail   bsr     req_on
        movem.l (sp)+,d6/a4-a5
        GO

op_storyvol                         ; .w flag: set if this chapter's own disk (or drawer) is there
        move.w  (a4)+,d6
        movem.l d6/a4-a5,-(sp)
        bsr     req_off
        move.l  dosbase,a6
        move.l  #n_vol_self,d1
        moveq   #-2,d2              ; SHARED_LOCK
        jsr     _LVOLock(a6)
        move.l  d0,d1
        beq     .fail
        jsr     _LVOUnLock(a6)
        bsr     req_on
        movem.l (sp)+,d6/a4-a5
        move.w  d6,d0
        bra     set_flag_go
.fail   bsr     req_on
        movem.l (sp)+,d6/a4-a5
        GO

set_flag_go
        lea     flags,a0
        move.w  d0,d1
        lsr.w   #3,d1
        bset    d0,(a0,d1.w)
        GO

req_off                             ; before a DOS call: lend the blitter to the disk (like stream_read),
        movem.l d0-d1/a0-a1/a6,-(sp)   ; or trackdisk waits for it forever (the DOS requesters are off: sys.s)
        bsr     blit_wait
        tst.b   blit_owned
        beq     .x
        move.l  gfxbase,a6
        jsr     _LVODisownBlitter(a6)
.x      movem.l (sp)+,d0-d1/a0-a1/a6
        rts
req_on                              ; after the DOS call: the blitter is ours again
        movem.l d0-d1/a0-a1/a6,-(sp)
        tst.b   blit_owned
        beq     .x
        move.l  gfxbase,a6
        jsr     _LVOOwnBlitter(a6)
        jsr     _LVOWaitBlit(a6)
.x      movem.l (sp)+,d0-d1/a0-a1/a6
        rts

story_apply                         ; story -> this chapter's flags and inventory
        move.l  story_map,a2
.lp     move.w  (a2)+,d2            ; kind (0 flag, 1 thing, -1 end)
        bmi     .x
        move.w  (a2)+,d3            ; story number
        move.w  (a2)+,d4            ; flag / thing here
        lea     story_buf+4,a0
        tst.w   d2
        beq     .t
        lea     story_buf+20,a0
.t      move.w  d3,d1
        lsr.w   #3,d1
        btst    d3,(a0,d1.w)
        beq     .lp
        tst.w   d2
        bne     .item
        lea     flags,a0
        move.w  d4,d1
        lsr.w   #3,d1
        bset    d4,(a0,d1.w)
        bra     .lp
.item   move.w  d4,d0
        bsr     inv_has
        bne     .lp
        move.w  d4,d0
        bsr     inv_add
        bra     .lp
.x      rts

story_collect                       ; this chapter's flags and inventory -> story
        move.l  story_map,a2
.lp     move.w  (a2)+,d2
        bmi     .x
        move.w  (a2)+,d3
        move.w  (a2)+,d4
        tst.w   d2
        bne     .item
        lea     flags,a0
        move.w  d4,d1
        lsr.w   #3,d1
        btst    d4,(a0,d1.w)
        sne     d5
        lea     story_buf+4,a0
        bra     .set
.item   move.w  d4,d0
        bsr     inv_has
        sne     d5
        lea     story_buf+20,a0
.set    move.w  d3,d1
        lsr.w   #3,d1
        bclr    d3,(a0,d1.w)
        tst.b   d5
        beq     .lp
        bset    d3,(a0,d1.w)
        bra     .lp
.x      move.l  #'WSTY',story_buf
        lea     story_buf,a0
        bsr     story_code
        move.l  d0,story_buf+36
        rts

story_code                          ; a0 = story (36 bytes) -> d0 = its check code
        movem.l d1-d2/a0,-(sp)
        move.l  #$5354524B,d0
        moveq   #36-1,d2
.c      rol.l   #5,d0
        moveq   #0,d1
        move.b  (a0)+,d1
        eor.l   d1,d0
        add.l   #$9E3779B9,d0
        dbf     d2,.c
        movem.l (sp)+,d1-d2/a0
        rts

inv_has                             ; d0 = thing -> Z=0 if it is in the inventory
        lea     inv,a0
        move.w  inv_n,d1
        subq.w  #1,d1
        bmi     .no
.f      cmp.w   (a0)+,d0
        beq     .yes
        dbf     d1,.f
.no     moveq   #0,d1
        rts
.yes    moveq   #1,d1
        rts
