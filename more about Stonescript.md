# More about Stonescripts

## What is this?

Despite an official manual of Stonescript, some key information are still not explained, especially the syntax. Therefore, I'm writing this to show what I have experimented. Note that I **cannot guarantee** the correctness of the information in this document. If you find any mistake, contact tyzhang0001@gmail.com. I'll be happy :D

## Syntax

1. As far as I know, lists of useful Stonescript information exist ONLY in the official manual:
    1. Search filters (to evaluate foes, locations and items)
    2. Math Operations
    3. Cooldown ID
    4. Key codes
    5. Sounds
    6. Music
    7. Ambient audio
    Information not found anywhere: Enemy names, Location names.
2. Some best practices for fighting lags:
    1. For any system variable or system function that you uses >1 times per frame, assign them to a local variable and call the local one instead.
    2. Quote strings. This is also a good coding habit :)
    For more information, see [this discord channel](https://discord.com/channels/423242655498240000/1149369674052677654) and [this document](https://docs.google.com/document/d/14Xyu1a84GEL7QRYeDIv0uSGq4c22wKjD4v9HpqJfsQw/edit) by MaxMinMedian.
3. Function overloading not supported. E.g., 
    ```stonescript
    func sum(x, y)
        return x + y
    func sum(x, y, z)
        return x + y + z
    sum(1, 2) // Error: expected 3 parameters but received 2
    ```
    Stonescript only takes the latest-defined version if function names overlap.

4. Do not add inline comment after a import. E.g.,
    ```stonescript
    var cl = import UserScript/cl //color
    ```
    This will cause failure to import.

5. Foe state.
    | foe state | meaning |
    |:--------:|:--------:|
    | -1 | not appeared |
    | 0 | idle |
    | 1 | waking Up |
    | 2 | approaching |
    | 4 | dying |
    | 32 | attack foreswing |
    | 33 | attacking |
    | 100+ | Alternate weapons (offset by either 100 or 110) |

    Item state.

    | item state | meaning |
    |:--------:|:--------:|
    | -1 | item.left.state = -1 when using two-handed item |
    | 1 | idle |
    | 2 | weapon foreswing + damage dealt at the end (Cast) |
    | 3 | weapon backswing (Perf) |
    | 4 | cooldown before another attack, or the only state for shields (Cooldown) |

6. About type-unsafe operations:
    Returns of Type() function include 'int', 'float', 'string', ''bool', 'function', 'object' and 'null'
    Operators include =!&|><+-*/ etc.
    ```stonescript
    // int and float
    0 = 0.0                     // true
    Type(0+0.0)                 // "float"
    1 / 2 = 0                   // true
    1.0/2 = 0.5                 // true
    1/2.0 = 0.5                 // true
    1.0/3 = 0.3333333           // false
    1.0/3 = 0.33333333          // true

    // int, float and string
    // turns int or float into string, then apply "=", "+".
    // float ending with ".0" will be treated like int when turning into a string
    "A" = "a"                   // true
    "a" = "A"                   // true

    #222222 = "#222222"         // true
    "#222222" = #222222         // true

    10 = "0"                    // true
    "0.1" = 1                   // true
    0.0 = "0.0"                 // false
    "9"+1                       // "91"
    "9"+1.0                     // "91"
    "9"+1.1                     // "91.1"
    1+"9"                       // "19"
    1.0+"9"                     // "19"
    1.1+"9"                     // "1.19"

    "1" = true                  // false
    true = "1"                  // false
    false = "false"             // true
    "false" = false             // true
    false + "1"                 // "False1"
    !"1"                        // false
    !""                         // true

    // if statements: 0, null, and empty string are falsy, others are truthy, including empty arrays
    ?""
        >no                     // will NOT run this line
    ?0
        >no                     // will NOT run this line
    ?null
        >no                     // will NOT run this line
    ?"0"
        >yes                    // will run this line
    ?1
        >yes                    // will run this line
    ?[]
        >yes                    // will run this line
    ```
    These will throw out an error:
    ```stonescript
    1 = true
    1 = false
    true = 1
    false = 1
    true + 1
    "0" * 2
    ```

7. Like python, the | operator will not try to evaluate the second argument if the first is already true. Similar for the & operator as well. E.g.,
    ```stonescript
    func test_true(str)
        >@str@
        return true

    func test_false(str)
        >@str@
        return false
    
    test_true("1") | test_false("2")     // prints "1"
    test_false("1") & test_true("2")     // prints "1"
    test_true("0") & test_false("1") & test_true("2")     // prints "1"
    ```

8. Moondialing. Increase atk speed with moondial stone. You may use it when you have at least 2 +17 rune swords. See [this document](https://docs.google.com/spreadsheets/d/1OiiPNoB4bg0FBuW9si7GpYBoTzafNBGE10y_L324rKA/edit#gid=2098533897). 3, 3-3 for two +21 swords, 4-2 for two +17 swords, 3, 4-5 for one +21 plus one +17. Here is an example of how to do moondialing with 2 +21 swords.
    ```stonescript
    var mdc = 1
    func md21()
    ?mdc = 1
        equipL moon
        equipR (equipment1)
    ?mdc = 2
        equipL moon
        equipR (equipment2)
    ?mdc = 3
        equipL (equipment1)
        equipR (equipment2)
        mdc = 0
    mdc++
    ```

9. You can use Bardiche ability just before Dysangelos starts talking. also works for xyloalgia death -> poena spawn. Best critical enchanted.


