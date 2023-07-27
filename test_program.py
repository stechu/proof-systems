from compiler.program import Program

if __name__ == "__main__":
    program = Program(["e public", "c <== 2 * a * b + 2 * a + b + 3", "e <== c * d"], 8)
    
    for c in program.constraints:
        print("L: {}, R:{}, O:{}, M:{}".format(c.L(), c.R(), c.O(), c.M()))