class AuxVisitorPrint:

    def __init__(self):
        self.output_xml = ""
        self.output_sql = ""
        self.pos_command = 1
        self.tab = 0
        self.mode = 1  # 1: SQL, 2: XML

    def inc_tab(self):
        self.tab += 1

    def dec_tab(self):
        self.tab -= 1

    def indent(self):
        return "   " * self.tab
    
    def add_output_xml(self, text):
        self.output_xml +=  text + "\n"

    def add_output_sql(self, text):
        self.output_sql += text

    def generate_output(self):
        if self.mode == 1:
            print(self.output_sql)
        elif self.mode == 2:
            print("<Script>\n" + self.output_xml + "</Script>\n")

        
    