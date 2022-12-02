"""

This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

POS_COMMANDS = {'add': 'D+M', 'sub': 'M-D', 'and': 'D&M', 'or': 'D|M'}
NEG_COMMANDS = {'neg': '-M', 'not': '!M', 'shiftright': 'M>>', 'shiftleft': 'M<<'}
COMPARE_COMMANDS = {'gt': 'JGE', 'lt': 'JLE', 'eq': 'JNE'}
MEMORY_SEGMENTS = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
                   'pointer': '3', 'temp': '5', 'static': '16', 'constant': '0'}
PUSH_SEG_LST = ['LCL', 'ARG', 'THIS', 'THAT']
STORE_SEG_LST = ['THAT', 'THIS', 'ARG', 'LCL']

C_PUSH, C_POP = 'C_PUSH', 'C_POP'
CALL_SYMBOL, BAR_SYMBOL, DOT_SYMBOL = '@', '$ֹ', '.'
LOOP, END, RET, END_FR = 'loop', 'end', 'ret', 'endfr'
RESET_STRING, RESET_NUM, NEXT = '', 0, 1

A_OR_M_PUSH = {'local': 'M', 'argument': 'M', 'this': 'M', 'that': 'M',
               'pointer': 'A', 'temp': 'M', 'static': 'M', 'constant': 'A'}
A_OR_M_POP = {'local': 'M', 'argument': 'M', 'this': 'M', 'that': 'M',
              'pointer': 'A', 'temp': 'A', 'static': 'M', 'constant': 'A'}

SEG_CONSTANT = 'D=D+A'
NOT_SEG_CONSTANT = 'A=D+A\nD='

PUSH_PART1, PUSH_PART2 = '@', '\nD='
PUSH_PART3, PUSH_PART4 = '\n@', '\n'
PUSH_PART5 = '\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

POP_PART1, POP_PART2 = '@SP', '\nM=M-1\nA=M\nD=M\n@R13\nM=D\n@'
POP_PART3, POP_PART4 = '\nD=', '\n@'
POP_PART5 = '\nD=D+A\n@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n'

POS_ASSEMBLY_CODE = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM='
POS_FINAL_COMMAND = '\n@SP\nM=M+1\n'
NEG_ASSEMBLY_CODE = '@SP\nM=M-1\nA=M\nM='
NEG_FINAL_COMMAND = '\n@SP\nM=M+1\n'

GT_PART1, GT_PART2 = '@SP\nA=M-1\nD=M\n@yp', '\nD;JGE\n@SP\nA=M-1\nA=A-1\nD=M\n@xpym'
GT_PART3, GT_PART4 = '\nD;JGE\n@xys', '\n0;JMP\n(yp'
GT_PART5, GT_PART6 = ')\n@SP\nA=M-1\nA=A-1\nD=M\n@xys', '\nD;JGE\n@SP\nM=M-1\nM=M-1\nA=M\nM=0\n@end'
GT_PART7, GT_PART8 = '\n0;JMP\n(xpym', ')\n@SP\nM=M-1\nM=M-1\nA=M\nM=0\nM=M-1\n@end'
GT_PART9, GT_PART10 = '\n0;JMP\n(xys', ')\n'

LT_PART1, LT_PART2 = '@SP\nA=M-1\nD=M\n@yp', '\nD;JGE\n@SP\nA=M-1\nA=A-1\nD=M\n@xpym'
LT_PART3, LT_PART4 = '\nD;JGE\n@xys', '\n0;JMP\n(yp'
LT_PART5, LT_PART6 = ')\n@SP\nA=M-1\nA=A-1\nD=M\n@xys', '\nD;JGE\n@SP\nM=M-1\nM=M-1\nA=M\nM=0\nM=M-1\n@end'
LT_PART7, LT_PART8 = '\n0;JMP\n(xpym', ')\n@SP\nM=M-1\nM=M-1\nA=M\nM=0\n@end'
LT_PART9, LT_PART10 = '\n0;JMP\n(xys', ')\n'

EQ_PART1, EQ_PART2 = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\nM=0\n@end', '\nD;'
EQ_PART3, EQ_PART4 = '\n@SP\nA=M\nM=M-1\n(end', ')\n@SP\nM=M+1\n'

LABEL_PART1, LABEL_PART2 = '(', ')\n'

GOTO_PART1 = '\n0;JMP\n'

IF_GOTO_PART1, IF_GOTO_PART2 = '@SP\nM=M-1\nA=M\nD=M\n@', '\nD;JNE\n'

FUNC_PART1, FUNC_PART2 = '(', ')\n@cur\nM=0\n('
FUNC_PART3, FUNC_PART4 = ')\n@cur\nD=M\n@', '\nD=D-A\n@'
FUNC_PART5, FUNC_PART6 = '\nD;JEQ\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@cur\nM=M+1\n@', '\n0;JMP\n('
FUNC_PART7 = ')\n'

PUSH_SEG = '\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
CALL_PART1, CALL_PART2 = '\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n', '@SP\nD=M\n@5\nD=D-A\n@'
CALL_PART3, CALL_PART4 = '\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n', '\n0;JMP\n('
CALL_PART5 = ')\n'

STORE_SEG1, STORE_SEG2 = '\nM=M-1\nA=M\nD=M\n', '\nM=D\n'
RETURN_PART1, RETURN_PART2 = '@LCL\nD=M\n@', '\nM=D\n'
RETURN_PART3, RETURN_PART4 = '@5\nA=D-A\nD=M\n@R15\nM=D\n', '@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n'
RETURN_PART5, RETURN_PART6 = '@ARG\nD=M+1\n@SP\nM=D\n', '@R15\nA=M\n0;JMP\n'




class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_file = output_stream
        self.counter_commands = RESET_NUM
        self.file_name = RESET_STRING
        self.func_name = RESET_STRING
        self.loop_counter = RESET_NUM
        self.end_counter = RESET_NUM
        self.return_counter = RESET_NUM
        self.func_dic = {}

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.file_name = filename
        self.output_file.write('//' + self.file_name + '\n')

    def write_compare_commands(self, command: str) -> None:
        """this command takes care of the writing of the compare commands.
                the commands are: gt, lt, eq"""
        if command == 'gt':
            self.output_file.write(GT_PART1 +
                                   str(self.counter_commands) + GT_PART2 +
                                   str(self.counter_commands) + GT_PART3 +
                                   str(self.counter_commands) + GT_PART4 +
                                   str(self.counter_commands) + GT_PART5 +
                                   str(self.counter_commands) + GT_PART6 +
                                   str(self.counter_commands) + GT_PART7 +
                                   str(self.counter_commands) + GT_PART8 +
                                   str(self.counter_commands) + GT_PART9 +
                                   str(self.counter_commands) + GT_PART10)
        elif command == 'lt':
            self.output_file.write(LT_PART1 +
                                   str(self.counter_commands) + LT_PART2 +
                                   str(self.counter_commands) + LT_PART3 +
                                   str(self.counter_commands) + LT_PART4 +
                                   str(self.counter_commands) + LT_PART5 +
                                   str(self.counter_commands) + LT_PART6 +
                                   str(self.counter_commands) + LT_PART7 +
                                   str(self.counter_commands) + LT_PART8 +
                                   str(self.counter_commands) + LT_PART9 +
                                   str(self.counter_commands) + LT_PART10)
        self.output_file.write(EQ_PART1 +
                               str(self.counter_commands) + EQ_PART2 +
                               COMPARE_COMMANDS[command] + EQ_PART3 +
                               str(self.counter_commands) + EQ_PART4)
        self.counter_commands += NEXT

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """

        if command in POS_COMMANDS:
            self.output_file.write(POS_ASSEMBLY_CODE + POS_COMMANDS[command] + POS_FINAL_COMMAND)
        elif command in NEG_COMMANDS:
            self.output_file.write(NEG_ASSEMBLY_CODE + NEG_COMMANDS[command] + NEG_FINAL_COMMAND)
        else:
            self.write_compare_commands(command)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if segment == 'constant':
            seg_val = SEG_CONSTANT
        elif segment == 'pointer':
            seg_val = NOT_SEG_CONSTANT + 'M'
        else:
            seg_val = NOT_SEG_CONSTANT + A_OR_M_PUSH[segment]
        if command == C_PUSH:
            self.output_file.write(PUSH_PART1 +
                                   MEMORY_SEGMENTS[segment] + PUSH_PART2
                                   + A_OR_M_POP[segment] + PUSH_PART3 +
                                   str(index) + PUSH_PART4 + seg_val +
                                   PUSH_PART5)
        if command == C_POP:
            self.output_file.write(POP_PART1 + POP_PART2
                                   + MEMORY_SEGMENTS[segment] + POP_PART3 +
                                   A_OR_M_POP[segment] + POP_PART4 +
                                   str(index) + POP_PART5)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        self.output_file.write(LABEL_PART1 + self.func_name + BAR_SYMBOL
                               + label + LABEL_PART2)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_file.write(CALL_SYMBOL + self.func_name + BAR_SYMBOL
                               + label + GOTO_PART1)

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        self.output_file.write(IF_GOTO_PART1 + self.func_name + BAR_SYMBOL
                               + label + IF_GOTO_PART2)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        self.func_name = function_name
        self.output_file.write(FUNC_PART1 + self.func_name + FUNC_PART2 +
                               self.func_name + DOT_SYMBOL + LOOP +
                               str(self.loop_counter) + FUNC_PART3 +
                               str(n_vars) + FUNC_PART4 + self.func_name +
                               DOT_SYMBOL + END + str(self.end_counter) +
                               FUNC_PART5 + self.func_name + DOT_SYMBOL +
                               LOOP + str(self.loop_counter) + FUNC_PART6 +
                               self.func_name + DOT_SYMBOL + END +
                               str(self.end_counter) + FUNC_PART7)
        self.end_counter += NEXT
        self.loop_counter += NEXT

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        if function_name not in self.func_dic:
            self.func_dic[function_name] = RESET_NUM
        else:
            self.func_dic[function_name] += NEXT
        cur_ret = BAR_SYMBOL + RET + DOT_SYMBOL + str(self.func_dic[function_name])
        print_ret = function_name + cur_ret + self.file_name
        self.output_file.write(BAR_SYMBOL + print_ret + CALL_PART1)
        for seg in PUSH_SEG_LST:
            self.output_file.write(BAR_SYMBOL + seg + PUSH_SEG)
        self.output_file.write(CALL_PART2 + str(n_args) + CALL_PART3 +
                               BAR_SYMBOL + function_name + CALL_PART4 +
                               print_ret + CALL_PART5)

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        self.output_file.write(RETURN_PART1 + self.file_name + DOT_SYMBOL +
                               END_FR + str(self.return_counter) + RETURN_PART2
                               + RETURN_PART3 + RETURN_PART4 + RETURN_PART5)
        restore_end = BAR_SYMBOL + self.file_name + DOT_SYMBOL + END_FR + str(self.return_counter)
        for seg in STORE_SEG_LST:
            self.output_file.write(restore_end + STORE_SEG1 + BAR_SYMBOL + seg + STORE_SEG2)
        self.output_file.write(RETURN_PART6)
        self.return_counter += NEXT


