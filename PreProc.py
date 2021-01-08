class PreProc:
    def __init__(self, x, gen):

        self.inFile = '2D_cylinder.in'
        # open and read YALES2 input file to array of strings for each line
        with open('2D_cylinder.in', 'r') as f_orig:
            f_lines = f_orig.readlines()

        for ind in range(len(self.x)):
            # Extract parameters for each individual
            para = self.x[ind, :]
            omega = para[0]
            freq = para[1]

            ####### Simulation Boundary Condition Parameters ###########
            # find line that must change using a keyword
            keyword = 'CYL_ROTATION_PROP'
            keyword_line, keyword_line_i = self.findKeywordLine(keyword)
            # create new string to replace line
            newLine = keyword + ' = ' + str(omega) + ' ' + str(freq) + '\n'
            f_lines[keyword_line_i] = newLine
            # REPEAT FOR EACH LINE THAT MUST BE CHANGED

            ######### Simulation Geometric Parameters ############


    def gmsh(self):


    def findKeywordLine(self, keyword):
        keyword_line = -1
        keyword_line_i = -1

        for line_i in range(len(f_lines)):
            line = f_lines[line_i]
            if line.find(keyword) >= 0:
                keyword_line = line
                keyword_line_i = line_i

        return keyword_line, keyword_line_i

