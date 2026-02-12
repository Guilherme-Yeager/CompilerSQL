package mars.mips.instructions.syscalls;

import mars.ProcessingException;
import mars.ProgramStatement;

import java.io.File;

public class RemoveDir extends AbstractSyscall {
    public RemoveDir() {
        super(100, "RemoveDir");
    }

    @Override
    public void simulate(ProgramStatement statement) throws ProcessingException {
        int address = mars.mips.hardware.RegisterFile.getValue(4);
        String path = "";
        try{
            while (true) {
                int byteValue;
                    byteValue = mars.mips.hardware.Memory.getInstance().getByte(address);
                    if (byteValue == 0) {
                        break;
                    }
                    path += (char) byteValue;
                    address++;
                }
        } catch (Exception e){
            throw new ProcessingException(statement, "Invalid memory access at address: " + address);
        }
        File dir = new File(path);
        this.removeDir(dir);
        if (!dir.exists()) {
            mars.mips.hardware.RegisterFile.updateRegister(2, 1);
        } else {
            mars.mips.hardware.RegisterFile.updateRegister(2, 0);
        }
    }

    private void removeDir(File dir) throws ProcessingException {
        if(dir.exists()){
            File[] files = dir.listFiles();
            if (files != null) {
                for (File file : files) {
                    this.removeDir(file);
                }
            }
            dir.delete();
        }
    }
}