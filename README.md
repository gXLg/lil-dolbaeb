# lil-dolbaeb
Esoteric Programming Language

# Description
Lil Dolbaeb is an esoteric programming language.
It is turing complete, support I/O operations
and has a rather simple syntax.

File extensions: `.lil`, `.ld`

# Syntax
In Lil Dolbaeb, every UTF-8 symbol
is a function. A function has a predefined
amount of arguments. The language is parsed
by the the rules of Polish Notation.

There are some predefined functions and
new functions may be created.

The parser consumes one functions at a time,
executes it and then repeats the process until
no more functions can be consumed.
This allows functions to have dynamic amount
of arguments after (re-)defining functions.

The language has neither variables
nor some kind of stack. Instead it offers
two global values called `last` and `args`.

Most functions don't modify these values,
but can access them. Some functions however
have "side effects" which will modify the values.

Any value in Lil Dolbaeb is saved internally as
a semi-list, which can be in one of four states:
* Empty list
* A single number
* A list of numbers of any length
* A list of numbers or lists - definition apply recursively

The values may be interpreted in two ways:
* A list
* A number

The conversion between these types is done internally
and can not be directly accessed. Following rules apply:
* When number is expected:
  * Empty list turns into zero
  * A single number is used directly
  * A list of numbers returns the last number
  * A recursive list takes the last element and applies
  the same rules as listed here
* When a list is expected:
  * Empty list, list of numbers or recursive list are used directly
  * A single number is used as a one-element-long list

Functions are interpreted one after another.
Whenever a function on the global level is
executed, `last` is set to its' return value.

When the program starts to execute, `last` is an empty list
and `args` is a one level recursive list of the program arguments
with first element being the file name of the program.
For example calling `python execute.py test.lil first "second argument"`
will result in `args := [[116, 101, 115, 116, 46, 108, 105, 108], [102, 105, 114, 115, 116], [115, 101, 99, 111, 110, 100, 32, 97, 114, 103, 117, 109, 101, 110, 116]]`.

# I/O
Lil Dolbaeb has 4 internal values
to keep track of I/O operations.
* `outputs` - list of `open("w")` streams
* `outputi` - index of the output currently operating on
* `inputs` - list of `open("r")` streams
* `inputi` - index of the input currently operating on

When starting the program following values are already available:
* `outputs`: `stdout` and `stderr`
* `outputi`: zero
* `inputs`: `stdin`
* `inputi`: zero

When reading, EOF is signaled through the value `-1`.

# Functions

Newlines are ignored.

## 0-9
No arguments.
Return the respectively selected number.

## +
Two arguments.
Add two numbers.

## -
Two arguments.
Subtract 2nd from the 1st number.

## *
Two arguments.
Multiply two numbers.

## /
Two arguments.
Divide 1st number by the 2nd.
The 2nd value is only executed
if 1st value is not equal to zero.
Dividing by zero produces zero.
The result is a whole number.

## L
No arguments.
Return `last`.

## A
No arguments.
Return `args`.

## :
Three arguments.
(Re-)define a function.
1. The function name
  * If this function was already defined earlier or is
  a builtin function, you have to supply dummy arguments
  for the parser to parse the code correctly.
2. Number of arguments
  * Expects a number
3. Code to execute when the function is called

Side effects:
  * calling a self defined function sets `args` to a list
  of the return values from the passed arguments

Return the number of arguments.

## !
One argument.
Write a character with the numerical value
equal to the provided number to the selected output.

## ?
No arguments.
Read one character from selected input,
convert it to a numerical value and return it.

## ¡
One argument.
Set `outputi` to the provided value modulo
the length of `outputs`.
Return the value.

## ¿
One argument.
Set `inputi` to the provided value modulo
the length of `inputs`.
Return the value.

## ^
No arguments.
Create a new write stream to the file,
whose location is saved as an array of character
values in `last`.
Return the new length of `outputs`.

## ~
No arguments.
Create a new read stream from the file,
whose location is saved as an array of character
values in `last`.
Return the new length of `inputs`.

## °
No arguments.
Close and remove the selected output.
Return the new length of `outputs`.

## °
No arguments.
Close and remove the selected input.
Return the new length of `inputs`.

## ,
One argument.
Concatenate `last` with the provided list
and return it.

## >
Two arguments.
Iterate over a list.
1. The list to iterate over
2. Function to use for iterating

Side effects and order of execution:
1. Execute 1st argument to get the list
2. Set `args` and `last` to empty lists
3. Before each iteration `args` is set to
the element which is currently being iterated over
4. Execute 2nd argument
5. After each iteration `last` is set to
the return value

Return the last return value.

## <
Three arguments.
Execute as long as two values are not equal.
1. Function to compare
2. Value to compare
3. Function to execute

Side effects and order of execution:
1. Execute 2nd argument
2. Execute 1st argument and compare it to the result;
if they are equal, exit the loop
3. Execute 3rd argument
4. Set `last` to the return value and go to step 2

## _
Two arguments.
Get an element from a list by the index.
Works like python's indexing where negative index
takes elements from the back of the list.
1. List to get the element from
2. Index as a number

Return the element or -1 if the index is out of bounds.

# Execution
This repo includes a python
script to run code written in Lil Dolbaeb.

To use it, clone the repository, `cd` into it and run:
```
python execute.py <code filename> [...args]
```
