okch = True
def debug(prefix, *args, N=6):
    ch = " " + prefix + args[0] + " " + repr(args[1]) + " "
    for i in range(1, len(args)//2):
        if not '/' in args[2*i]:
            ch += " "*(N-len(ch)%N)+"║"+args[2*i]+" "+repr(args[2*i+1])
    try:
        if ":" in args[1]:
            print(ch)
    except: pass
    # print(ch)


from sys import argv

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEC = "0123456789"
OP = {
  '+': lambda a:a[0]+a[1],
  '_': lambda a:-a[0] if isinstance(a[0],int) else len(a),
  '=': lambda a:a[0]==a[1],
  '>': lambda a:a[0]>a[1],
  't': lambda a:str(a[0]),
  ':': lambda a:a[0][a[1]],
  "list": lambda a:a
}


def raw_number(λ):
    z, ζ = 0, 1
    for char in λ:
        if char in DEC:
            z = 10*z + int(char)
            ζ += 1
        else:
            break
    return z, ζ





def run(blip):
    funs = "+_=>t*?;:"
    funs_n = {'+':2, '_':1, '=':2, '>':2, 't':1, '*':2, '?':1, ';':2, ':':2}
    funs_l = {}
    funs_t = ""
    funs_i = ""
    args = [[] for i in range(26)]
    postack = []
    pos = [len(blip)-1, 0]
    stack = []
    quer = [-1]
    text_pos = []
    oper = []
    iter_a = []
    iter_i = []
    iter_v = []
    iter_p = []

    for i in range(len(blip)-1):
        λ = blip[i]
        if not λ[0] in ":\n":
            τ = λ[0] == 't'
            ι = λ[0] == 'i'
            j, n = 1+τ+ι, 0
            while j < len(λ):
                if λ[j] == 't' and j != len(λ)-1 and λ[j+1] in DEC:
                    z,ζ = raw_number(λ[j+1:])
                    j += z+ζ-1
                if λ[j] in ALPHA:
                    n = max(n, ALPHA.index(λ[j])+1)
                j += 1
            funs += λ[τ+ι]
            funs_n[λ[τ+ι]] = n-ι
            funs_l[λ[τ+ι]] = i
            if τ:
                funs_t += λ[1]
            if ι:
                funs_i += λ[1]

    i, n = 0, 0
    while i < len(blip[-1]):
        if blip[-1][i] == 't' and i != len(blip[-1])-1 and blip[-1][i+1] in DEC:
            z,ζ = raw_number(blip[-1][i+1:])
            i += z+ζ-1
        if blip[-1][i] in ALPHA:
            n = max(n, ALPHA.index(blip[-1][i])+1)
        i += 1

    for i in range(n):
        args[i].append(int(input()))
    
    stop = False
    jump = 0
    text = False
    iterator = 0
    while not stop:
        ε = blip[pos[0]][pos[1]]
        debug("║", "s", stack, "p", pos, "ε", ε, "j", jump, "ps", postack, "/i", (iter_a, iter_i, iter_p, iter_v), "a", args[0], "tp", text_pos)
        if ε in ALPHA:
            if not jump:
                stack.append(args[ALPHA.index(ε)][-1])
                quer[-1] -= 1
            pos[1] += 1
        elif ε == 'n':
            x, ξ = raw_number(blip[pos[0]][pos[1]+1:])
            if not jump:
                stack.append(x)
                quer[-1] -= 1
            pos[1] += ξ
        elif ε == 't' and blip[pos[0]][pos[1]+1] in DEC+'t':
            if blip[pos[0]][pos[1]+1] == 't':
                if not jump:
                    stack.append('\n')
                    quer[-1] -= 1
                pos[1] += 2
            else:
                x, ξ = raw_number(blip[pos[0]][pos[1]+1:])
                if not jump:
                    stack.append(blip[pos[0]][pos[1]+ξ:pos[1]+ξ+x])
                    quer[-1] -= 1
                pos[1] += ξ+x
        elif ε == ':' and blip[pos[0]][pos[1]+1] in DEC:
            x, ξ = raw_number(blip[pos[0]][pos[1]+1:])
            if jump:
                jump += x
            else:
                oper.append(len(stack))
                quer.append(x)
                stack.append("list")
            pos[1] += ξ
        
        
        elif ε == '.':
            if not jump:
                stack.append(iter_v[-1])
                quer[-1] -= 1
            pos[1] += 1
        elif ε == 'i':
            if not jump:
                stack.append(iter_i[-1])
                quer[-1] -= 1
            pos[1] += 1

        elif ε in funs:
            if jump:
                jump += funs_n[ε]
            else:
                oper.append(len(stack))
                quer.append(funs_n[ε])
                stack.append(ε)
            pos[1] += 1
        
        debug("╟", "s", stack, "p", pos, "ε", ε, "j", jump, "ps", postack, "/i", (iter_a, iter_i, iter_p, iter_v), "a", args[0], "tp", text_pos)

        while quer[-1] != 0 and pos[0] != len(blip)-1 and pos[1] == len(blip[pos[0]])-1:
            depth = len(postack)
            pos = postack[-1]
            postack.pop()
            i = 0
            while len(args[i]) == depth:
                args[i].pop()
                i += 1
            debug("╢", "s", stack, "p", pos, "ε", ε, "j", jump, "ps", postack, "/i", (iter_a, iter_i, iter_p, iter_v), "a", args[0], "tp", text_pos)
        
        jumping = False
        while quer[-1] == 0:
            fun = stack[oper[-1]]
            if fun in OP.keys():
                stack.append(OP[fun](stack[oper[-1]+1:]))
                del stack[oper[-1]:-1]
                oper.pop()
                quer.pop()
                quer[-1] -= 1
            elif fun == '?':
                if stack[oper[-1]+1]:
                    stack.pop()
                    stack[-1] = "jump"
                    quer[-1] = 1
                else:
                    jump += 1
                    jumping = True
                    oper.pop()
                    quer.pop()
                    del stack[-2:]
            elif fun == "jump":
                jump += 1
                jumping = True
                del stack[-2]
                oper.pop()
                quer.pop()
                quer[-1] -= 1
            elif fun == "text":
                print(stack.pop())
                stack.pop()
                oper.pop()
                quer.pop()
                pos[1] = 2
            elif fun == ';':
                iter_a.append(stack[-2])
                iter_v.append(stack[-1])
                iter_i.append(1)
                del stack[-2:]
                stack[-1] = "iter"
                quer[-1] = 1
            elif fun == "iter":
                assert iter_i[-1] <= iter_a[-1], "Iterator Error ( i>max(i) )"
                if iter_i[-1] == iter_a[-1]:  # Fin d'itération
                    del stack[-2]
                    for λ in (oper, quer, iter_i, iter_v, iter_a, iter_p):
                        λ.pop()
                    quer[-1] -= 1
                else:
                    iter_v[-1] = stack[-1]
                    stack.pop()
                    quer[-1] = 1
                    iter_i[-1] += 1
                    new_pos = iter_p[-1].copy()
                    if new_pos[0] != pos[0]:
                        depth = len(postack)
                        postack.pop()
                        i = 0
                        while len(args[i]) == depth:
                            args[i].pop()
                            i += 1
                        if len(text_pos)>0 and pos[1] == text_pos[-1]:
                            text_pos.pop()
                        debug("╣", "s", stack, "p", pos, "ε", ε, "j", jump, "ps", postack, "/i", (iter_a, iter_i, iter_p, iter_v), "a", args[0], "tp", text_pos)
                    pos = new_pos.copy()
            else:
                postack.append(pos.copy())
                for i in range(len(stack)-oper[-1]-1):
                    args[i].append(stack[oper[-1]+i+1])
                if fun in funs_i:
                    args[len(stack)-oper[-1]-1].append(int(input()))
                pos = [funs_l[fun], 1 + (fun in funs_t+funs_i)]
                del stack[oper[-1]:]
                oper.pop()
                quer.pop()
                if fun in funs_t:
                    jump = 2
                    oper.append(len(stack))
                    quer.append(1)
                    stack.append("text")


        debug("╠", "s", stack, "p", pos, "ε", ε, "j", jump, "ps", postack, "/i", (iter_a, iter_i, iter_p, iter_v), "a", args[0], "tp", text_pos)
        
        if len(text_pos) > 0 and pos[1] == text_pos[-1]:
            jump = 1
            jumping = True
            text_pos.pop()

        if jump and not jumping:
            jump -= 1

            if jump == 0 and len(stack)>0 and stack[-1] == "text":
                text_pos.append(pos[1])
        
        if jump == 0 and len(stack)>0 and stack[-1] == "iter" and len(iter_p)<len(iter_a):
            iter_p.append(pos.copy())

        if quer[-1] == -2:
            stop = True

        # iterator += 1
        # if iterator>100:
        #     print("┌────────────────┐")
        #     print("│ STACK OVERFLOW │")
        #     print("└────────────────┘")
        #     stop=True

    return stack[0]










if argv[1] == "exe":
    file = argv[2]
    if len(file)<5 or file[-5:] != ".blip": file += ".blip"
    print(run(open(file, 'r', encoding="utf-8").readlines()))
elif argv[1] == "run":
    print(run(argv[2]))
