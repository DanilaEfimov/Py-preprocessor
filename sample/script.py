# @random has lower priority than @repeat
# here can be compiled something like:
# print(PI)         3.14159
# print(PI)         3.14159
# print(E)          2.71828
# print(GREETING)   Hello, world!
# print(E)          2.71828 e.g.
from unicodedata import mirrored


@repeat(MAX_RETRIES)
@random(["print(\"GREETING\")", "print(\"PI\" )", "print(\"E\")", "@repeat(MAX_RETRIES)"])


# @random has higher priority than @debug_only and @invisible
# it is important to remember the maximum nesting depth of directives (16 by default)
@random(["\n#compiled comment", "@invisible"])
print("this source string was inputted in debug mode or hidden")


# conditional compilation example
@ifdef MAX_RETRIES
    @define MAX_RETRIES 2
# it is important to remember the maximum nesting depth of directives (16 by default)
# it will look like: 0 * print(GETTING), MAX_RETRIES * print(GETTING), and so on...
    @repeat(MAX_RETRIES)
    @random(["print(\"GREETING\" )", "@repeat(MAX_RETRIES)\nprint(\"GREETING\")"])
    @ifdef PI
if MAX_RETRIES != 5:
    print("defined: PI ")
    @define PI 3.14
    print("redefinition: PI ")
    @undef E
    @endif
@endif


    # other custom directives
@ifndef E
    @ifdef E
        print("cannot be included in compiled file")
    @elif A
        print("other unexecutable expression branch")
    @else
    if True:
        print("some code block")
        @ifdef DEBUG
        @debug_only
        @endif
# logs
        @invisible
        # TODO: secret comment for debug
    @endif
@endif

@mirror
print("reversed string"); l = [1,2,3]


# including test
print("used default symbols table:")
"""
#include <sample/symbols.ini>
@include sample/symbols.ini
"""
