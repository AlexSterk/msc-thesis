TEMP = "data/rq3/tabs/temp.tex"
TAB = "data/rq3/tabs/Q43.tex"

# read files
with open(TEMP, "r") as f:
    temp = f.readlines()
with open(TAB, "r") as f:
    tab = f.readlines()

# print(temp)
# split into header, body and end
header_len = 6
end_len = 2

for i in range(header_len, len(temp) - end_len):
    line = temp[i]

    # replace \& with \and
    line = line.replace("\\&", "\\and")

    #split by &
    line = line.split("&")
    # remove last 2
    line = line[:-2]
    # wrap last in quotes
    line[-1] = "``" + line[-1].strip() + "\""

    t_line = tab[i]
    #split by &
    t_line = t_line.split("&")
    # copy last 2 items
    line.append(t_line[-2])
    line.append(t_line[-1])

    # join with &
    line = " & ".join(line)

    temp[i] = line

# write to file
with open(TEMP, "w") as f:
    f.writelines(temp)






