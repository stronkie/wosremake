;======================================================================
;  ui.s - the panel under the room: the sentence line, nine verbs, the
;         inventory; pointing at things, clicking, conversations
;======================================================================

PAN_SENT_Y = 3              ; sentence line
VERB_Y     = 18             ; first verb row (rows 15 apart)
INV_X      = 192            ; inventory: 4 x 2 icons of 32 x 24
INV_Y      = 15
INV_DY     = 31
ARROW_X    = 176
MENU_Y     = 66             ; the MENU button under the verbs
PC_SENT    = 6              ; panel colours
PC_VERB    = 4
PC_VERBHI  = 7
PC_DLG     = 4
PC_DLGHI   = 7

;---- drawing into the panel (4 interleaved planes) ----------------------
panel_clear_rect                    ; d0 = x (multiple of 8), d1 = y, d2 = width (bytes), d3 = lines
        movem.l d0-d4/a0-a1,-(sp)
        move.l  p_panel,a0
        lsr.w   #3,d0
        add.w   d0,a0
        mulu    #PANEL_ROW,d1
        add.l   d1,a0
        subq.w  #1,d3
.row    move.l  a0,a1
        moveq   #PANEL_PL-1,d4
.pl     move.w  d2,d1
        subq.w  #1,d1
        move.l  a1,-(sp)
.b      clr.b   (a1)+
        dbf     d1,.b
        move.l  (sp)+,a1
        lea     40(a1),a1
        dbf     d4,.pl
        lea     PANEL_ROW(a0),a0
        dbf     d3,.row
        movem.l (sp)+,d0-d4/a0-a1
        rts

panel_text                          ; a0 = text, d0 = x, d1 = y, d2 = colour -> d0 = x after
        movem.l d1-d7/a0-a3,-(sp)
        move.l  a0,a2
.ch     moveq   #0,d3
        move.b  (a2)+,d3
        beq     .x
        sub.b   #32,d3
        bcs     .ch
        mulu    #9,d3
        move.l  font,a1
        add.w   d3,a1
        moveq   #0,d6
        move.b  (a1)+,d6            ; width
        moveq   #7,d7               ; rows
        move.w  d1,d4
.row    move.b  (a1)+,d3
        move.w  d0,d5
.px     add.b   d3,d3
        bcc     .n
        bsr     panel_pixel         ; d5 = x, d4 = y, d2 = colour
.n      addq.w  #1,d5
        tst.b   d3
        bne     .px
        addq.w  #1,d4
        dbf     d7,.row
        add.w   d6,d0
        addq.w  #1,d0
        bra     .ch
.x      movem.l (sp)+,d1-d7/a0-a3
        rts

panel_pixel                         ; d5 = x, d4 = y, d2 = colour (clipped)
        cmp.w   #319,d5
        bhi     .out
        cmp.w   #PANEL_H-1,d4
        bhi     .out
        movem.l d0-d1/a0,-(sp)
        move.l  p_panel,a0
        move.w  d4,d0
        mulu    #PANEL_ROW,d0
        add.l   d0,a0
        move.w  d5,d0
        lsr.w   #3,d0
        add.w   d0,a0
        move.w  d5,d1
        not.w   d1
        and.w   #7,d1
        btst    #0,d2
        beq     .0
        bset    d1,(a0)
.0      btst    #1,d2
        beq     .1
        bset    d1,40(a0)
.1      btst    #2,d2
        beq     .2
        bset    d1,80(a0)
.2      btst    #3,d2
        beq     .3
        bset    d1,120(a0)
.3      movem.l (sp)+,d0-d1/a0
.out    rts

;---- the verbs ----------------------------------------------------------
verb_rect                           ; d0 = verb 1-9 -> d0 = x, d1 = y (columns of three)
        subq.w  #1,d0
        moveq   #0,d1
        move.w  d0,d1
        divu    #3,d1               ; column = (v-1)/3, row = (v-1) mod 3
        move.w  d1,d2
        swap    d1
        lea     verb_cols,a0
        add.w   d2,d2
        move.w  (a0,d2.w),d0
        mulu    #15,d1
        add.w   #VERB_Y,d1
        rts

draw_verbs
        moveq   #0,d0
        moveq   #12,d1
        moveq   #22,d2              ; 176 pixels
        moveq   #PANEL_H-12,d3
        bsr     panel_clear_rect
        moveq   #1,d7
.lp     move.w  d7,d0
        bsr     verb_rect
        moveq   #PC_VERB,d2
        cmp.w   hover_verb,d7
        bne     .n
        moveq   #PC_VERBHI,d2
.n      move.w  d7,d3
        add.w   d3,d3
        add.w   d3,d3
        move.l  verb_names,a0
        move.l  (a0,d3.w),a0
        add.l   dat,a0
        bsr     panel_text
        addq.w  #1,d7
        cmp.w   #NVERBS,d7
        blo     .lp
        lea     t_menu,a0           ; and MENU under them
        moveq   #8,d0
        moveq   #MENU_Y,d1
        moveq   #PC_SENT,d2
        bra     panel_text

verb_at                             ; mouse in the panel -> d0 = verb 1-9 (0 none)
        move.w  mouse_y,d1
        sub.w   #ROOM_H+1,d1        ; panel y
        move.w  mouse_x,d0
        cmp.w   #ARROW_X-4,d0
        bhs     .no
        sub.w   #VERB_Y-2,d1
        bmi     .no
        ext.l   d1
        divu    #15,d1
        cmp.w   #3,d1
        bhs     .no
        moveq   #0,d2               ; column
        cmp.w   verb_cols+2,d0
        blo     .c
        moveq   #1,d2
        cmp.w   verb_cols+4,d0
        blo     .c
        moveq   #2,d2
.c      mulu    #3,d2               ; verb = column*3 + row + 1
        add.w   d1,d2
        addq.w  #1,d2
        move.w  d2,d0
        rts
.no     moveq   #0,d0
        rts

;---- the inventory ----------------------------------------------------------
draw_inventory
        move.w  #ARROW_X,d0
        moveq   #12,d1
        moveq   #18,d2
        moveq   #PANEL_H-12,d3
        bsr     panel_clear_rect
        moveq   #0,d7               ; slot 0-7
.lp     move.w  inv_top,d0
        add.w   d7,d0
        cmp.w   inv_n,d0
        bhs     .arrows
        add.w   d0,d0
        lea     inv,a0
        move.w  (a0,d0.w),d0
        bsr     obj_ptr
        move.l  O_ICON(a0),d0
        beq     .nx
        move.l  dat,a1
        add.l   d0,a1               ; icon: 24 lines x 4 planes x 4 bytes
        move.w  d7,d0
        bsr     slot_xy             ; -> d0/d1
        move.l  p_panel,a0
        mulu    #PANEL_ROW,d1
        add.l   d1,a0
        lsr.w   #3,d0
        add.w   d0,a0
        moveq   #24*PANEL_PL-1,d2
.row    move.l  (a1)+,(a0)
        lea     40(a0),a0
        dbf     d2,.row
.nx     addq.w  #1,d7
        cmp.w   #8,d7
        blo     .lp
.arrows tst.w   inv_top             ; the scroll arrows
        beq     .a1
        lea     t_up,a0
        move.w  #ARROW_X+3,d0
        moveq   #INV_Y+8,d1
        moveq   #PC_VERB,d2
        bsr     panel_text
.a1     move.w  inv_top,d0
        addq.w  #8,d0
        cmp.w   inv_n,d0
        bhs     .x
        lea     t_down,a0
        move.w  #ARROW_X+3,d0
        moveq   #INV_Y+INV_DY+8,d1
        moveq   #PC_VERB,d2
        bsr     panel_text
.x      rts

slot_xy                             ; d0 = slot 0-7 -> d0 = x, d1 = y
        move.w  d0,d1
        and.w   #3,d0
        lsl.w   #5,d0
        add.w   #INV_X,d0
        lsr.w   #2,d1
        mulu    #INV_DY,d1
        add.w   #INV_Y,d1
        rts

inv_at                              ; mouse -> d0 = object (0 none), d1 = -1/-2 arrows
        moveq   #0,d1
        move.w  mouse_y,d3
        sub.w   #ROOM_H+1,d3
        move.w  mouse_x,d2
        cmp.w   #ARROW_X,d2
        blo     .no
        cmp.w   #INV_X,d2
        bhs     .icons
        moveq   #-1,d1              ; up arrow / down arrow
        cmp.w   #INV_Y+INV_DY-2,d3
        blo     .no
        moveq   #-2,d1
.no     moveq   #0,d0
        rts
.icons  sub.w   #INV_Y,d3
        bmi     .no
        ext.l   d3
        divu    #INV_DY,d3
        cmp.w   #2,d3
        bhs     .no
        sub.w   #INV_X,d2
        lsr.w   #5,d2
        lsl.w   #2,d3
        add.w   d2,d3
        add.w   inv_top,d3
        cmp.w   inv_n,d3
        bhs     .no
        add.w   d3,d3
        lea     inv,a0
        move.w  (a0,d3.w),d0
        rts

inv_add                             ; d0 = object
        lea     inv,a0
        move.w  inv_n,d1
        cmp.w   #MAXINV,d1
        bhs     .x
        add.w   d1,d1
        move.w  d0,(a0,d1.w)
        addq.w  #1,inv_n
        move.w  inv_n,d1            ; show the new one
        subq.w  #1,d1
        and.w   #$fff8,d1
        move.w  d1,inv_top
        st      panel_dirty
.x      rts

inv_remove                          ; d0 = object
        lea     inv,a0
        move.w  inv_n,d1
        subq.w  #1,d1
        bmi     .x
.f      cmp.w   (a0)+,d0
        beq     .got
        dbf     d1,.f
        rts
.got    subq.w  #1,d1
        bmi     .last
.mv     move.w  (a0),-2(a0)
        addq.l  #2,a0
        dbf     d1,.mv
.last   subq.w  #1,inv_n
        move.w  inv_top,d0
        cmp.w   inv_n,d0
        blo     .ok
        clr.w   inv_top
.ok     st      panel_dirty
.x      rts

has_item                            ; d0 = object -> Z=0 if carried
        lea     inv,a0
        move.w  inv_n,d1
        subq.w  #1,d1
        bmi     .no
.f      cmp.w   (a0)+,d0
        beq     .yes
        dbf     d1,.f
.no     cmp.w   d0,d0
        rts
.yes    moveq   #1,d1
        rts

;---- the sentence line ----------------------------------------------------------
build_sentence                      ; -> sentence (text)
        lea     sentence,a1
        move.w  sel_verb,d0
        bne     .v
        tst.w   hover_obj           ; an item in the inventory: Look at
        beq     .v
        cmp.w   #ROOM_H,mouse_y
        blo     .v
        moveq   #V_LOOK,d0
.v      move.w  d0,d1
        add.w   d1,d1
        add.w   d1,d1
        move.l  verb_names,a0
        move.l  (a0,d1.w),a0
        add.l   dat,a0
        bsr     .cpy
        move.w  sel_obj1,d0
        beq     .one
        move.b  #' ',(a1)+
        bsr     .name
        lea     t_with,a0
        cmp.w   #V_GIVE,sel_verb
        bne     .w
        lea     t_to,a0
.w      bsr     .cpy
        move.w  hover_obj,d0
        cmp.w   sel_obj1,d0
        beq     .end
.one    move.w  hover_obj,d0
        beq     .end
        move.b  #' ',(a1)+
        bsr     .name
.end    clr.b   (a1)
        rts
.name   bsr     obj_ptr
        move.l  O_NAME(a0),a0
        add.l   dat,a0
.cpy    move.b  (a0)+,(a1)+
        bne     .cpy
        subq.l  #1,a1
        rts

draw_sentence
        lea     sentence,a0         ; only when it changed
        lea     sentence_shown,a1
.cmp    move.b  (a0)+,d0
        cmp.b   (a1)+,d0
        bne     .draw
        tst.b   d0
        bne     .cmp
        rts
.draw   lea     sentence,a0
        lea     sentence_shown,a1
.cp     move.b  (a0)+,(a1)+
        bne     .cp
        moveq   #0,d0
        moveq   #PAN_SENT_Y-1,d1
        moveq   #40,d2
        moveq   #10,d3
        bsr     panel_clear_rect
        lea     sentence,a0
        bsr     text_width
        move.w  #320,d1
        sub.w   d0,d1
        bpl     .fit
        moveq   #4,d1               ; too long: from the left (cut at the right)
.fit    lsr.w   #1,d1
        move.w  d1,d0
        moveq   #PAN_SENT_Y,d1
        moveq   #PC_SENT,d2
        lea     sentence,a0
        bra     panel_text

;----------------------------------------------------------------------
;  what is under the pointer
;----------------------------------------------------------------------
object_at                           ; -> d0 = object in the room under the pointer (0 none)
        movem.l d2-d7/a2,-(sp)
        move.w  mouse_x,d4
        move.w  mouse_y,d5
        moveq   #0,d6               ; found
        move.l  cur_room_ptr,a2
        move.l  R_OBJS(a2),d0
        beq     .x
        move.l  dat,a2
        add.l   d0,a2
.lp     move.w  (a2)+,d0
        bmi     .x
        lea     obj_state,a0
        btst    #0,(a0,d0.w)        ; ST_HERE
        beq     .lp
        move.w  d0,d7
        bsr     obj_ptr
        move.w  O_ACTOR(a0),d1
        beq     .box
        movem.l d0/a0,-(sp)         ; an actor: the box of its frame
        move.w  d1,d0
        subq.w  #1,d0
        bsr     act_ptr
        move.l  a0,a1
        movem.l (sp)+,d0/a0
        move.w  A_ROOM(a1),d1
        cmp.w   cur_room,d1
        bne     .lp
        move.l  A_COST(a1),a3
        add.l   dat,a3
        move.l  C_FRAMES(a3),a3
        add.l   dat,a3
        move.w  A_X(a1),d0
        sub.w   F_HX(a3),d0
        move.w  A_Y(a1),d1
        sub.w   F_HY(a3),d1
        move.w  F_WW(a3),d2
        subq.w  #1,d2
        lsl.w   #4,d2
        add.w   d0,d2
        move.w  F_H(a3),d3
        add.w   d1,d3
        bra     .test
.box    move.w  O_X0(a0),d0
        move.w  O_Y0(a0),d1
        move.w  O_X1(a0),d2
        move.w  O_Y1(a0),d3
.test   cmp.w   d0,d4
        blt     .lp
        cmp.w   d2,d4
        bgt     .lp
        cmp.w   d1,d5
        blt     .lp
        cmp.w   d3,d5
        bgt     .lp
        move.w  d7,d6               ; (the last one in the list wins)
        bra     .lp
.x      move.w  d6,d0
        movem.l (sp)+,d2-d7/a2
        rts

;----------------------------------------------------------------------
;  one tick of the user interface
;----------------------------------------------------------------------
ui_tick
        tst.b   dlg_on
        bne     dialog_tick
        tst.w   ui_frozen           ; a script runs: only skipping texts
        bne     .frozen
        clr.w   hover_obj           ; what is under the pointer
        move.w  mouse_y,d0
        cmp.w   #ROOM_H,d0
        bhs     .panel
        bsr     object_at
        move.w  d0,hover_obj
        clr.w   new_hverb
        bra     .keys
.panel  bsr     verb_at
        move.w  d0,new_hverb
        bsr     inv_at
        move.w  d0,hover_obj
.keys   move.w  new_hverb,d0        ; highlight of the verbs
        cmp.w   hover_verb,d0
        beq     .hv
        move.w  d0,hover_verb
        bsr     draw_verbs
.hv     tst.w   pend_on             ; walking to do something: show that
        bne     .sent
        bsr     build_sentence
.sent   bsr     draw_sentence
        tst.b   panel_dirty
        beq     .k
        clr.b   panel_dirty
        bsr     draw_inventory
.k      bsr     get_key
        beq     .x
        cmp.w   #$101,d0
        beq     left_click
        cmp.w   #$102,d0
        beq     right_click
        cmp.w   #$54,d0             ; F5
        beq     game_menu
        cmp.w   #$40,d0             ; SPACE: pause
        beq     pause_game
        cmp.w   #$45,d0             ; ESC
        beq     skip_texts
        lea     verb_keys,a0        ; the letters of the verbs
.vk     move.w  (a0)+,d1
        beq     .k
        move.w  (a0)+,d2
        cmp.w   d1,d0
        bne     .vk
        move.w  d2,sel_verb
        clr.w   sel_obj1
        bra     .k
.x      rts
.frozen bsr     get_key
        beq     .x
        st      key_hit
        cmp.w   #$101,d0            ; click / ESC / . : skip the text
        beq     .skip
        cmp.w   #$45,d0
        beq     .esc
        cmp.w   #$38,d0             ; '.'
        beq     .skip
        cmp.w   #$40,d0             ; SPACE skips a text too
        beq     .skip
        cmp.w   #$54,d0             ; F5: the menu
        beq     game_menu
        bra     .frozen
.esc    tst.b   in_cutscene         ; ESC in a cutscene: skip it
        beq     .skip
        st      skip_cutscene
.skip   bra     skip_texts
verb_keys                           ; raw key, verb
        dc.w    $24,V_GIVE,$19,V_PICKUP,$16,V_USE,$18,V_OPEN,$28,V_LOOK
        dc.w    $21,V_PUSH,$33,V_CLOSE,$14,V_TALK,$15,V_PULL,$31,V_PULL,0

skip_texts
        lea     texts,a0
        moveq   #1,d0
.l      tst.w   T_ON(a0)
        beq     .n
        move.w  #1,T_TIME(a0)
.n      lea     T_SIZE(a0),a0
        dbf     d0,.l
        bra     speech_stop

left_click
        move.w  mouse_y,d0
        cmp.w   #ROOM_H,d0
        bhs     .panel
        move.w  hover_obj,d0
        beq     .walk
        move.w  sel_verb,d1
        bra     click_object
.walk   clr.w   sel_obj1            ; walk to the spot
        clr.w   sel_verb
        clr.w   pend_on
        move.w  mouse_x,d1
        move.w  mouse_y,d2
        moveq   #0,d0
        bra     walk_actor
.panel  move.w  mouse_y,d0          ; MENU under the verbs
        cmp.w   #ROOM_H+1+MENU_Y-2,d0
        blo     .pv
        cmp.w   #ARROW_X-4,mouse_x
        bhs     .pv
        bra     game_menu
.pv     move.w  hover_verb,d0
        beq     .inv
        move.w  d0,sel_verb
        clr.w   sel_obj1
        rts
.inv    bsr     inv_at
        tst.w   d1
        bne     .arrow
        tst.w   d0
        beq     .x
        move.w  sel_verb,d1
        bne     click_object
        moveq   #V_LOOK,d1          ; walk to an item: look at it
        bra     click_object
.arrow  cmp.w   #-1,d1
        bne     .down
        tst.w   inv_top
        beq     .x
        subq.w  #4,inv_top
        st      panel_dirty
        rts
.down   move.w  inv_top,d0
        addq.w  #8,d0
        cmp.w   inv_n,d0
        bhs     .x
        addq.w  #4,inv_top
        st      panel_dirty
.x      rts

right_click
        move.w  hover_obj,d0
        beq     .x
        clr.w   sel_obj1
        bsr     obj_ptr
        moveq   #0,d1
        move.b  O_DEFV(a0),d1
        tst.w   O_ROOM(a0)
        bne     .room
        moveq   #V_LOOK,d1          ; an item: look at it
.room   move.w  hover_obj,d0
        bra     click_object
.x      rts

click_object                        ; d0 = object, d1 = verb
        cmp.w   #V_USE,d1           ; use / give: the first thing, then "with"
        beq     .two
        cmp.w   #V_GIVE,d1
        bne     .one
.two    tst.w   sel_obj1
        bne     .second
        bsr     obj_ptr             ; only things you carry can be used with...
        tst.w   O_ROOM(a0)
        bne     .one                ; (a room thing: just use it)
        move.w  d0,sel_obj1
        rts
.second move.w  sel_obj1,d2
        cmp.w   d0,d2
        beq     .self
        exg     d0,d2               ; obj1 = the item, obj2 = the target
        bra     start_action
.self   moveq   #0,d2               ; the same item again: use it on its own (put on the suit)
        clr.w   sel_obj1
        bra     start_action
.one    moveq   #0,d2
        clr.w   sel_obj1
        bra     start_action
.x      rts

;----------------------------------------------------------------------
;  an action: walk to the thing first, then run its script
;----------------------------------------------------------------------
start_action                        ; d0 = object 1, d1 = verb, d2 = object 2
        move.w  d0,pend_obj
        move.w  d1,pend_verb
        move.w  d2,pend_obj2
        move.w  #1,pend_on
        bsr     build_sentence      ; keep the sentence as it is now
        move.w  pend_obj2,d0        ; the thing in the room to walk to
        bne     .w
        move.w  pend_obj,d0
.w      bsr     obj_ptr
        tst.w   O_ROOM(a0)
        beq     .now                ; carried: no walking
        move.w  O_ACTOR(a0),d1
        bne     .act
        move.w  O_WX(a0),d1
        bmi     .now
        move.w  O_WY(a0),d2
        moveq   #0,d0
        bra     walk_actor
.act    subq.w  #1,d1               ; to a person: next to them
        move.w  d1,d0
        bsr     act_ptr
        move.w  A_X(a0),d1
        move.w  A_Y(a0),d2
        sub.w   #30,d1
        movem.w d1-d2,-(sp)
        moveq   #0,d0
        bsr     act_ptr
        movem.w (sp)+,d1-d2
        move.w  A_X(a0),d3
        cmp.w   d1,d3
        blt     .left
        add.w   #60,d1
.left   moveq   #0,d0
        bra     walk_actor
.now    rts

action_tick                         ; arrived? then do it
        tst.w   pend_on
        beq     .x
        moveq   #0,d0
        bsr     act_ptr
        tst.w   A_MODE(a0)
        bne     .x                  ; still walking
        clr.w   pend_on
        move.w  pend_obj2,d0        ; face the thing
        bne     .f
        move.w  pend_obj,d0
.f      bsr     obj_ptr
        tst.w   O_ROOM(a0)
        beq     .run
        move.w  O_ACTOR(a0),d1
        beq     .fd
        move.l  a0,-(sp)            ; a person: face them
        subq.w  #1,d1
        move.w  d1,d0
        bsr     act_ptr
        move.w  A_X(a0),d2
        moveq   #0,d0
        bsr     act_ptr
        moveq   #0,d1
        cmp.w   A_X(a0),d2
        bge     .fr
        moveq   #1,d1
.fr     move.w  d1,A_DIR(a0)
        move.l  (sp)+,a0
        bra     .run
.fd     moveq   #0,d1
        move.b  O_DIR(a0),d1
        cmp.b   #4,d1
        bhs     .run
        move.l  a0,-(sp)
        moveq   #0,d0
        bsr     act_ptr
        move.w  d1,A_DIR(a0)
        move.l  (sp)+,a0
.run    clr.w   sel_obj1
        clr.w   sel_verb
        move.w  pend_obj,d0
        move.w  pend_verb,d1
        move.w  pend_obj2,d2
        bsr     find_handler        ; -> a0 = script (0: none)
        move.l  a0,d0
        bne     .go
        move.w  pend_verb,d1        ; the default answer for this verb
        bsr     default_script
.go     moveq   #0,d0               ; slot 0: the player's action
        bra     run_script
.x      rts

find_handler                        ; d0 = obj, d1 = verb, d2 = obj2 -> a0 = script or 0
        movem.l d3-d4,-(sp)
        bsr     .search
        bne     .x
        tst.w   d2                  ; with two things: the other one's handlers
        beq     .none
        exg     d0,d2
        bsr     .search
        exg     d0,d2
        bne     .x
.none   sub.l   a0,a0
.x      movem.l (sp)+,d3-d4
        rts
.search movem.l d0,-(sp)
        bsr     obj_ptr
        move.l  O_HAND(a0),d3
        beq     .no
        move.l  dat,a0
        add.l   d3,a0
.h      move.b  (a0),d3             ; .b verb, .b -, .w obj2, .l script
        cmp.b   #$ff,d3
        beq     .no
        cmp.b   d1,d3
        bne     .hn
        move.w  2(a0),d4
        cmp.w   d2,d4
        beq     .hit
        cmp.w   #$ffff,d4           ; any other thing
        bne     .hn
        tst.w   d2
        bne     .hit
.hn     addq.l  #8,a0
        bra     .h
.hit    move.l  4(a0),a0
        add.l   dat,a0
        movem.l (sp)+,d0
        moveq   #1,d3               ; Z=0
        rts
.no     movem.l (sp)+,d0
        moveq   #0,d3               ; Z=1
        rts

default_script                      ; d1 = verb -> a0 = a script saying a default line
        lea     default_scripts,a0
        add.w   d1,d1
        add.w   d1,d1
        move.l  (a0,d1.w),a0
        add.l   dat,a0
        rts

;----------------------------------------------------------------------
;  conversations: the choices replace the verbs and the inventory
;----------------------------------------------------------------------
dialog_tick
        move.w  mouse_y,d0          ; which line is pointed at
        sub.w   #ROOM_H+1+12,d0
        moveq   #-1,d1
        tst.w   d0
        bmi     .h
        ext.l   d0
        divu    #11,d0
        cmp.w   dlg_n,d0
        bhs     .h
        move.w  d0,d1
.h      cmp.w   dlg_hover,d1
        beq     .k
        move.w  d1,dlg_hover
        bsr     draw_dialog
.k      bsr     get_key
        beq     .x
        cmp.w   #$101,d0
        beq     .click
        subq.w  #1,d0               ; keys 1-9 pick an answer
        cmp.w   #9,d0
        bhs     .k
        cmp.w   dlg_n,d0
        bhs     .k
        bra     .pick
.click  move.w  dlg_hover,d0
        bmi     .k
.pick
        clr.b   dlg_on
        move.w  d0,dlg_choice
        clr.w   sentence_shown      ; redraw the panel
        st      panel_dirty
        bsr     panel_normal
.x      rts

draw_dialog
        moveq   #0,d0
        moveq   #0,d1
        moveq   #40,d2
        moveq   #PANEL_H,d3
        bsr     panel_clear_rect
        moveq   #0,d7
.lp     cmp.w   dlg_n,d7
        bhs     .x
        move.w  d7,d0
        add.w   d0,d0
        add.w   d0,d0
        lea     dlg_text,a0
        move.l  (a0,d0.w),a0
        moveq   #PC_DLG,d2
        cmp.w   dlg_hover,d7
        bne     .n
        moveq   #PC_DLGHI,d2
.n      moveq   #8,d0
        move.w  d7,d1
        mulu    #11,d1
        add.w   #13,d1
        bsr     panel_text
        addq.w  #1,d7
        bra     .lp
.x      rts

panel_normal                        ; the verbs and the inventory again
        moveq   #0,d0
        moveq   #0,d1
        moveq   #40,d2
        moveq   #PANEL_H,d3
        bsr     panel_clear_rect
        clr.b   sentence_shown
        move.b  #1,sentence_shown   ; (forces a redraw)
        bsr     draw_verbs
        bra     draw_inventory
