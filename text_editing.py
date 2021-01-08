
omega = 10  # radians/s
freq = 50  # cycles/s



keyword = 'CYL_ROTATION_PROP'




f_lines[keyword_line_i] = keyword + ' = ' + str(omega) + ' ' + str(freq) + '\n'

with open('2D_cylinder.in', 'w') as f_out:
    f_out.writelines(f_lines)
