;======================================================================
;  THE WORLD OF STRONKIE II: A LOVE ON STRONKIE
;  A point-and-click adventure for the Amiga 500
;  Created By Mark Stronks - Stronkie Soft
;
;  Assembler : vasm (Motorola syntax)
;              vasmm68k_mot -Fhunkexe -nosym -o WOS2 wos2.s
;  Machine   : Amiga 500 with Kickstart/Workbench 3.1 and an accelerator
;              with fast memory (ACA500 Pro); OCS/ECS, 512 KB chip memory
;  Files     : WOS2 (this program), WOS2.DAT (rooms, scripts, texts,
;              sounds: fast memory), WOS2.GFX (people, objects, the
;              instruments: chip memory)
;
;  Files: wos2.s (start-up, the main loop, rooms, saving), sys.s, gfx.s,
;         actor.s, ui.s, script.s, sound.s, defs.i
;======================================================================

        include "defs.i"
        include "game.i"            ; made by build.py: sound numbers

        section code,code

start   lea     bss_start,a0        ; the variables start at 0
        move.l  #bss_end,d1
        sub.l   a0,d1
        lsr.l   #1,d1
        subq.l  #1,d1
.clr    clr.w   (a0)+
        subq.l  #1,d1
        bpl     .clr
        move.l  sp,stack
        lea     own_stack_end,sp    ; our own 8K stack (a CLI gives only 4000 bytes)
        move.l  4.w,a6
        move.l  a6,execbase
        sub.l   a1,a1
        jsr     _LVOFindTask(a6)
        move.l  d0,mytask
        move.l  d0,a4
        move.l  50(a4),old_trap     ; tc_TrapCode: a crash shows where it happened
        move.l  #trap_code,50(a4)
        tst.l   172(a4)             ; pr_CLI
        bne     .cli
        lea     92(a4),a0           ; started from the Workbench
        jsr     _LVOWaitPort(a6)
        lea     92(a4),a0
        jsr     _LVOGetMsg(a6)
        move.l  d0,wbmsg
.cli    move.l  4.w,a6
        lea     dosname,a1
        jsr     _LVOOldOpenLibrary(a6)
        move.l  d0,dosbase
        beq     exit_wb
        lea     gfxname,a1
        jsr     _LVOOldOpenLibrary(a6)
        move.l  d0,gfxbase
        beq     exit_dos
        move.l  #n_save_digit,save_digit
        cmp.w   #37,20(a6)          ; exec version: Kickstart 2.04 or later (made for 3.1)
        bhs     .ks
        lea     m_needks,a0
        bra     fail_msg
.ks     move.l  #CHIP_TOTAL,d0      ; the screens and buffers (no fast memory needed:
                                    ; rooms and speech are read from disk when needed)
        move.l  #MEMF_CHIP|MEMF_CLEAR,d1
        jsr     _LVOAllocMem(a6)
        move.l  d0,p_chip
        beq     .nomem
        bsr     chip_pointers
        bsr     loading_show        ; the loading screen while the files load
        lea     n_gfx,a0            ; the files
        moveq   #MEMF_ANY,d1
        bsr     load_whole
        move.l  d0,gfx
        move.l  d1,gfx_size
        beq     .nofile
        lea     n_dat,a0
        moveq   #MEMF_ANY,d1
        bsr     load_whole
        move.l  d0,dat
        move.l  d1,dat_size
        beq     .nofile
        move.l  dat,a0
        cmp.l   #'WOS2',(a0)
        bne     .nofile
        move.l  4.w,a6              ; chip: the instruments and the frame cache
        move.l  #INS_AL+FC_SIZE,d0
        move.l  #MEMF_CHIP,d1
        jsr     _LVOAllocMem(a6)
        move.l  d0,p_ins
        beq     .nomem
        move.l  d0,a1
        move.l  gfx,a0
        add.l   #INS_START,a0
        move.l  #INS_AL/4-1,d1
.ins    move.l  (a0)+,(a1)+
        subq.l  #1,d1
        bpl     .ins
        move.l  d0,d1
        sub.l   #INS_START,d1
        move.l  d1,ins_base
        add.l   #INS_AL,d0
        move.l  d0,p_fcache
        bsr     fc_reset
        move.l  4.w,a6              ; the buffers for a room picture and a spoken line
        move.l  #STR_ROOM_MAX+STR_SPK_MAX,d0
        moveq   #MEMF_ANY,d1
        jsr     _LVOAllocMem(a6)
        move.l  d0,room_buf
        beq     .nomem
        add.l   #STR_ROOM_MAX,d0
        move.l  d0,spk_buf
        bsr     stream_open
        tst.l   str_fh
        beq     .nofile
        bsr     data_pointers
        bsr     input_on
        tst.l   d0
        beq     .noinput
        bsr     sound_init
        bsr     video_on
        st      video_is_on
        bsr     vbl_on
        bsr     game
        bsr     sound_off
        bsr     vbl_off
        bsr     video_off
        clr.b   video_is_on
        bsr     input_off
        bra     exit_mem
.noinput
.nofile lea     m_nofile,a0
        tst.b   load_nomem          ; (a file that didn't fit is not missing)
        beq     fail_msg
        bra     .nomem
.nomem  lea     m_nomem,a0
        bsr     mem_report          ; what is free, for the message
fail_msg
        move.l  a0,-(sp)
        bsr     loading_close
        move.l  (sp)+,a0
        bsr     say_cli
exit_mem
        bsr     stream_close
        move.l  4.w,a6
        move.l  p_ins,d0
        beq     .pi
        move.l  d0,a1
        move.l  #INS_AL+FC_SIZE,d0
        jsr     _LVOFreeMem(a6)
.pi     move.l  room_buf,d0
        beq     .rb
        move.l  d0,a1
        move.l  #STR_ROOM_MAX+STR_SPK_MAX,d0
        jsr     _LVOFreeMem(a6)
.rb     move.l  gfx,d0
        beq     .g
        move.l  d0,a1
        move.l  gfx_size,d0
        jsr     _LVOFreeMem(a6)
.g      move.l  dat,d0
        beq     .d
        move.l  d0,a1
        move.l  dat_size,d0
        jsr     _LVOFreeMem(a6)
.d      move.l  p_chip,d0
        beq     .c
        move.l  d0,a1
        move.l  #CHIP_TOTAL,d0
        jsr     _LVOFreeMem(a6)
.c      move.l  gfxbase,a1
        jsr     _LVOCloseLibrary(a6)
exit_dos
        move.l  4.w,a6
        move.l  dosbase,a1
        jsr     _LVOCloseLibrary(a6)
exit_wb move.l  mytask,a0
        move.l  old_trap,50(a0)
        move.l  stack,sp
        move.l  wbmsg,d0
        beq     .x
        move.l  4.w,a6
        jsr     _LVOForbid(a6)
        move.l  wbmsg,a1
        jsr     _LVOReplyMsg(a6)
.x      moveq   #0,d0
        rts

trap_code                           ; supervisor: (sp) = exception number, then the frame
        tst.b   crash_busy          ; a crash while reporting one: the system's own alert
        beq     .first
        move.l  old_trap,-(sp)
        rts
.first  st      crash_busy
        move.l  (sp)+,crash_exc
        cmp.l   #2,crash_exc        ; bus / address error: a longer 68000 frame
        blo     .norm
        cmp.l   #3,crash_exc
        bhi     .norm
        move.l  2(sp),crash_addr
        addq.l  #8,sp
.norm   move.l  2(sp),crash_pc
        move.l  #crash_report,2(sp)
        rte

crash_report                        ; user mode again: put the system back, say where
        lea     own_stack_end,sp
        move.l  crash_pc,d0
        sub.l   #start,d0
        move.l  d0,crash_off
        tst.b   video_is_on
        beq     .nv
        bsr     sound_off
        bsr     vbl_off
        bsr     video_off
        bsr     input_off
        clr.b   video_is_on
.nv     lea     crash_text,a3
        clr.b   (a3)+               ; x (a word, maybe at an odd address)
        move.b  #16,(a3)+
        move.b  #14,(a3)+           ; y
        lea     m_crash1,a0
        bsr     .str
        move.l  crash_exc,d0
        bsr     .hex
        lea     m_crash1b,a0
        bsr     .str
        move.l  crash_addr,d0
        bsr     .hex
        clr.b   (a3)+
        move.b  #1,(a3)+            ; another line
        clr.b   (a3)+
        move.b  #16,(a3)+
        move.b  #28,(a3)+
        lea     m_crash2,a0
        bsr     .str
        move.l  crash_pc,d0
        bsr     .hex
        lea     m_crash2b,a0
        bsr     .str
        move.l  crash_off,d0
        bsr     .hex
        clr.b   (a3)+
        move.b  #1,(a3)+
        clr.b   (a3)+
        move.b  #16,(a3)+
        move.b  #42,(a3)+
        lea     m_crash3,a0
        bsr     .str
        clr.b   (a3)+
        clr.b   (a3)+               ; the last line
        move.l  4.w,a6
        lea     intname,a1
        jsr     _LVOOldOpenLibrary(a6)
        tst.l   d0
        beq     .x
        move.l  d0,a6
        moveq   #0,d0               ; RECOVERY_ALERT
        lea     crash_text,a0
        moveq   #54,d1
        jsr     -90(a6)             ; DisplayAlert
        move.l  a6,a1
        move.l  4.w,a6
        jsr     _LVOCloseLibrary(a6)
.x      bra     exit_mem
.str    move.b  (a0)+,(a3)+         ; a0 = text (0 at the end) -> at a3
        bne     .str
        subq.l  #1,a3
        rts
.hex    moveq   #7,d1               ; d0 -> 8 hex digits at a3
.h1     rol.l   #4,d0
        move.b  d0,d2
        and.b   #15,d2
        add.b   #'0',d2
        cmp.b   #'9',d2
        bls     .h2
        addq.b  #7,d2
.h2     move.b  d2,(a3)+
        dbf     d1,.h1
        rts

strip_progdir                       ; "PROGDIR:name" -> "name" (Kickstart 1.x)
        lea     progdir_names,a2
.n      move.l  (a2)+,d0
        beq     .x
        move.l  d0,a0
        cmp.l   #'PROG',(a0)
        bne     .n
        cmp.l   #'DIR:',4(a0)
        bne     .n
        lea     8(a0),a1
.c      move.b  (a1)+,(a0)+
        bne     .c
        bra     .n
.x      subq.l  #8,save_digit       ; (n_save runs on into its digit)
        rts
progdir_names
        dc.l    n_dat,n_gfx,n_str,n_save,n_story_in,n_story_out,0

mem_report                          ; a0 = message -> a0 = message + the free memory
        movem.l d0-d1/a1-a3/a6,-(sp)
        move.l  a0,a1
        lea     mem_text,a3
.cp     move.b  (a1)+,(a3)+
        bne     .cp
        subq.l  #1,a3
        move.l  4.w,a6
        lea     mem_args,a2
        move.l  #MEMF_CHIP,d1
        jsr     _LVOAvailMem(a6)
        lsr.l   #8,d0
        lsr.l   #2,d0
        move.l  d0,(a2)+
        move.l  #MEMF_CHIP|$20000,d1    ; MEMF_LARGEST
        jsr     _LVOAvailMem(a6)
        lsr.l   #8,d0
        lsr.l   #2,d0
        move.l  d0,(a2)+
        moveq   #MEMF_ANY,d1
        jsr     _LVOAvailMem(a6)
        move.l  d0,d1
        move.l  #MEMF_CHIP,d1
        move.l  d0,-(sp)
        jsr     _LVOAvailMem(a6)
        move.l  (sp)+,d1
        sub.l   d0,d1
        lsr.l   #8,d1
        lsr.l   #2,d1
        move.l  d1,(a2)+
        moveq   #0,d1               ; the chip memory still to get
        tst.l   p_ins
        bne     .g
        move.l  #INS_AL+FC_SIZE,d1
.g      tst.l   p_chip
        bne     .c
        add.l   #CHIP_TOTAL,d1
.c      lsr.l   #8,d1
        lsr.l   #2,d1
        move.l  d1,(a2)+
        lea     m_memfmt,a0
        lea     mem_args,a1
        lea     .put,a2
        jsr     -522(a6)            ; RawDoFmt
        lea     mem_text,a0
        movem.l (sp)+,d0-d1/a1-a3/a6
        rts
.put    move.b  d0,(a3)+
        rts

say_cli                             ; a0 = message: to the CLI, or a window from the Workbench
        movem.l d2-d4/a2,-(sp)
        move.l  a0,a2
        move.l  dosbase,a6
        moveq   #0,d4
        tst.l   wbmsg
        bne     .win
        jsr     _LVOOutput(a6)
        move.l  d0,d1
        bra     .w
.win    move.l  #con_name,d1
        move.l  #MODE_NEWFILE,d2
        jsr     _LVOOpen(a6)
        move.l  d0,d4
        move.l  d0,d1
.w      tst.l   d1
        beq     .x
        move.l  a2,d2
        moveq   #-1,d3
.l      addq.l  #1,d3
        tst.b   (a2)+
        bne     .l
        jsr     _LVOWrite(a6)
        tst.l   d4
        beq     .x
        move.l  #250,d1             ; 5 seconds to read it
        jsr     -198(a6)            ; Delay
        move.l  d4,d1
        jsr     _LVOClose(a6)
.x      movem.l (sp)+,d2-d4/a2
        rts

load_whole                          ; a0 = name, d1 = memory type -> d0 = memory, d1 = size (0: failed)
        movem.l d2-d7/a2,-(sp)      ; a crunched file ('WZX1', size, memory) is unpacked in place
        move.l  d1,d7
        move.l  dosbase,a6
        move.l  a0,d1
        move.l  a0,-(sp)
        move.l  #MODE_OLDFILE,d2
        jsr     _LVOOpen(a6)
        move.l  (sp)+,a0
        move.l  d0,d6
        bne     .open
        lea     8(a0),a0            ; no PROGDIR: (WHDLoad): the current drawer
        move.l  a0,d1
        move.l  #MODE_OLDFILE,d2
        jsr     _LVOOpen(a6)
        move.l  d0,d6
        beq     .fail
.open
        move.l  d6,d1               ; the size: to the end and back
        moveq   #0,d2
        moveq   #1,d3               ; OFFSET_END
        jsr     _LVOSeek(a6)
        move.l  d6,d1
        moveq   #0,d2
        moveq   #-1,d3              ; OFFSET_BEGINNING
        jsr     _LVOSeek(a6)
        move.l  d0,d5               ; (the old position: the end)
        cmp.l   #12,d5
        ble     .close
        move.l  d6,d1               ; the header
        move.l  #zx_head,d2
        moveq   #12,d3
        jsr     _LVORead(a6)
        cmp.l   #12,d0
        bne     .close
        move.l  d5,zx_alloc
        cmp.l   #'WZX1',zx_head
        bne     .plain
        sub.l   #12,d5              ; the packed bytes
        move.l  zx_head+8,zx_alloc  ; the memory it needs
        bra     .mem
.plain  move.l  d6,d1               ; not crunched: from the start
        moveq   #0,d2
        moveq   #-1,d3
        jsr     _LVOSeek(a6)
.mem    move.l  4.w,a6
        move.l  zx_alloc,d0
        move.l  d7,d1
        jsr     _LVOAllocMem(a6)
        move.l  d0,d4
        bne     .gotmem
        st      load_nomem
        bra     .close
.gotmem
        move.l  zx_alloc,d0         ; read into the end of the memory
        sub.l   d5,d0
        bclr    #0,d0               ; (at an even address)
        move.l  d4,a2
        add.l   d0,a2
        move.l  d5,d7
.rd     move.l  dosbase,a6          ; read in pieces: the bar moves
        move.l  d6,d1
        move.l  a2,d2
        move.l  #16384,d3
        cmp.l   d3,d7
        bhs     .big
        move.l  d7,d3
.big    move.l  d3,-(sp)
        jsr     _LVORead(a6)
        move.l  (sp)+,d3
        cmp.l   d3,d0
        bne     .free
        add.l   d3,a2
        add.l   d3,loaded
        bsr     loading_bar
        sub.l   d3,d7
        bne     .rd
        move.l  d6,d1
        jsr     _LVOClose(a6)
        cmp.l   #'WZX1',zx_head
        bne     .done
        move.l  zx_alloc,d0         ; unpack to the start
        sub.l   d5,d0
        bclr    #0,d0               ; (where it was read)
        move.l  d4,a1
        lea     (a1,d0.l),a0
        bsr     unzx
.done   move.l  d4,d0
        move.l  zx_alloc,d1
        movem.l (sp)+,d2-d7/a2
        rts
.free   move.l  4.w,a6
        move.l  d4,a1
        move.l  zx_alloc,d0
        jsr     _LVOFreeMem(a6)
.close  move.l  dosbase,a6
        move.l  d6,d1
        jsr     _LVOClose(a6)
.fail   moveq   #0,d0
        moveq   #0,d1
        movem.l (sp)+,d2-d7/a2
        rts

;----------------------------------------------------------------------
;  the stream file: room pictures and speech, read from disk when needed
;----------------------------------------------------------------------
stream_open
        movem.l d2-d3/a6,-(sp)
        move.l  dosbase,a6
        lea     n_str,a0
        move.l  a0,d1
        move.l  #MODE_OLDFILE,d2
        jsr     _LVOOpen(a6)
        tst.l   d0
        bne     .ok
        lea     n_str+8,a0          ; no PROGDIR: (WHDLoad): the current drawer
        move.l  a0,d1
        move.l  #MODE_OLDFILE,d2
        jsr     _LVOOpen(a6)
.ok     move.l  d0,str_fh
        move.l  #-1,pic_cached
        movem.l (sp)+,d2-d3/a6
        rts

stream_close
        move.l  str_fh,d1
        beq     .x
        move.l  a6,-(sp)
        move.l  dosbase,a6
        jsr     _LVOClose(a6)
        move.l  (sp)+,a6
        clr.l   str_fh
.x      rts

stream_read                         ; d0 = $80000000+offset, a1 = buffer, d1 = its size
        movem.l d2-d7/a2-a6,-(sp)   ; -> d0 = length (0: failed), a0 = the data
        move.l  a1,a2
        move.l  d1,d7
        move.l  d0,d6
        bclr    #31,d6
        tst.l   str_fh
        beq     .fail
        bsr     blit_wait           ; the disk may need the blitter: lend it
        tst.b   blit_owned
        beq     .lent
        move.l  gfxbase,a6
        jsr     _LVODisownBlitter(a6)
.lent   move.l  dosbase,a6
        move.l  str_fh,d1
        move.l  d6,d2
        moveq   #-1,d3              ; OFFSET_BEGINNING
        jsr     _LVOSeek(a6)
        move.l  str_fh,d1
        move.l  #str_len,d2
        moveq   #4,d3
        jsr     _LVORead(a6)
        cmp.l   #4,d0
        bne     .bad
        move.l  str_len,d3
        beq     .bad
        cmp.l   d7,d3
        bhi     .bad
        move.l  str_fh,d1
        move.l  a2,d2
        jsr     _LVORead(a6)
        cmp.l   str_len,d0
        bne     .bad
        move.l  d0,d5
        bra     .back
.bad    moveq   #0,d5
.back   tst.b   blit_owned
        beq     .done
        move.l  gfxbase,a6
        jsr     _LVOOwnBlitter(a6)
        jsr     _LVOWaitBlit(a6)
.done   move.l  d5,d0
        move.l  a2,a0
        movem.l (sp)+,d2-d7/a2-a6
        rts
.fail   moveq   #0,d0
        move.l  a2,a0
        movem.l (sp)+,d2-d7/a2-a6
        rts

;----------------------------------------------------------------------
;  chip memory: one block for the screens, the copper list, the pointer,
;  the texts and the sound buffer
;----------------------------------------------------------------------
C_BUF0    = 0
C_BUF1    = C_BUF0+ROOM_SIZE
C_BG      = C_BUF1+ROOM_SIZE
C_PANEL   = C_BG+ROOM_SIZE
C_COPPER  = C_PANEL+PANEL_SIZE
C_POINTER = C_COPPER+1024
C_NULLSPR = C_POINTER+4+16*4+4
C_SILENCE = C_NULLSPR+8
C_TEXT    = C_SILENCE+8
C_SPEECH  = C_TEXT+2*TXT_BYTES
CHIP_TOTAL = C_SPEECH+SPEECH_MAX+16
INS_AL    = (INS_SIZE+3)&-4

chip_pointers
        move.l  p_chip,d0
        lea     chip_offs,a0
        lea     p_buf0,a1
        moveq   #(chip_offs_end-chip_offs)/4-1,d1
.lp     move.l  (a0)+,d2
        add.l   d0,d2
        move.l  d2,(a1)+
        dbf     d1,.lp
        move.l  p_pointer,a1        ; the pointer: a cross
        addq.l  #4,a1
        lea     pointer_gfx,a0
        moveq   #15,d1
.p      move.l  (a0)+,(a1)+
        dbf     d1,.p
        clr.l   (a1)
        move.l  p_buf0,shown
        move.l  #txt_chunky_buf,txt_chunky
        rts

data_pointers                       ; the tables of the data file
        move.l  dat,a0
        lea     dat_offs,a1
        moveq   #(dat_offs_end-dat_offs)/4-1,d1
        lea     4(a0),a2
.lp     move.l  (a2)+,d0
        add.l   a0,d0
        move.l  (a1)+,a3
        move.l  d0,(a3)
        dbf     d1,.lp
        rts

;----------------------------------------------------------------------
;  the game
;----------------------------------------------------------------------
game    bsr     new_game
        clr.w   fade_level
        st      pal_dirty
        bsr     panel_normal
.main           bsr     wait_tick
        bsr     ui_tick
        bsr     action_tick
        bsr     vm_tick
        tst.b   game_over
        bne     .x
        tst.b   quit_game
        bne     .x
        bsr     actors_tick
        bsr     texts_tick
        bsr     room_events
        tst.w   cur_room
        beq     .main
        bsr     render
        bra     .main
.x      rts

wait_tick                           ; 25 game ticks a second
.w      move.l  frames,d0
        sub.l   last_tick,d0
        cmp.l   #TICK,d0
        blo     .w
        move.l  frames,last_tick
        rts

new_game
        clr.w   cur_room
        lea     flags,a0
        moveq   #31,d0
.f      clr.b   (a0)+
        dbf     d0,.f
        move.l  obj_init,a0         ; the objects' states at the start
        lea     obj_state,a1
        move.w  #255,d0
.o      move.b  (a0)+,(a1)+
        dbf     d0,.o
        clr.w   inv_n
        clr.w   inv_top
        moveq   #0,d7               ; the actors (16 bytes each in the data)
.a      move.w  d7,d0
        bsr     act_ptr
        move.l  a0,a1
        move.w  #A_SIZE/2-1,d1
.ca     clr.w   (a1)+
        dbf     d1,.ca
        move.l  actor_init,a1
        move.w  d7,d1
        lsl.w   #4,d1
        add.w   d1,a1
        move.w  (a1)+,A_ROOM(a0)
        move.w  (a1)+,A_X(a0)
        move.w  (a1)+,A_Y(a0)
        move.w  (a1)+,A_DIR(a0)
        move.l  (a1)+,A_COST(a0)
        move.w  (a1)+,A_COL(a0)
        addq.w  #1,d7
        cmp.w   #MAXACT,d7
        blo     .a
        move.l  fixed_pal,a0        ; colours 16-31 and the panel
        lea     cur_pal+32,a1
        moveq   #15,d0
.c1     move.w  (a0)+,(a1)+
        dbf     d0,.c1
        move.l  panel_pal_src,a0
        lea     panel_pal,a1
        moveq   #15,d0
.c2     move.w  (a0)+,(a1)+
        dbf     d0,.c2
        st      pointer_on
        clr.w   sel_verb
        clr.w   sel_obj1
        clr.w   pend_on
        lea     slots,a0
        moveq   #NSLOTS*SL_SIZE/2-1,d0
.s      clr.w   (a0)+
        dbf     d0,.s
        move.l  start_script,a0     ; the title and the intro
        moveq   #0,d0
        bra     run_script

;----------------------------------------------------------------------
;  rooms
;----------------------------------------------------------------------
obj_ptr                             ; d0 = object -> a0
        move.l  d0,-(sp)
        and.l   #$ffff,d0
        mulu    #O_SIZE,d0
        move.l  objects,a0
        add.l   d0,a0
        move.l  (sp)+,d0
        rts

change_room                         ; d0 = room, d1/d2 = x/y, d3 = direction
        movem.l d0-d7/a0-a6,-(sp)
        movem.w d0-d3,cr_args
        bsr     stop_room_scripts
        moveq   #0,d1
        bsr     text_off
        moveq   #1,d1
        bsr     text_off
        clr.w   pend_on
        tst.w   cur_room
        beq     .dark
        moveq   #0,d0               ; fade out
        bsr     fade_to
        bsr     fade_wait
.dark   movem.w cr_args,d0-d3
        move.w  d0,cur_room
        moveq   #0,d0               ; the player
        bsr     act_ptr
        movem.w cr_args,d0-d3
        move.w  d0,A_ROOM(a0)
        move.w  d1,A_X(a0)
        move.w  d2,A_Y(a0)
        move.w  d3,A_DIR(a0)
        clr.w   A_MODE(a0)
        clr.w   A_NPATH(a0)
        move.w  cur_room,d0
        subq.w  #1,d0
        mulu    #R_SIZE,d0
        move.l  rooms,a0
        add.l   d0,a0
        move.l  a0,cur_room_ptr
        clr.l   walk_mask
        move.l  R_WALK(a0),d0
        beq     .nw
        add.l   dat,d0
        move.l  d0,walk_mask
.nw     bsr     show_room_picture
        move.l  cur_room_ptr,a0
        move.w  R_MUSIC(a0),d0
        beq     .nm
        bsr     music_play
.nm     clr.w   room_ticks
        bsr     set_random_timer
        move.l  cur_room_ptr,a0
        move.l  R_ENTER(a0),d0
        beq     .ne
        add.l   dat,d0
        move.l  d0,a0
        moveq   #3,d0
        bsr     run_script
.ne     bsr     render              ; both screens
        bsr     render
        moveq   #16,d0
        bsr     fade_to
        movem.l (sp)+,d0-d7/a0-a6
        rts

redraw_room                         ; an object picture changed
        movem.l d0-d7/a0-a6,-(sp)
        tst.w   cur_room
        beq     .x
        move.l  cur_room_ptr,a0
        bsr     show_room_picture
.x      movem.l (sp)+,d0-d7/a0-a6
        rts

set_random_timer
        move.l  cur_room_ptr,a0
        clr.w   random_ticks
        move.w  R_RMAX(a0),d1
        beq     .x
        sub.w   R_RMIN(a0),d1
        addq.w  #1,d1
        bsr     random
        move.l  cur_room_ptr,a0
        add.w   R_RMIN(a0),d0
        move.w  d0,random_ticks
.x      rts

room_events                         ; the room's timer and its random event
        tst.w   cur_room
        beq     .x
        tst.b   in_cutscene
        bne     .x
        move.l  cur_room_ptr,a2
        addq.w  #1,room_ticks
        move.w  R_TICKS(a2),d0
        beq     .rnd
        cmp.w   room_ticks,d0
        bne     .rnd
        move.l  R_TIMER(a2),d0
        add.l   dat,d0
        move.l  d0,a0
        moveq   #2,d0
        bsr     run_script
.rnd    tst.w   random_ticks
        beq     .x
        subq.w  #1,random_ticks
        bne     .x
        tst.l   slots+SL_SIZE       ; slot 1 busy: later
        bne     .later
        tst.b   dlg_on              ; not in the middle of a conversation
        bne     .later
        move.l  cur_room_ptr,a2
        move.l  R_RANDOM(a2),d0
        add.l   dat,d0
        move.l  d0,a0
        moveq   #1,d0
        bsr     run_script
        bra     set_random_timer
.later  move.w  #25,random_ticks
.x      rts

;----------------------------------------------------------------------
;  the menu (F5, or MENU in the panel): save, load, music, dev mode, quit
;----------------------------------------------------------------------
MENU_ITEMS = 12

game_menu
        tst.b   dlg_on              ; not in the middle of a conversation
        bne     .x
        move.b  panel_dark,menu_dark
        move.b  pointer_on,menu_ptr
        clr.b   panel_dark
        st      pointer_on
        st      pal_dirty
.again  lea     menu_texts,a2
        lea     m_menu_title,a3
        bsr     menu_draw
.lp     bsr     wait_frame
        bsr     get_key
        beq     .lp
        cmp.w   #$45,d0             ; ESC / F5: back
        beq     .back
        cmp.w   #$54,d0
        beq     .back
        cmp.w   #$101,d0
        bne     .lp
        bsr     menu_item
        tst.w   d0
        bmi     .lp
        cmp.w   #4,d0
        blo     .save
        cmp.w   #8,d0
        blo     .load
        beq     .music
        cmp.w   #9,d0
        beq     .dev
        cmp.w   #10,d0
        beq     .back
        st      quit_game
.back   move.b  menu_ptr,pointer_on
        move.b  menu_dark,panel_dark
        st      pal_dirty
        bra     panel_normal
.x      rts
.save   tst.b   in_cutscene         ; (not in a cutscene: it would not come back)
        bne     .lp
        bsr     save_game
        bra     .back
.load   subq.w  #4,d0
        clr.b   menu_dark
        st      menu_ptr
        bsr     load_game
        bra     .back
.music  move.w  music_lvl,d0        ; High, Medium, Low, Off
        addq.w  #1,d0
        and.w   #3,d0
        move.w  d0,music_lvl
        add.w   d0,d0
        lea     music_levels,a0
        move.w  (a0,d0.w),mus_loud
        cmp.w   #3,music_lvl
        beq     .moff
        tst.b   music_off
        beq     .again
        clr.b   music_off           ; back on: the song again
        move.w  saved_song,d0
        clr.w   cur_song
        bsr     music_play
        bra     .again
.moff   st      music_off
        move.w  cur_song,saved_song
        moveq   #0,d0
        bsr     music_play
        bra     .again
.dev    bsr     dev_menu
        bra     .back

menu_draw                           ; a2 = item texts, a3 = title
        moveq   #0,d0
        moveq   #0,d1
        moveq   #40,d2
        moveq   #PANEL_H,d3
        bsr     panel_clear_rect
        move.l  a3,a0
        moveq   #8,d0
        moveq   #3,d1
        moveq   #PC_SENT,d2
        bsr     panel_text
        moveq   #0,d7
.dl     move.w  d7,d0
        bsr     menu_pos
        movem.w d0-d1,-(sp)
        move.w  d7,d0
        add.w   d0,d0
        add.w   d0,d0
        move.l  (a2,d0.w),a0
        move.l  a0,d0               ; (an empty place)
        bne     .h
        addq.l  #4,sp
        bra     .nx
.h      cmp.l   #mt8,a0             ; the music item shows its level
        bne     .t
        move.w  music_lvl,d0
        add.w   d0,d0
        add.w   d0,d0
        lea     music_texts,a0
        move.l  (a0,d0.w),a0
.t      movem.w (sp)+,d0-d1
        moveq   #PC_VERB,d2
        bsr     panel_text
.nx     addq.w  #1,d7
        cmp.w   #MENU_ITEMS,d7
        blo     .dl
        rts

menu_pos                            ; item -> d0 = x, d1 = y (4 columns, 3 rows)
        move.w  d0,d1
        and.w   #3,d0
        mulu    #78,d0
        addq.w  #8,d0
        lsr.w   #2,d1
        mulu    #18,d1
        add.w   #20,d1
        rts

menu_item                           ; -> d0 = item under the pointer (-1 none)
        move.w  mouse_y,d1
        sub.w   #ROOM_H+1+18,d1
        bmi     .no
        ext.l   d1
        divu    #18,d1
        cmp.w   #3,d1
        bhs     .no
        move.w  mouse_x,d0
        subq.w  #8,d0
        bmi     .no
        ext.l   d0
        divu    #78,d0
        cmp.w   #4,d0
        bhs     .no
        lsl.w   #2,d1
        add.w   d1,d0
        cmp.w   #MENU_ITEMS,d0
        bhs     .no
        rts
.no     moveq   #-1,d0
        rts

dev_menu                            ; dev mode: go to any room, get every item
        lea     dev_texts,a2
        lea     m_dev_title,a3
        bsr     menu_draw
.lp     bsr     wait_frame
        bsr     get_key
        beq     .lp
        cmp.w   #$45,d0
        beq     .x
        cmp.w   #$54,d0
        beq     .x
        cmp.w   #$101,d0
        bne     .lp
        bsr     menu_item
        tst.w   d0
        bmi     .lp
        cmp.w   #DEV_ROOMS,d0
        blo     .room
        cmp.w   #DEV_ROOMS,d0
        bne     .x
        lea     dev_items,a2        ; every item
.it     move.w  (a2)+,d0
        beq     .x
        bsr     has_item
        bne     .it
        bsr     inv_add
        bra     .it
.room   mulu    #6,d0
        lea     dev_rooms,a0
        add.w   d0,a0
        lea     slots,a1            ; nothing runs
        moveq   #NSLOTS*SL_SIZE/2-1,d1
.s      clr.w   (a1)+
        dbf     d1,.s
        clr.b   in_cutscene
        clr.b   menu_dark
        st      menu_ptr
        move.w  (a0)+,d0
        move.w  (a0)+,d1
        move.w  (a0)+,d2
        moveq   #2,d3
        bsr     change_room
.x      st      panel_dirty
        rts

pause_game
        lea     m_paused,a0
        lea     sentence,a1
.c      move.b  (a0)+,(a1)+
        bne     .c
        bsr     draw_sentence
.w      bsr     wait_frame
        bsr     get_key
        beq     .w
        rts

SAVE_SIZE = 2+2+32+256+2+2*MAXINV+MAXACT*12+2

save_name                           ; d0 = slot 0-3 -> d1 = name
        lea     n_save,a0
        add.b   #'1',d0
        move.l  save_digit,a1
        move.b  d0,(a1)
        move.l  a0,d1
        rts

save_game                           ; d0 = slot 0-3
        bsr     save_name
        move.l  d1,-(sp)
        lea     save_buf,a1         ; the state
        move.w  #$5732,(a1)+        ; "W2"
        moveq   #0,d0
        bsr     act_ptr             ; the player's room
        move.w  A_ROOM(a0),(a1)+
        lea     flags,a0
        moveq   #31,d0
.f      move.b  (a0)+,(a1)+
        dbf     d0,.f
        lea     obj_state,a0
        move.w  #255,d0
.o      move.b  (a0)+,(a1)+
        dbf     d0,.o
        move.w  inv_n,(a1)+
        lea     inv,a0
        moveq   #MAXINV-1,d0
.i      move.w  (a0)+,(a1)+
        dbf     d0,.i
        moveq   #0,d7
.a      move.w  d7,d0
        bsr     act_ptr
        move.w  A_ROOM(a0),(a1)+
        move.w  A_X(a0),(a1)+
        move.w  A_Y(a0),(a1)+
        move.w  A_DIR(a0),(a1)+
        move.l  A_COST(a0),(a1)+
        addq.w  #1,d7
        cmp.w   #MAXACT,d7
        blo     .a
        move.w  cur_song,(a1)+
        move.l  (sp)+,d1
        move.l  dosbase,a6
        move.l  #MODE_NEWFILE,d2
        jsr     _LVOOpen(a6)
        move.l  d0,d7
        beq     .err
        move.l  d7,d1
        move.l  #save_buf,d2
        move.l  #SAVE_SIZE,d3
        jsr     _LVOWrite(a6)
        move.l  d0,d6
        move.l  d7,d1
        jsr     _LVOClose(a6)
        cmp.l   #SAVE_SIZE,d6
        bne     .err
        lea     m_saved,a0
        bra     say_now
.err    lea     m_saveerr,a0
        bra     say_now

load_game                           ; d0 = slot 0-3
        bsr     save_name
        move.l  dosbase,a6
        move.l  #MODE_OLDFILE,d2
        jsr     _LVOOpen(a6)
        move.l  d0,d7
        beq     .err
        move.l  d7,d1
        move.l  #save_buf,d2
        move.l  #SAVE_SIZE,d3
        jsr     _LVORead(a6)
        move.l  d0,d6
        move.l  d7,d1
        jsr     _LVOClose(a6)
        cmp.l   #SAVE_SIZE,d6
        bne     .err
        lea     save_buf,a1
        cmp.w   #$5732,(a1)+
        bne     .err
        move.w  (a1)+,d5            ; the room
        beq     .err
        lea     flags,a0
        moveq   #31,d0
.f      move.b  (a1)+,(a0)+
        dbf     d0,.f
        lea     obj_state,a0
        move.w  #255,d0
.o      move.b  (a1)+,(a0)+
        dbf     d0,.o
        move.w  (a1)+,inv_n
        lea     inv,a0
        moveq   #MAXINV-1,d0
.i      move.w  (a1)+,(a0)+
        dbf     d0,.i
        clr.w   inv_top
        moveq   #0,d7
.a      move.w  d7,d0
        bsr     act_ptr
        move.w  (a1)+,A_ROOM(a0)
        move.w  (a1)+,A_X(a0)
        move.w  (a1)+,A_Y(a0)
        move.w  (a1)+,A_DIR(a0)
        move.l  (a1)+,A_COST(a0)
        clr.w   A_MODE(a0)
        clr.w   A_TALKING(a0)
        addq.w  #1,d7
        cmp.w   #MAXACT,d7
        blo     .a
        move.w  (a1)+,d4            ; the song
        lea     slots,a0            ; nothing runs
        moveq   #NSLOTS*SL_SIZE/2-1,d0
.s      clr.w   (a0)+
        dbf     d0,.s
        clr.b   in_cutscene
        clr.b   panel_dark
        st      pointer_on
        clr.w   cur_song
        moveq   #0,d0
        bsr     act_ptr
        move.w  d5,d0
        move.w  A_X(a0),d1
        move.w  A_Y(a0),d2
        move.w  A_DIR(a0),d3
        bsr     change_room
        move.w  d4,d0
        bsr     music_play
        st      panel_dirty
        rts
.err    lea     m_loaderr,a0

say_now                             ; a0 = text: the player says it (no script)
        move.l  a0,txt_src
        moveq   #0,d0
        bsr     act_ptr
        move.w  A_COL(a0),d0
        moveq   #0,d1
        moveq   #0,d2
        move.w  A_ROOM(a0),d3
        cmp.w   cur_room,d3
        beq     .h
        moveq   #-2,d2
.h      move.l  txt_src,a0
        bsr     make_text
        move.w  #75,texts+T_TIME
        rts

;----------------------------------------------------------------------
unzx                                ; a0 = packed -> a1
        movem.l d2-d3/d7/a2,-(sp)
        move.b  #$80,d7
.lp     add.b   d7,d7               ; next bit
        bne     .b1
        move.b  (a0)+,d7
        addx.b  d7,d7
.b1     bcs     .match
        move.b  (a0)+,(a1)+         ; 0: a literal byte
        bra     .lp
.match  bsr     .gamma              ; 1: offset high byte + 1 (128 = end)
        cmp.w   #128,d0
        beq     .end
        subq.w  #1,d0
        lsl.w   #8,d0
        move.b  (a0)+,d0
        addq.w  #1,d0               ; offset = hi*256 + lo + 1
        move.l  a1,a2
        sub.l   d0,a2
        bsr     .gamma              ; length - 1
.cp     move.b  (a2)+,(a1)+
        dbf     d0,.cp
        bra     .lp
.end    movem.l (sp)+,d2-d3/d7/a2
        rts
.gamma  moveq   #1,d0
.g1     add.b   d7,d7
        bne     .g2
        move.b  (a0)+,d7
        addx.b  d7,d7
.g2     bcs     .g3
        add.b   d7,d7
        bne     .g4
        move.b  (a0)+,d7
        addx.b  d7,d7
.g4     addx.w  d0,d0
        bra     .g1
.g3     rts

        include "sys.s"
        include "gfx.s"
        include "actor.s"
        include "ui.s"
        include "script.s"
        include "sound.s"

;======================================================================
        section data,data
chip_offs
        dc.l    C_BUF0,C_BUF1,C_BG,C_PANEL,C_COPPER,C_POINTER,C_NULLSPR,C_SILENCE,C_TEXT,C_SPEECH
chip_offs_end
dat_offs
        dc.l    rooms,objects,actor_init,strings,songs,instruments,sounds,font
        dc.l    verb_names,default_scripts,start_script,obj_init,panel_pal_src,fixed_pal
        dc.l    story_map,story_def
dat_offs_end

pointer_gfx                         ; 16 lines: plane 0 (white), plane 1 (black edge)
        dc.w    $0100,$0280,$0100,$0280,$0100,$0280,$0100,$0280
        dc.w    $0100,$0280,$0000,$0380,$0000,$ffff,$f93e,$06c1
        dc.w    $0000,$ffff,$0000,$0380,$0100,$0280,$0100,$0280
        dc.w    $0100,$0280,$0100,$0280,$0100,$0280,$0000,$0000

verb_cols dc.w  8,60,116
pf_dirs dc.w    1,0,-1,0,0,1,0,-1,1,1,-1,1,1,-1,-1,-1
periods                             ; 60 notes (ProTracker: C-1 856 ... B-3 113), 5 octaves
        dc.w    1712,1616,1525,1440,1357,1281,1209,1141,1077,1017,961,907
        dc.w    856,808,762,720,678,640,604,570,538,508,480,453
        dc.w    428,404,381,360,339,320,302,285,269,254,240,226
        dc.w    214,202,190,180,170,160,151,143,135,127,120,113
        dc.w    107,101,95,90,85,80,76,71,67,64,60,57
fib_tab dc.b    -34,-21,-13,-8,-5,-3,-2,-1,0,1,2,3,5,8,13,21

dosname dc.b    "dos.library",0
gfxname dc.b    "graphics.library",0
inputname dc.b  "input.device",0
        include "names.i"
        even
loadpal incbin  "loadpal.bin"
barstrip
        incbin  "barstrip.bin"
loadpic incbin  "loadpic.zx"
        even
        include "story.i"
        include "files.i"
        include "stream.i"
n_save_digit dc.b "1",0
con_name dc.b   "CON:40/40/560/90/World of Stronkie remake",0
m_crash1 dc.b   "World of Stronkie remake stopped: exception $",0
m_crash1b dc.b  ", address $",0
m_crash2 dc.b   "PC $",0
m_crash2b dc.b  "  game+$",0
m_crash3 dc.b   "Please send Mark a photo of this. Click the mouse to go back.",0
intname  dc.b   "intuition.library",0
        even
m_needks dc.b   10,"World of Stronkie remake needs Kickstart / Workbench 3.1.",10,0
m_memfmt dc.b   "Free now: %ldK chip memory (largest block %ldK), %ldK other memory.",10
        dc.b    "Still needed: %ldK more chip memory.",10,0
m_nomem dc.b    10,"World of Stronkie remake: not enough memory free.",10
        dc.b    "It needs 512K chip + 512K trapdoor memory. Boot from the game disk,",10
        dc.b    "or close some Workbench windows and try again.",10,0
        include "nofile.i"
        dc.b    "(start the game from its own drawer or disk).",10,0
m_menu_title dc.b "MENU   (F5 or ESC: back to the game)",0
m_paused dc.b   "Game paused. Press any key.",0
m_saved dc.b    "Game saved.",0
m_saveerr dc.b  "I couldn't save the game. Is the disk write-protected?",0
m_loaderr dc.b  "There is no saved game there.",0
t_with  dc.b    " with",0
t_to    dc.b    " to",0
t_menu  dc.b    "MENU",0
t_up    dc.b    "^",0
t_down  dc.b    "v",0
mt0     dc.b    "Save 1",0
mt1     dc.b    "Save 2",0
mt2     dc.b    "Save 3",0
mt3     dc.b    "Save 4",0
mt4     dc.b    "Load 1",0
mt5     dc.b    "Load 2",0
mt6     dc.b    "Load 3",0
mt7     dc.b    "Load 4",0
mt8     dc.b    "Music",0
mt8a    dc.b    "Music: high",0
mt8b    dc.b    "Music: medium",0
mt8c    dc.b    "Music: low",0
mt8d    dc.b    "Music: off",0
mt11    dc.b    "Dev mode",0
mt9     dc.b    "Resume",0
mt10    dc.b    "Quit",0
        even
        even
menu_texts dc.l mt0,mt1,mt2,mt3,mt4,mt5,mt6,mt7,mt8,mt11,mt9,mt10
music_texts dc.l mt8a,mt8b,mt8c,mt8d
music_levels dc.w 40,26,14,0
m_dev_title dc.b "DEV MODE: click a room to go there",0
        even
        include "dev.i"

mus_volume dc.w 64
mus_level  dc.w 26
mus_loud   dc.w 26
music_lvl  dc.w 1

;======================================================================
        section bss,bss
bss_start
stack           ds.l    1
own_stack       ds.b    8192
own_stack_end
execbase        ds.l    1
dosbase         ds.l    1
gfxbase         ds.l    1
mytask          ds.l    1
wbmsg           ds.l    1
old_view        ds.l    1
old_winptr      ds.l    1
old_dma         ds.w    1
p_chip          ds.l    1
p_buf0          ds.l    1           ; (the order of chip_offs)
p_buf1          ds.l    1
p_bg            ds.l    1
p_panel         ds.l    1
p_copper        ds.l    1
p_pointer       ds.l    1
p_nullspr       ds.l    1
p_silence       ds.l    1
p_textbuf       ds.l    1
p_speech        ds.l    1
p_cop_planes    ds.l    1
p_cop_room_pal  ds.l    1
p_cop_panel_pal ds.l    1
dat             ds.l    1
dat_size        ds.l    1
gfx             ds.l    1
gfx_size        ds.l    1
rooms           ds.l    1           ; (the order of dat_offs)
objects         ds.l    1
actor_init      ds.l    1
strings         ds.l    1
songs           ds.l    1
instruments     ds.l    1
sounds          ds.l    1
font            ds.l    1
verb_names      ds.l    1
default_scripts ds.l    1
start_script    ds.l    1
obj_init        ds.l    1
panel_pal_src   ds.l    1
fixed_pal       ds.l    1
frames          ds.l    1
zx_head         ds.l    3
zx_alloc        ds.l    1
room_buf        ds.l    1
old_trap        ds.l    1
crash_exc       ds.l    1                   ; these four in this order
crash_addr      ds.l    1
crash_pc        ds.l    1
crash_off       ds.l    1
crash_text      ds.b    300
crash_busy      ds.b    1
                even
save_digit      ds.l    1
p_ins           ds.l    1
ins_base        ds.l    1
p_fcache        ds.l    1
fc_head         ds.l    1
fc_tab          ds.l    3*64
fc_next         ds.w    1
                even
spk_buf         ds.l    1
str_fh          ds.l    1
str_len         ds.l    1
pic_cached      ds.l    1
mem_args        ds.l    4
mem_text        ds.b    600
load_nomem      ds.b    1
                even
last_tick       ds.l    1
seed            ds.l    1
swap_to         ds.l    1
shown           ds.l    1
cur_room_ptr    ds.l    1
walk_mask       ds.l    1
txt_chunky      ds.l    1
txt_src         ds.l    1
vbl_int         ds.b    22
in_port         ds.b    34
in_req          ds.b    48
in_int          ds.b    22
        even
key_buf         ds.w    32
key_r           ds.w    1
key_w           ds.w    1
mouse_x         ds.w    1
mouse_y         ds.w    1
cur_room        ds.w    1
cr_args         ds.w    4
room_ticks      ds.w    1
random_ticks    ds.w    1
fade_level      ds.w    1
fade_target     ds.w    1
cur_pal         ds.w    32
panel_pal       ds.w    16
ndirty0         ds.w    1
ndirty1         ds.w    1
dirty0          ds.w    4*MAXDIRTY
dirty1          ds.w    4*MAXDIRTY
draw_list       ds.w    MAXACT+1
actors          ds.b    A_SIZE*MAXACT
texts           ds.b    T_SIZE*2
txt_lines       ds.l    2*TXT_MAXL+2
txt_col         ds.w    1
txt_act         ds.w    1
txt_nlines      ds.w    1
txt_w           ds.w    1
txt_h           ds.w    1
txt_rows        ds.w    1
loaded          ds.l    1
video_is_on     ds.b    1
        even
load_on         ds.b    1
blit_owned      ds.b    1
        even
bob_rect        ds.w    2
txt_words       ds.w    1
pf_tx           ds.w    1
pf_ty           ds.w    1
pf_sx           ds.w    1
pf_sy           ds.w    1
pf_x            ds.w    1
pf_y            ds.w    1
pf_from         ds.w    WALK_W*WALK_H
pf_queue        ds.w    WALK_W*WALK_H
inv             ds.w    MAXINV
inv_n           ds.w    1
inv_top         ds.w    1
sel_verb        ds.w    1
sel_obj1        ds.w    1
hover_obj       ds.w    1
hover_verb      ds.w    1
new_hverb       ds.w    1
pend_on         ds.w    1
pend_obj        ds.w    1
pend_verb       ds.w    1
pend_obj2       ds.w    1
ui_frozen       ds.w    1
cur_slot        ds.w    1
slots           ds.b    SL_SIZE*NSLOTS
dlg_n           ds.w    1
dlg_hover       ds.w    1
dlg_choice      ds.w    1
dlg_text        ds.l    8
dlg_target      ds.l    8
rs_args         ds.w    2
cur_song        ds.w    1
saved_song      ds.w    1
smp_frames      ds.w    1
tracks          ds.b    TR_SIZE*3
flags           ds.b    32
story_buf       ds.b    STORY_SIZE
story_tmp       ds.b    STORY_SIZE
        even
story_map       ds.l    1
story_def       ds.l    1
obj_state       ds.b    256
sentence        ds.b    120
sentence_shown  ds.b    120
save_buf        ds.b    SAVE_SIZE+2
pointer_on      ds.b    1
pal_dirty       ds.b    1
panel_dark      ds.b    1
panel_dirty     ds.b    1
in_cutscene     ds.b    1
menu_dark       ds.b    1
menu_ptr        ds.b    1
skip_cutscene   ds.b    1
dlg_on          ds.b    1
game_over       ds.b    1
quit_game       ds.b    1
swapped         ds.b    1
mus_on          ds.b    1
music_off       ds.b    1
speech_on       ds.b    1
smp_state       ds.b    1
key_hit         ds.b    1
        even
txt_chunky_buf  ds.b    320*TXT_H
bss_end
