"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter

C_ARITHMETIC, C_PUSH, C_POP, C_RETURN = 'C_ARITHMETIC', 'C_PUSH', 'C_POP', 'C_RETURN'
C_LABLE, C_IF, C_GOTO, C_CALL, C_FUNCTION = 'C_LABLE', 'C_IF', 'C_GOTO', 'C_CALL', 'C_FUNCTION'



def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    vm_file = Parser(input_file)
    output_vm_file = CodeWriter(output_file)
    filename, ext = os.path.splitext(os.path.basename(input_file.name))
    output_vm_file.set_file_name(filename)
    while vm_file.has_more_commands():
        vm_file.advance()
        cur_command = vm_file.command_type()
        if cur_command == C_RETURN:
            output_vm_file.write_return()
            continue
        arg1 = vm_file.arg1()
        if cur_command == C_ARITHMETIC:
            output_vm_file.write_arithmetic(arg1)
        elif cur_command == C_LABLE:
            output_vm_file.write_label(arg1)
        elif cur_command == C_IF:
            output_vm_file.write_if(arg1)
        elif cur_command == C_GOTO:
            output_vm_file.write_goto(arg1)
        else:
            arg2 = vm_file.arg2()
            if cur_command == C_CALL:
                output_vm_file.write_call(arg1, arg2)
            elif cur_command == C_FUNCTION:
                output_vm_file.write_function(arg1, arg2)
            else:
                output_vm_file.write_push_pop(cur_command, arg1, arg2)



if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)
