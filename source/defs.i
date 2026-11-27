;======================================================================
;  defs.i - hardware registers, library offsets, engine constants
;======================================================================

; ---- exec / dos / graphics -------------------------------------------
_LVOForbid        = -132
_LVOPermit        = -138
_LVOAllocMem      = -198
_LVOAvailMem      = -216
_LVOFreeMem       = -210
_LVOFindTask      = -294
_LVOAddIntServer  = -168
_LVORemIntServer  = -174
_LVOGetMsg        = -372
_LVOReplyMsg      = -378
_LVOWaitPort      = -384
_LVOOldOpenLibrary = -408
_LVOCloseLibrary  = -414
_LVOOpenScreenTagList = -612
_LVOCloseScreen   = -66
_LVOLoadRGB4      = -192
_LVOAllocSignal   = -330
_LVOFreeSignal    = -336
_LVOOpenDevice    = -444
_LVOCloseDevice   = -450
_LVODoIO          = -456
_LVOOpen          = -30
_LVOClose         = -36
_LVORead          = -42
_LVOWrite         = -48
_LVOLock          = -84
_LVOUnLock        = -90
_LVOOutput        = -60
_LVOSeek          = -66
_LVOLoadView      = -222
_LVOWaitBlit      = -228
_LVOWaitTOF       = -270
_LVOOwnBlitter    = -456
_LVODisownBlitter = -462

MEMF_ANY    = 0
MEMF_CHIP   = 2
MEMF_FAST   = 4
MEMF_CLEAR  = $10000
MODE_OLDFILE = 1005
MODE_NEWFILE = 1006
INTB_VERTB  = 5

; ---- custom chips ------------------------------------------------------
CUSTOM   = $dff000
DMACONR  = $002
VPOSR    = $004
VHPOSR   = $006
JOY0DAT  = $00a
POTGOR   = $016
INTENAR  = $01c
BLTCON0  = $040
BLTCON1  = $042
BLTAFWM  = $044
BLTALWM  = $046
BLTCPT   = $048
BLTBPT   = $04c
BLTAPT   = $050
BLTDPT   = $054
BLTSIZE  = $058
BLTCMOD  = $060
BLTBMOD  = $062
BLTAMOD  = $064
BLTDMOD  = $066
BLTADAT  = $074
COP1LC   = $080
COP2LC   = $084
COPJMP1  = $088
DIWSTRT  = $08e
DIWSTOP  = $090
DDFSTRT  = $092
DDFSTOP  = $094
DMACON   = $096
INTENA   = $09a
ADKCON   = $09e
AUD0LC   = $0a0
AUD0LEN  = $0a4
AUD0PER  = $0a6
AUD0VOL  = $0a8
BPL1PT   = $0e0
BPLCON0  = $100
BPLCON1  = $102
BPLCON2  = $104
BPL1MOD  = $108
BPL2MOD  = $10a
SPR0PT   = $120
COLOR00  = $180

; ---- the screen ----------------------------------------------------------
SCR_W     = 320
ROOM_H    = 168             ; room lines
ROOM_PL   = 5               ; 32 colours (0-15 the room, 16-31 everybody)
ROOM_ROW  = 40*ROOM_PL      ; interleaved: bytes from one line to the next
ROOM_SIZE = ROOM_ROW*ROOM_H
PANEL_H   = 80
PANEL_PL  = 4
PANEL_ROW = 40*PANEL_PL
PANEL_SIZE = PANEL_ROW*PANEL_H
TOP_LINE  = $2c
PANEL_LINE = TOP_LINE+ROOM_H+1  ; one black line between room and panel

; ---- engine ------------------------------------------------------------------
NVERBS    = 10              ; 0 = walk to
V_WALK    = 0
V_GIVE    = 1
V_PICKUP  = 2
V_USE     = 3
V_OPEN    = 4
V_LOOK    = 5
V_PUSH    = 6
V_CLOSE   = 7
V_TALK    = 8
V_PULL    = 9

MAXINV    = 24
MAXACT    = 12
MAXDIRTY  = 24
NSLOTS    = 4               ; script threads
WALK_W    = 80              ; walk mask: 4x4 pixel cells
WALK_H    = 42
MAXPATH   = 40
TICK      = 2               ; frames per game tick (25 per second)

; ---- data file layout (made by build.py, see data.i) ---------------------------
; ROOM   0 .l picture   4 .w palette[16]   36 .l walk mask   40 .l objects
;        44 .l enter script   48 .l timer script   52 .w timer ticks
;        54 .w random min   56 .w random max   58 .l random script   62 .w music
;        64 .l colour cycles: .w n, n x (.w register, frames per step, count, count x colour)
R_PIC     = 0
R_PAL     = 4
R_WALK    = 36
R_OBJS    = 40
R_ENTER   = 44
R_TIMER   = 48
R_TICKS   = 52
R_RMIN    = 54
R_RMAX    = 56
R_RANDOM  = 58
R_MUSIC   = 62
R_CYC     = 64              ; .l colour cycles (0: none)
R_SIZE    = 68

; OBJECT 0 .w x0 y0 x1 y1   8 .w walk x, y   12 .b dir  13 .b default verb
;        14 .w room   16 .l name   20 .l handlers   24 .l image (frame)
;        28 .w image x, y   32 .l icon   36 .w state at start   38 .w actor+1
O_X0      = 0
O_Y0      = 2
O_X1      = 4
O_Y1      = 6
O_WX      = 8
O_WY      = 10
O_DIR     = 12
O_DEFV    = 13
O_ROOM    = 14
O_NAME    = 16
O_HAND    = 20
O_IMAGE   = 24
O_IX      = 28
O_IY      = 30
O_ICON    = 32
O_STATE   = 36
O_ACTOR   = 38
O_SIZE    = 40

ST_HERE   = 1               ; object state bits: there (can be pointed at)
ST_IMAGE  = 2               ;   its picture is drawn into the room

; FRAME  0 .w width in words (+1 for the shift)   2 .w height   4 .w hot x   6 .w hot y
;        8 .l planes (offset in the chip file; the mask follows)
F_WW      = 0
F_H       = 2
F_HX      = 4
F_HY      = 6
F_DATA    = 8
F_SIZE    = 12

; COSTUME 0 .l frames   4 .w stand[4]   12 .w walk count   14 .w walk[4][8]
;         78 .w talk[4][2]   94 .l specials   98 .w talk colour
C_FRAMES  = 0
C_STAND   = 4
C_WALKN   = 12
C_WALK    = 14
C_TALK    = 78
C_SPEC    = 94
C_SIZE    = 100

; ACTOR (run time)
A_ROOM    = 0               ; .w room (0 = nowhere)
A_X       = 2
A_Y       = 4
A_DIR     = 6               ; 0 right 1 left 2 front 3 back
A_COST    = 8               ; .l costume
A_FRAME   = 12              ; .w frame shown
A_MODE    = 14              ; .w 0 stand 1 walk 2 talk 3 special
A_CNT     = 16
A_POS     = 18
A_NPATH   = 20
A_PATHI   = 22
A_SPEC    = 24              ; .l special animation
A_LOOP    = 28              ; .w special loops
A_COL     = 30              ; .w talk colour
A_SPEED   = 32
A_TALKING = 34
A_PATH    = 36              ; MAXPATH * (x.w, y.w)
A_SIZE    = A_PATH+MAXPATH*4

MARK    macro                       ; debugging: a stage number at $1e0
        move.w  #\1,$1e0.w
        endm
