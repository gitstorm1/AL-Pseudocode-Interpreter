# A-Level Pseudocode Documentation

This contains all the different features of the language that is implemented by this interpreter. Most of these have been taken from the [Pseudocode guide](https://pastpapers.co/cie/A-Level/Computer%20Science%20(for%20first%20examination%20in%202021)%20(9618)/Syllabus%20&%20Specimen/9618_y21_sg.pdf); however, where there are ambiguities, I have specified them based on my own preferences.

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

#### Constants
- These variables, once initialized, cannot be modified later.
- It is necessary to initialize constants (declaration alone is not allowed).
- A non-constant variable can be made into a constant by using the same identifier name.
```
CONSTANT <identifier> = <expression>
```

#### Non-constants
- These variables can be both declared and assigned to.

##### Declaring variables explicitly
- Explicit declaration of variables before using them is a good practice:
```
DECLARE <identifier> : <datatype>
```

##### Value assignment
- Variables can undergo value assignment i.e. new values can be bound to already existing identifiers.
```
<identifier> <- <expression>
```
- Assigning to a variable that has not been declared declares that variable implicitly. The datatype is detected automatically. The same holds true when initializing constants.

#### Datatypes \<datatype\>


## Expressions \<expression\>
- Any valid piece of code that returns one or more value(s) is an expression.
- An expression cannot contain a statement within it.