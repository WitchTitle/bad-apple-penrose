import os


output_txt_filename = r'PATH\bad_apple_penrose\penroses\command_line.bat'
if not os.path.exists(output_txt_filename):
    with open(output_txt_filename, 'w') as file:
            
        for i in range(0,2589+1):
            b = len(str(i))-1 #1-9 returns 0, 10-99 returns 1, 100-999 returns 2...
            zero = "0"*(5-b) #Sony vegas image sequences are name_000000
            name = "a_"+zero + str(i) #an example of name is a_000123 (frame 123)

            file.write(fr'python PATH\bad_apple_penrose\pywonderland-master\src\misc\penrose.py {i}'+'\n')