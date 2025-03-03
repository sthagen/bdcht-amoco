# -*- coding: utf-8 -*-

# This code is part of Amoco
# Copyright (C) 2006-2011 Axel Tillequin (bdcht3@gmail.com)
# published under GPLv2 license

from amoco.logger import Log

logger = Log(__name__)
logger.debug("loading module")

from amoco.system.core import DefineLoader, CoreExec


@DefineLoader("raw")
class RawExec(CoreExec):
    def __init__(self, p, cpu=None):
        CoreExec.__init__(self, p, cpu)
        self.auto_load()

    # load the program into virtual memory (populate the state.mmap)
    def auto_load(self):
        p = self.bin
        if hasattr(p, "load_binary"):
            p.load_binary(self.state.mmap)
        else:
            self.state.mmap.write(0, p.dataio[0:])
        if self.cpu is None:
            logger.warning("a cpu module must be imported")
        else:
            pc = self.cpu.getPC()
            entry = 0
            if hasattr(p, "entrypoint"):
                entry = p.entrypoint
            self.state[pc] = self.cpu.cst(entry, pc.size)

    def use_x86(self):
        from amoco.arch.x86.cpu_x86 import cpu

        self.cpu = cpu
        self.state[cpu.eip] = cpu.cst(0, 32)

    def use_x64(self):
        from amoco.arch.x64.cpu_x64 import cpu

        self.cpu = cpu
        self.state[cpu.rip] = cpu.cst(0, 64)

    def use_arm(self):
        from amoco.arch.arm.cpu_armv7 import cpu

        self.cpu = cpu
        self.state[cpu.pc_] = cpu.cst(0, 32)

    def use_avr(self):
        from amoco.arch.avr.cpu import cpu

        self.cpu = cpu
        self.state[cpu.pc] = cpu.cst(0, 16)

    def relocate(self, vaddr):
        if self.cpu is None:
            logger.warning("a cpu module must be imported")
        else:
            m = self.state
            mz = m.mmap._zones[None]
            sta, sto = mz.range()
            delta = vaddr - sta
            for z in mz._map:
                z.vaddr += delta
            # force mmap cache update:
            m.restruct()
            # create _initmap with new pc as vaddr:
            pc = self.cpu.PC()
            m[pc] = self.cpu.cst(vaddr, pc.size)
