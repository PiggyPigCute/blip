from sys import argv

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEC = "0123456789"

def raw_number(λ):
    z, ζ = 0, 1
    for char in λ:
        if char in DEC:
            z = 10*z + int(char)
            ζ += 1
        else:
            break
    return z, ζ


def calc(λ, args, funs, σ, size = False):
    σ += 1
    print(σ)
    if λ[0] in ALPHA:
        return args[ALPHA.index(λ[0])], 1
    elif λ[0] == '+':
        a, α = calc(λ[1:], args, funs, σ)
        b, β = calc(λ[(1+α):], args, funs, σ)
        return a+b, α+β+1
    elif λ[0] == '_':
        a, α = calc(λ[1:], args, funs, σ)
        return -a, α+1
    elif λ[0] == '?':
        a, α = calc(λ[1:], args, funs, σ)
        b, β = calc(λ[(1+α):], args, funs, σ, True)
        c, γ = calc(λ[(1+α+β):], args, funs, σ, True)
        if a:
            b, β = calc(λ[(1+α):], args, funs, σ)
            return b, α+β+γ+1
        else:
            c, γ = calc(λ[(1+α+β):], args, funs, σ)
            return c, α+β+γ+1
    elif λ[0] == '=':
        a, α = calc(λ[1:], args, funs, σ)
        b, β = calc(λ[(1+α):], args, funs, σ)
        return a==b, α+β+1
    elif λ[0] == '>':
        a, α = calc(λ[1:], args, funs, σ)
        b, β = calc(λ[(1+α):], args, funs, σ)
        return a>b, α+β+1
    elif λ[0] == ';':
        a, α = calc(λ[1:], args, funs, σ)
        b, β = calc(λ[(1+α):], args, funs, σ)

        z = b
        ζ = calc(λ[(1+α+β):], args+[b,1], funs, σ)[1]
        for i in range(1,a+1):
            z = calc(λ[(1+α+β):], args+[z,i], funs, σ)[0]
        
        return z, α+β+ζ+1
    elif λ[0] == 'i':
        return args[-1], 1
    elif λ[0] == '.':
        return args[-2], 1
    elif λ[0] == 'n':
        return raw_number(λ[1:])
    elif λ[0] == 't':
        if λ[1] == 't':
            return "\n", 2
        elif λ[1] in DEC:
            z, ζ = raw_number(λ[1:])
            return λ[ζ:ζ+z], ζ+z
        else:
            a, α = calc(λ[1:], args, funs, σ)
            return str(a), α+1

    elif λ[0] in funs.keys():
        if σ == 900:
            print("┌──────────────────────────────┐")
            print("│ Python recursion depth limit │")
            print("└──────────────────────────────┘")
            return 0, 0
        n = funs[λ[0]][1]
        fun_args = []
        φ = 1
        if size:
            return 0, φ
        for i in range(n):
            z, ζ = calc(λ[φ:], args, funs, σ)
            fun_args.append(z)
            φ += ζ
        a, α = calc(funs[λ[0]][0], fun_args, funs, σ)
        if funs[λ[0]][2]:
            b, β = calc(funs[λ[0]][0][α:], fun_args, funs, σ)
            print(b)
        return a, φ

    return 0,0

def run(blip):
    funs = {}
    for λ in blip[:-1]:
        τ = λ[0] == 't'
        i, n = 1+τ, 0
        while i < len(λ):
            if λ[i] == 't' and i != len(λ)-1 and λ[i+1] in DEC:
                z,ζ = raw_number(λ[i+1:])
                i += z+ζ-1
            if λ[i] in ALPHA:
                n = max(n, ALPHA.index(λ[i])+1)
            i += 1
        funs[λ[τ]] = λ[1+τ:], n, τ
    
    i, n = 0, 0
    while i < len(blip[-1]):
        if blip[-1][i] == 't' and i != len(blip[-1])-1 and blip[-1][i+1] in DEC:
            z,ζ = raw_number(blip[-1][i+1:])
            i += z+ζ-1
        if blip[-1][i] in ALPHA:
            n = max(n, ALPHA.index(blip[-1][i])+1)
        i += 1
    args = []
    for i in range(n):
        args.append(int(input()))
    return calc(blip[-1], args, funs, 0)[0]


if argv[1] == "exe":
    print(run(open(argv[2], 'r').readlines()))
elif argv[1] == "run":
    print(run(argv[2]))