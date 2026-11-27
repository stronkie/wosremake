;*---------------------------------------------------------------------------
;  :Program.	World of Stronkie remake - WHDLoad slave
;  :Contents.	Boots Kickstart 3.1 (kick31 emulation by Wepl, JOTD and
;		Psygore; 68000 version: the A600 Kickstart 40.063), mounts
;		the data drawer as DH0: and starts the game from there.
;  :Author.	Mark Stronks, Stronkie Soft (slave by Claude)
;  :Language.	68000 Assembler (vasm)
;---------------------------------------------------------------------------*

	INCLUDE	whdload.i
	INCLUDE	whdmacros.i
	INCLUDE	lvo/dos.i
	INCLUDE	lvo/exec.i

CHIPMEMSIZE	= $100000	;1 MB chip, like an A500 with the 8372A Agnus
FASTMEMSIZE	= 0		;no fast memory: ExpMem holds only the Kickstart image
NUMDRIVES	= 1
WPDRIVES	= %0000

NO68020				;runs on a plain 68000 too
BLACKSCREEN
BOOTDOS
CACHECHIP
HDINIT
IOCACHE		= 1024

slv_Version	= 19
slv_Flags	= WHDLF_NoError
slv_keyexit	= $59		;F10 quits

	INCLUDE	whdload/kick31.s

slv_CurrentDir	dc.b	"data",0
		INCLUDE	whdname.i
slv_copy	dc.b	"2026 Mark Stronks, Stronkie Soft",0
slv_info	dc.b	"by Mark Stronks, Stronkie Soft",10
		INCLUDE	version.i
		dc.b	"WHDLoad install for Stronkie Soft",10
		dc.b	"kick31 emulation by Wepl, JOTD, Psygore",0
	EVEN
slv_config	= slv_base	;(no config options)

;============================================================================
; _bootdos: give the process a home drawer (PROGDIR:), load the game with
; dos.LoadSeg and run it

_bootdos	move.l	(_resload,pc),a2
		lea	(_dosname,pc),a1
		move.l	(4).w,a6
		jsr	(_LVOOldOpenLibrary,a6)
		move.l	d0,a6
		lea	(_here,pc),a0		;PROGDIR: = the data drawer
		move.l	a0,d1
		moveq	#-2,d2			;SHARED_LOCK
		jsr	(_LVOLock,a6)
		move.l	d0,d5
		sub.l	a1,a1
		move.l	a6,-(a7)
		move.l	(4).w,a6
		jsr	(_LVOFindTask,a6)
		move.l	(a7)+,a6
		move.l	d0,a0
		move.l	d5,188(a0)		;pr_HomeDir
		lea	(_program,pc),a0
		move.l	a0,d1
		jsr	(_LVOLoadSeg,a6)
		move.l	d0,d7
		beq	.noseg
		lsl.l	#2,d0
		move.l	d0,a1
		lea	(_args,pc),a0
		moveq	#1,d0
		movem.l	d7/a2/a6,-(a7)
		jsr	(4,a1)
		movem.l	(a7)+,d7/a2/a6
		move.l	d7,d1
		jsr	(_LVOUnLoadSeg,a6)
		pea	TDREASON_OK
		jmp	(resload_Abort,a2)
.noseg		pea	(_program,pc)
		pea	205			;object not found
		pea	TDREASON_DOSREAD
		jmp	(resload_Abort,a2)

		INCLUDE	whdprog.i
_here		dc.b	"",0
_args		dc.b	10,0
	EVEN
