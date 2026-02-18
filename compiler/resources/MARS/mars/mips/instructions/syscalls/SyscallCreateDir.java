package mars.mips.instructions.syscalls;

import java.io.File;

import mars.ProcessingException;
import mars.ProgramStatement;

public class SyscallCreateDir extends AbstractSyscall {

    public SyscallCreateDir() {
        super(101, "CreateDir");
    }
    
    @Override
    public void simulate(ProgramStatement statement) throws ProcessingException {
        int address = mars.mips.hardware.RegisterFile.getValue(4);
        StringBuilder pathBuilder = new StringBuilder();
        try {
            while (true) {
                int byteValue = mars.mips.hardware.Memory.getInstance().getByte(address);
                if (byteValue == 0) {
                    break;
                }
                pathBuilder.append((char) byteValue);
                address++;
            }
        } catch (Exception e) {
            throw new ProcessingException(statement, "Invalid memory access at address: " + address);
        }

        String path = pathBuilder.toString();

        File dir = new File(path);
        boolean success = false;
        if (!dir.exists()) {
            success = dir.mkdirs();
        }

        if (success) {
            mars.mips.hardware.RegisterFile.updateRegister(2, 1);
        } else {
            mars.mips.hardware.RegisterFile.updateRegister(2, 0);
        }
    }
    
}
