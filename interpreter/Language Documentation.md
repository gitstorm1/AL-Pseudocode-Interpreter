# A-Level Pseudocode Documentation

This contains all the different features of the language that is implemented by this interpreter. Most of these have been taken from the [Pseudocode guide](https://pastpapers.co/cie/A-Level/Computer%20Science%20(for%20first%20examination%20in%202021)%20(9618)/Syllabus%20&%20Specimen/9618_y21_sg.pdf); however, where there are ambiguities, I have specified them based on my own preferences.

## ASCII
The interpreter currently only supports ASCII. Please do not input Unicode characters in it, not yet.

## Statements \<statement\>
- Any valid piece of code that does not return a value is a statement.
- A statement may or may not contain an expression within it.

### Comments
- Only single-line comments are supported.
- Comments begin with `//` and end at the end of the line.
```
// This is a comment
<statement> // This is a comment
<expression> // This is a comment
```

### Identifiers \<identifier\>
- It is possible to bind values to names; these names are known as identifiers.
- They can consist of `a-z`, `A-Z`, `_`, and `0-9` characters only.
- Identifiers cannot begin with a number.

### Variables
- There are two types of variables: constants and non-constants.
- A variable's type cannot be changed after declaration.

#### Constants
- These variables, once initialized, cannot be modified later.
- It is necessary to initialize constants (declaration alone is not allowed).
- A non-constant variable can be made into a constant by using the same identifier name.
```
CONSTANT <identifier> = <value>
```
- Note: Constants can only be initialized with literals.

#### Non-constants
- These variables can be both declared and assigned to.

##### Declaring variables explicitly
- Explicit declaration of variables before using them is a good practice:
```
DECLARE <identifier> : <datatype>
```

##### Value assignment
- Variables can undergo value assignment i.e. new values can be bound to already existing identifiers. The value must be of the same type as the old value.
```
<identifier> <- <expression>
```
- Assigning to a variable that has not been declared declares that variable implicitly. The datatype is detected automatically. The same holds true when initializing constants.

#### Datatypes \<datatype\>
- There are six basic datatypes:
1. `INTEGER`: A whole number. Example: `24`
2. `REAL`: A number with a decimal point. Example: `2.4`
3. `CHAR`: A single character. Example: `'e'`
4. `STRING`: A sequence of zero or more characters. Example: `"some text"`
5. `BOOLEAN`: Represents either true or false. Example: `TRUE`, `FALSE`
6. `DATE`: Represents a date in the format `dd/mm/yyyy`. Example: `D"17/8/2023"`

#### Arrays
- An array contains a series of values.
- An array has a constant length.
- All the values in an array must be of the same datatype.
- Arrays can be n-dimensional (basically, an array of arrays is possible, but only with this special syntax).
```
// Declaring an array
DECLARE <identifier> : ARRAY[1:<[dimension #1] array length>, 1:<[dimension #2] array length>, ..., 1:<[dimension #n] array length>] OF <datatype>
// Accessing the array
<identifier>[<expression>, <expression>,...,<expression>]
```
- Arrays cannot be initialized; you have to declare them and then fill in the values using a loop or by assigning to them an existing array of the same structure.
- Example:
```
DECLARE grid : ARRAY[1:50, 1:50] OF REAL
grid[2, 3] <- 20.0 // Assignment method 1
DECLARE copy : ARRAY[1:50, 1:50] OF REAL
copy <- grid // Assignment method 2
```


## Expressions \<expression\>
- Any valid piece of code that returns a value is an expression.
- An expression cannot contain a statement within it.