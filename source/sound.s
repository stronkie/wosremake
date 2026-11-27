;======================================================================
;  sound.s - music on channels 0-2 (sampled instruments, a small
;            sequencer), effects and speech on channel 3
;
;  SONG   .w tracks, then per track .l offset of its events
;  EVENT  .b note (1-60, 0 rest, $ff: back to the start), .b instrument,
;         .b frames, .b volume (0-64)
;  INSTR  (12 bytes) .l sample (offset in the chip file), .w length (words),
;         .w loop start (words), .w loop length (words, 1: no loop),
;         .w decay (volume/16 per frame)
;  SOUND  (8 bytes) .l packed samples (offset in the data file),
;         .w samples, .w period
;======================================================================

SPEECH_MAX = 30000          ; the decode buffer (chip)

; track (run time), per music channel
TR_PTR   = 0                ; .l next event
TR_START = 4
TR_LEFT  = 8                ; .w frames left
TR_VOL   = 10               ; .w volume * 16
TR_DECAY = 12
TR_LOOP  = 14               ; .l loop start (chip), 18 .w loop length
TR_SET   = 20               ; .b set the loop at the next frame
TR_SIZE  = 22

MUS_LOUD   = 20               ; music volume (of 64), normally and under speech
MUS_SPEECH = 7

sound_init
        lea     CUSTOM,a5
        move.w  #$000f,DMACON(a5)
        move.w  #$00ff,ADKCON(a5)
        lea     AUD0LC(a5),a0
        moveq   #3,d0
.ch     move.l  p_silence,(a0)
        move.w  #1,4(a0)
        move.w  #400,6(a0)
        clr.w   8(a0)
        lea     $10(a0),a0
        dbf     d0,.ch
        clr.b   mus_on
        rts

sound_off
        lea     CUSTOM,a5
        clr.b   mus_on
        clr.w   AUD0VOL(a5)
        clr.w   AUD0VOL+$10(a5)
        clr.w   AUD0VOL+$20(a5)
        clr.w   AUD0VOL+$30(a5)
        move.w  #$000f,DMACON(a5)
        rts

wait_lines                          ; a few raster lines (Paula sees the DMA off)
        movem.l d3-d4,-(sp)
        moveq   #4,d4
.l      move.b  CUSTOM+6,d3
.w      cmp.b   CUSTOM+6,d3
        beq     .w
        dbf     d4,.l
        movem.l (sp)+,d3-d4
        rts

;----------------------------------------------------------------------
;  music
;----------------------------------------------------------------------
music_play                          ; d0 = song number (0 = silence)
        cmp.w   cur_song,d0
        beq     .x
        move.w  d0,cur_song
        clr.b   mus_on
        lea     CUSTOM,a5
        clr.w   AUD0VOL(a5)
        clr.w   AUD0VOL+$10(a5)
        clr.w   AUD0VOL+$20(a5)
        tst.w   d0
        beq     .x
        tst.b   music_off
        bne     .x
        move.l  songs,a0
        subq.w  #1,d0
        add.w   d0,d0
        add.w   d0,d0
        move.l  (a0,d0.w),a0
        add.l   dat,a0
        move.w  (a0)+,d6            ; tracks
        lea     tracks,a1
        moveq   #2,d7
.t      tst.w   d6
        beq     .none
        move.l  (a0)+,d0
        add.l   dat,d0
        move.l  d0,TR_PTR(a1)
        move.l  d0,TR_START(a1)
        move.w  #1,TR_LEFT(a1)
        subq.w  #1,d6
        bra     .n
.none   clr.l   TR_PTR(a1)
.n      clr.w   TR_VOL(a1)
        clr.b   TR_SET(a1)
        lea     TR_SIZE(a1),a1
        dbf     d7,.t
        st      mus_on
.x      rts

music_tick
        tst.b   mus_on
        beq     .x
        lea     tracks,a2
        lea     CUSTOM+AUD0LC,a3
        moveq   #0,d7               ; channel
        moveq   #0,d6               ; channels to start
.t      tst.l   TR_PTR(a2)
        beq     .nx
        tst.b   TR_SET(a2)          ; started last frame: now the loop
        beq     .ns
        clr.b   TR_SET(a2)
        move.l  TR_LOOP(a2),(a3)
        move.w  TR_LOOP+4(a2),4(a3)
.ns     move.w  TR_VOL(a2),d0       ; the volume fades
        sub.w   TR_DECAY(a2),d0
        bpl     .v
        moveq   #0,d0
.v      move.w  d0,TR_VOL(a2)
        lsr.w   #4,d0
        mulu    mus_level,d0
        lsr.w   #6,d0
        move.w  d0,8(a3)
        subq.w  #1,TR_LEFT(a2)
        bgt     .nx
        move.l  TR_PTR(a2),a0
.ev     moveq   #0,d0
        move.b  (a0)+,d0            ; note
        cmp.b   #$ff,d0
        bne     .note
        move.l  TR_START(a2),a0
        bra     .ev
.note   moveq   #0,d1
        move.b  (a0)+,d1            ; instrument
        moveq   #0,d2
        move.b  (a0)+,d2            ; frames
        moveq   #0,d3
        move.b  (a0)+,d3            ; volume
        move.l  a0,TR_PTR(a2)
        move.w  d2,TR_LEFT(a2)
        tst.w   d0
        beq     .nx                 ; a rest: the note goes on fading
        lea     periods,a0
        subq.w  #1,d0
        add.w   d0,d0
        move.w  (a0,d0.w),6(a3)
        move.l  instruments,a0
        mulu    #12,d1
        add.w   d1,a0
        move.l  (a0),d0
        add.l   ins_base,d0         ; (the instruments were copied to chip memory)
        move.l  d0,(a3)
        move.w  4(a0),4(a3)
        moveq   #0,d1
        move.w  6(a0),d1            ; loop start (words)
        add.l   d1,d1
        add.l   d1,d0
        move.l  d0,TR_LOOP(a2)
        move.w  8(a0),TR_LOOP+4(a2)
        cmp.w   #1,8(a0)
        bne     .lo
        move.l  p_silence,TR_LOOP(a2)
.lo     move.w  10(a0),TR_DECAY(a2)
        lsl.w   #4,d3
        move.w  d3,TR_VOL(a2)
        lsr.w   #4,d3
        mulu    mus_level,d3
        lsr.w   #6,d3
        move.w  d3,8(a3)
        st      TR_SET(a2)
        bset    d7,d6
.nx     lea     TR_SIZE(a2),a2
        lea     $10(a3),a3
        addq.w  #1,d7
        cmp.w   #3,d7
        blo     .t
        tst.w   d6                  ; restart the channels with a new note
        beq     .x
        lea     CUSTOM,a5
        move.w  d6,DMACON(a5)
        bsr     wait_lines
        or.w    #$8000,d6
        move.w  d6,DMACON(a5)
.x      rts

;----------------------------------------------------------------------
;  effects and speech (channel 3)
;----------------------------------------------------------------------
sfx_play                            ; d0 = effect (not while somebody speaks)
        tst.b   speech_on
        bne     snd_rts
        tst.w   d0
        beq     snd_rts
        movem.l d0-d4/a0-a1/a5,-(sp)
        bsr     sound_entry
        tst.w   d0
        beq     .no
        bsr     decode_play
.no     movem.l (sp)+,d0-d4/a0-a1/a5
snd_rts rts

speech_play                         ; d0 = sound
        tst.w   d0
        beq     snd_rts
        movem.l d0-d4/a0-a1/a5,-(sp)
        bsr     sound_entry
        tst.w   d0
        beq     .no
        bsr     decode_play
        st      speech_on
.no     movem.l (sp)+,d0-d4/a0-a1/a5
        rts

speech_stop
        clr.b   speech_on
        clr.b   smp_state
        lea     CUSTOM,a5
        clr.w   AUD0VOL+$30(a5)
        move.w  #$0008,DMACON(a5)
        rts

sound_entry                         ; d0 = sound -> a0 = packed, d0 = samples (0: none), d4 = period
        move.l  sounds,a1
        subq.w  #1,d0
        lsl.w   #3,d0
        add.w   d0,a1
        move.w  6(a1),d4
        move.l  (a1),d0
        bpl     .dat
        move.l  a1,-(sp)            ; speech: from the stream file
        move.l  spk_buf,a1
        move.l  #STR_SPK_MAX,d1
        bsr     stream_read
        move.l  (sp)+,a1
        tst.l   d0
        beq     .x
        move.w  4(a1),d0
        rts
.dat    move.l  d0,a0
        add.l   dat,a0
        move.w  4(a1),d0
.x      rts

fib_decode                          ; a0 = data (start value, then 2 samples a byte), a1 = out,
        movem.l d0-d3/a2,-(sp)      ; d0.w = samples (even)
        lea     fib_tab,a2
        move.b  (a0)+,d1
        lsr.w   #1,d0
        subq.w  #1,d0
        bmi     .x
.lp     moveq   #0,d2
        move.b  (a0)+,d2
        move.w  d2,d3
        lsr.w   #4,d3
        add.b   (a2,d3.w),d1
        move.b  d1,(a1)+
        and.w   #15,d2
        add.b   (a2,d2.w),d1
        move.b  d1,(a1)+
        dbf     d0,.lp
.x      movem.l (sp)+,d0-d3/a2
        rts

decode_play                         ; a0 = packed, d0 = samples, d4 = period
        lea     CUSTOM,a5
        move.w  #$0008,DMACON(a5)   ; channel 3 off: its buffer is overwritten now
        clr.b   smp_state
        cmp.w   #SPEECH_MAX,d0
        bls     .ok
        move.w  #SPEECH_MAX,d0
.ok     move.w  d0,d3
        move.l  p_speech,a1
        bsr     fib_decode
        move.l  p_speech,a0
        moveq   #0,d2               ; frames = samples * period / 70938
        move.w  d3,d2
        mulu    d4,d2
        divu    #35469,d2
        lsr.w   #1,d2
        addq.w  #2,d2
        move.w  d3,d0
        lsr.w   #1,d0
        move.w  d4,d1
        clr.w   AUD0VOL+$30(a5)
        bsr     wait_lines
        move.l  a0,AUD0LC+$30(a5)
        move.w  d0,AUD0LEN+$30(a5)
        move.w  d1,AUD0PER+$30(a5)
        move.w  #64,AUD0VOL+$30(a5)
        move.w  d2,smp_frames
        move.b  #2,smp_state
        move.w  #$8008,DMACON(a5)
        rts

sample_tick                         ; after the start, loop on silence; then done
        tst.b   smp_state
        beq     .x
        lea     CUSTOM,a5
        cmp.b   #2,smp_state
        bne     .c
        move.l  p_silence,AUD0LC+$30(a5)
        move.w  #1,AUD0LEN+$30(a5)
        move.b  #1,smp_state
.c      subq.w  #1,smp_frames
        bne     .x
        clr.b   smp_state
        clr.b   speech_on
        clr.w   AUD0VOL+$30(a5)
.x      rts

sound_tick                          ; (vertical blank)
        move.w  mus_loud,d0         ; the music goes quiet while somebody speaks
        tst.b   speech_on
        beq     .l
        cmp.w   #MUS_SPEECH,d0
        bls     .l
        moveq   #MUS_SPEECH,d0
.l      move.w  mus_level,d1
        cmp.w   d0,d1
        beq     .m
        blt     .up
        subq.w  #2,d1
        cmp.w   d0,d1
        bge     .s
        move.w  d0,d1
        bra     .s
.up     addq.w  #1,d1
.s      move.w  d1,mus_level
.m      bsr     music_tick
        bra     sample_tick
