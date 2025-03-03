from amoco.config import conf

conf.UI.formatter = "Null"
conf.Cas.unicode = False
conf.UI.unicode = False

from amoco.arch.x86.cpu_x86 import cpu
from amoco.arch.x86.formats import IA32_Intel, IA32_Binutils_ATT

# enforce Intel syntax and NullFormatter output:
cpu.disassemble.iclass.set_formatter(IA32_Intel)


def test_decoder_000():
    c = b"\x90"
    i = cpu.disassemble(c)
    assert i.mnemonic == "NOP"


# mov eax,[eax+0x10]
def test_decoder_001():
    c = b"\x8b\x40\x10"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "eax"
    op2 = i.operands[1]
    assert str(op2) == "M32ds(eax+16)"


# callf [ebx+eax*8+0x01eb6788]
def test_decoder_002():
    c = b"\xff\x9c\xc3\x88\x67\xeb\x01"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "M48ds(((eax*0x8)+ebx)+32204680)"
    c = b"\x66\xff\x9c\xc3\x88\x67\xeb\x01"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert op1.size == 32


# jmp 0xc (relative to current eip!)
def test_decoder_003():
    c = b"\xeb\x0c"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert op1.value == 0xC and op1.size == 32


# mov edx,[eax*4+0x0805bd00]
def test_decoder_004():
    c = b"\x8b\x14\x85\x00\xbd\x05\x08"
    i = cpu.disassemble(c)
    op2 = i.operands[1]
    assert str(op2) == "M32ds((eax*0x4)+134593792)"


# les eax,[ebp+edi+0x70a310d3]
def test_decoder_005():
    c = b"\xc4\x84\x3d\xd3\x10\xa3\x70"
    i = cpu.disassemble(c)
    op2 = i.operands[1]
    assert str(op2) == "M48es((ebp+edi)+1889734867)"


# and bl,[0x39a3ac3d]
def test_decoder_006():
    c = b"\x22\x1d\x2d\xac\xa3\x39"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert op1.x.ref == "ebx"
    assert str(op1) == "bl"
    op2 = i.operands[1]
    assert str(op2) == "M8ds(0x39a3ac2d)"


# imul ebp,ecx,0xc23d
def test_decoder_007():
    c = b"\x69\xe9\x3d\xc2\x00\x00"
    i = cpu.disassemble(c)
    op1, op2, op3 = i.operands
    assert str(op1) == "ebp" and str(op2) == "ecx" and str(op3) == "0xc23d"


# add dh,[ebp+0x240489ca]
def test_decoder_008():
    c = b"\x02\xb5\xca\x89\x04\x24"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "dh"
    op2 = i.operands[1]
    assert str(op2) == "M8ds(ebp+604277194)"


# add [eax],al
def test_decoder_009():
    c = b"\x00\x00"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "M8ds(eax)"
    op2 = i.operands[1]
    assert str(op2) == "al"


# add bh,al
def test_decoder_010():
    c = b"\x00\xc7"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    op2 = i.operands[1]
    assert str(op1) == "bh" and str(op2) == "al"


# movzx edx,[eax+0x0805b13c]
def test_decoder_011():
    c = b"\x0f\xb6\x90\x3c\xb1\x05\x08"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    op2 = i.operands[1]
    assert str(op1) == "edx" and str(op2) == "M8ds(eax+134590780)"


# ror cs:[edi],0x8f
def test_decoder_012():
    c = b"\x2e\xc0\x0f\x8f"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "M8cs(edi)"
    assert op1.a.seg.ref == "cs"
    assert op1.size == 8
    op2 = i.operands[1]
    assert op2.size == 8


# mov cs,[edi-0x6d1b46d2]
def test_decoder_013():
    c = b"\x8e\x8f\x2e\xb9\xe4\x92"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    op2 = i.operands[1]
    assert str(op1) == "cs" and op2.size == 16


# fsub st,st(5)
def test_decoder_014():
    c = b"\xd8\xe5"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    op2 = i.operands[1]
    assert str(op1) == "st0" and str(op2) == "st5" and op1.size == 80 and op2.size == 80


# dec [edx+0x6153e80e]
def test_decoder_015():
    c = b"\xfe\x8a\x0e\xe8\x53\x61"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "M8ds(edx+1632888846)"


# fistp word [ebx+edi*8]
def test_decoder_016():
    c = b"\xdf\x1c\xfb"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "M16ds((ebx+(edi*0x8)))"


# imul ecx,fs:[edx-0x2893a953],0x82da771e
def test_decoder_017():
    c = b"\x64\x69\x8a\xad\x56\x6c\xd7\x1e\x77\xda\x82"
    i = cpu.disassemble(c)
    op1, op2, op3 = i.operands
    assert str(op2) == "M32fs(edx-680765779)" and str(op3) == "0x82da771e"


# fsubrl [ecx]
def test_decoder_018():
    c = b"\xdc\x29"
    i = cpu.disassemble(c)
    op1 = i.operands[0]
    assert str(op1) == "M64ds(ecx)"


# cmpxchg8b qword ptr [ecx]
def test_decoder_019():
    c = b"\x0f\xc7\x09"
    i = cpu.disassemble(c)
    assert str(i.operands[0]) == "M64ds(ecx)"


# movzx eax, byte ptr [eax+0x806fb088]
def test_decoder_020():
    c = b"\x0f\xb6\x80\x88\xb0\x6f\x80"
    i = cpu.disassemble(c)
    assert str(i.operands[1]) == "M8ds(eax-2140163960)"
    assert i.toks()[-1][1] == "byte ptr [eax+0x806fb088]"


# mov eax, [esp-300]
def test_decoder_021():
    c = b"\x8b\x84\x24\xd4\xfe\xff\xff"
    i = cpu.disassemble(c)
    assert str(i.operands[1]) == "M32ds(esp-300)"
    assert i.toks()[-1][1] == "[esp-300]"


# cvtss2sd [ebp-16], xmm0
def test_decoder_022():
    c = b"\xf3\x0f\x5a\x45\xf0"
    i = cpu.disassemble(c)
    assert i.mnemonic == "CVTSS2SD"
    op1 = i.operands[0]
    assert op1._is_reg and op1.size == 128
    assert str(op1) == "xmm0"


# cvttss2si eax, [ebp-16]
def test_decoder_023():
    c = b"\xf3\x0f\x2c\x45\xf0"
    i = cpu.disassemble(c)
    assert i.mnemonic == "CVTTSS2SI"
    assert i.toks()[2][1] == "eax"


# cvtss2si eax, [ebp-16]
def test_decoder_024():
    c = b"\xf3\x0f\x2d\x45\xf0"
    i = cpu.disassemble(c)
    assert i.mnemonic == "CVTSS2SI"
    assert i.toks()[2][1] == "eax"


# push -1
def test_decoder_025():
    c = b"\x6a\xff"
    i = cpu.disassemble(c)
    assert i.mnemonic == "PUSH"
    op1 = i.operands[0]
    assert op1.sf
    assert op1.value == -1
    assert op1.size == 8


# movq qword ptr [ebp-16], xmm1
def test_decoder_026():
    c = b"\x66\x0f\xd6\x4d\xf0"
    i = cpu.disassemble(c)
    assert i.mnemonic == "MOVQ"
    assert i.toks()[2][1] == "qword ptr [ebp-16]"


# movq xmm2, qword ptr [ebp-16]
def test_decoder_027():
    c = b"\xf3\x0f\x7e\x55\xf0"
    i = cpu.disassemble(c)
    assert i.mnemonic == "MOVQ"
    assert i.toks()[2][1] == "xmm2"
    assert i.toks()[4][1] == "qword ptr [ebp-16]"


# movq xmm0, xmm1
def test_decoder_028():
    c = b"\xf3\x0f\x7e\xc1"
    i = cpu.disassemble(c)
    assert i.mnemonic == "MOVQ"
    op1, op2 = i.operands
    assert op1.size == op2.size == 128


# lock incl (%ecx)
def test_decoder_029():
    c = b"\xf0\xff\x01"
    i = cpu.disassemble(c)
    assert i.mnemonic == "INC"
    assert i.misc["pfx"] == ["lock", None, None, None]


def test_decoder_rep_scasd():
    c = b"\xf3\xaf"
    i = cpu.disassemble(c)
    i.set_formatter(IA32_Binutils_ATT)
    assert str(i).strip() == "repz scasl"
    i.set_formatter(IA32_Intel)
    assert i.length == 2


def test_pickle_instruction():
    import pickle

    pickler = lambda x: pickle.dumps(x, 2)
    c = b"\xff\x9c\xc3\x88\x67\xeb\x01"
    i = cpu.disassemble(c)
    i.address = cpu.cst(0x1000, 32)
    p = pickler(i)
    j = pickle.loads(p)
    assert str(j) == str(i)


# ------------------------------------------------------------------------------


def test_asm_000(amap):
    c = b"\x90"
    i = cpu.disassemble(c, address=0)
    # fake eip cst:
    amap[cpu.eip] = cpu.cst(0, 32)
    i(amap)
    assert str(amap(cpu.eip)) == "0x1"


# wait
def test_asm_001(amap):
    c = b"\x9b"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert i.mnemonic == "WAIT"
    assert str(amap(cpu.eip)) == "0x2"


# leave
def test_asm_002(amap):
    c = b"\xc9"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert (
        str(amap)
        == """\
eip <- { | [0:32]->0x3 | }
esp <- { | [0:32]->(ebp+0x4) | }
ebp <- { | [0:32]->M32ss(ebp) | }"""
    )


# ret
def test_asm_003(amap):
    c = b"\xc3"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert str(amap(cpu.eip)) == "M32ss(ebp+4)"
    assert str(amap(cpu.esp)) == "(ebp+0x8)"
    assert str(amap(cpu.ebp)) == "M32ss(ebp)"


# hlt
def test_asm_004(amap):
    c = b"\xf4"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert i.mnemonic == "HLT"
    assert amap(cpu.eip) == cpu.top(32)


# int3
def test_asm_005(amap):
    c = b"\xcc"
    i = cpu.disassemble(c, address=0)
    assert i.mnemonic == "INT3"
    i(amap)


# push eax
def test_asm_006(amap):
    c = b"\x50"
    i = cpu.disassemble(c, address=0)
    amap.clear()
    amap[cpu.eip] = cpu.cst(0)
    amap[cpu.esp] = cpu.cst(0)
    i(amap)
    assert amap(cpu.mem(cpu.esp)) == cpu.eax
    assert amap(cpu.esp) == cpu.cst(-4)


# pop eax
def test_asm_007(amap):
    c = b"\x58"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.eax) == cpu.eax
    assert amap(cpu.esp) == 0


# call edx
def test_asm_008(amap):
    c = b"\xff\xd2"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.eip) == cpu.edx
    assert amap(cpu.mem(cpu.esp)) == 0x4


# call eip+0x00000000 (eip+0)
def test_asm_009(amap):
    c = b"\xe8\x00\x00\x00\x00"
    i = cpu.disassemble(c, address=0)
    i.address = 0x08040000
    amap.clear()
    i(amap)
    assert amap(cpu.mem(cpu.esp, 32)) == amap(cpu.eip)


# call eip+0xffffff9b (eip-101)
def test_asm_010(amap):
    c = b"\xe8\x9b\xff\xff\xff"
    i = cpu.disassemble(c, address=0)
    amap.clear()
    i.address = 0x08040005
    amap[cpu.eip] = cpu.cst(i.address, 32)
    i(amap)
    assert str(i) == "call        0x803ffa5"
    assert amap(cpu.mem(cpu.esp)) == i.address + 5
    assert amap(cpu.eip) == (i.address + 5 - 101)


# jmp eip+12
def test_asm_011(amap):
    c = b"\xeb\x0c"
    i = cpu.disassemble(c, address=0)
    i.address = amap(cpu.eip).v
    i(amap)
    assert amap(cpu.mem(cpu.esp)) == i.address + 101
    assert amap(cpu.eip) == i.address + i.length + 12


# jmp eip-32
def test_asm_012(amap):
    c = b"\xe9\xe0\xff\xff\xff"
    i = cpu.disassemble(c, address=0)
    i.address = amap(cpu.eip).v
    i(amap)
    assert amap(cpu.eip) == i.address + i.length - 32


# jmp [0x0805b0e8]
def test_asm_013(amap):
    c = b"\xff\x25\xe8\xb0\x05\x08"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.eip) == cpu.mem(cpu.cst(0x805B0E8), seg=cpu.ds)


# retn 0xc
def test_asm_014(amap):
    c = b"\xc2\x0c\x00"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.eip) == 0x804000A
    assert str(amap(cpu.esp)) == "(esp+0xc)"


# int 0x80
def test_asm_015(amap):
    c = b"\xcd\x80"
    i = cpu.disassemble(c, address=0)
    i(amap)


# inc eax
def test_asm_016(amap):
    c = b"\x40"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.eax) == (cpu.eax + 1)


# dec esi
def test_asm_017(amap):
    c = b"\x4e"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.esi) == (cpu.esi - 1)


# mov eax,[eax+0x10]
def test_asm_018(amap):
    c = b"\x8b\x40\x10"
    i = cpu.disassemble(c, address=0)
    amap.clear()
    i(amap)
    assert str(amap(cpu.eax)) == "M32ds(eax+16)"


# movsx edx,al
def test_asm_019(amap):
    c = b"\x0f\xbe\xd0"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.edx)[0:8] == amap(cpu.al)
    assert str(amap(cpu.edx)[8:32]) == "(M8ds(eax+16)[7:8] ? -0x1 : 0x0)"


# movzx edx,[eax+0x0805b13c]
def test_asm_020(amap):
    c = b"\x0f\xb6\x90\x3c\xb1\x05\x08"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.edx)[8:32] == 0


# add [eax],al
def test_asm_021(amap):
    c = b"\x00\x00"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert str(amap(cpu.mem(cpu.eax, 8))) == "(M8ds(M32ds(eax+16))+M8ds(eax+16))"


# sub [edx+esi-0x43aa74b0], cl
def test_asm_022(amap):
    c = b"\x28\x8c\x32\x50\x8b\x55\xbc"
    i = cpu.disassemble(c, address=0)
    i(amap)
    loc = cpu.ptr(amap(cpu.edx) + cpu.esi, disp=-0x43AA74B0)
    assert (
        str(amap[cpu.mem(loc, 8)])
        == "((-cl)+M8ds(({ | [0:8]->M8ds(M32ds(eax+16)+134590780) | [8:32]->0x0 | }+esi)-1135244464))"
    )


# and ebp,[edi-0x18]
def test_asm_023(amap):
    c = b"\x23\x6f\xe8"
    i = cpu.disassemble(c, address=0)
    amap.clear()
    i(amap)
    assert amap(cpu.ebp) == cpu.ebp & cpu.mem(cpu.edi, 32, disp=-0x18, seg=cpu.ds)


# and esp,0xfffffff0
def test_asm_024(amap):
    c = b"\x83\xe4\xf0"
    i = cpu.disassemble(c, address=0)
    amap[cpu.esp] = cpu.cst(0xC0000004)
    i(amap)
    assert amap[cpu.esp] == 0xC0000000


# or al,0
def test_asm_025(amap):
    c = b"\x0c\x00"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.al) == cpu.al | 0
    assert amap(cpu.ah) == cpu.ah


# xor edx,[ebp-0x1c]
def test_asm_026(amap):
    c = b"\x33\x55\xe4"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.edx) == cpu.edx ^ amap(cpu.mem(cpu.ebp, 32, disp=-0x1C, seg=cpu.ds))


# cmp edx,0
def test_asm_027(amap):
    c = b"\x83\xfa\x00"
    i = cpu.disassemble(c, address=0)
    amap.clear()
    i(amap)
    assert str(amap(cpu.zf)) == "(edx==0x0)"


# sal al,2
def test_asm_028(amap):
    c = b"\xc0\xf0\x02"
    i = cpu.disassemble(c, address=0)
    i(amap)


# sal esi,0
def test_asm_029(amap):
    c = b"\xc1\xf6\x20"
    i = cpu.disassemble(c, address=0)
    i(amap)


# mov byte ptr [edx], al
def test_asm_030(amap):
    c = b"\x88\x02"
    i = cpu.disassemble(c, address=0)
    i(amap)


# lea eax, [edx]
def test_asm_031(amap):
    c = b"\x8d\x02\xc3"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert str(amap(cpu.eax)) == "edx"


# pop esp
def test_asm_032(amap):
    c = b"\x5c"
    i = cpu.disassemble(c, address=0)
    amap.clear()
    amap[cpu.esp] = cpu.cst(0x1000, 32)
    amap[cpu.mem(cpu.esp, 32)] = cpu.cst(0x67452301, 32)
    i(amap)
    assert amap(cpu.esp) == cpu.cst(0x67452301, 32)


# push esp
def test_asm_033(amap):
    c = b"\x54"
    i = cpu.disassemble(c, address=0)
    i(amap)
    assert amap(cpu.esp) == 0x67452301 - 4
    assert amap(cpu.mem(cpu.esp, 32)) == cpu.cst(0x67452301, 32)
