Hei!

Report:

Introduction:

Good, nice that you mention previous work!

Methods:

Good design section, for the future i would try to distance the report from the design and rather only focus on what you are designing and implementing!
I understand referring to the assignment makes it easier, however later during the degree this will help you out.

The implementation section is OK, i would recommend writing the report using an `objective voice` meaning; do not use personal pronouns.
I actually would like more about how all the components are implemented, instead of only what is different and workarounds.

The experiments section is good.

Results:

I see something went wrong referencing the figure, and please use something else than a screenshot from the terminal as a figure.
I recommend a table or something to show which tests failed. Otherwise good.

Discussion: 

Good points.

The book does go through some basic opcode to control signals however as you say it is far from complete.
I think the intention is to get us to think about how we should fill in the missing ones.

I agree about signed and unsigned Python and `ints` can be difficult.

Conclusion:

Good, it is a bit short, however i do not have any suggestion on what to write.

Code:

Implementation looking good, here are a few nitpicks that i saw:

* When writing unittests, split the test function up to test one aspect of the component. For example in ALU it would be natural to have one test that tests add, one that tests sub, and so on.

* In controlUnit, i would set all the controlSignals out to 0 first and then only assert the ones that are needed. It makes the code take less space, while achieving the same thing.

Since you already are allowed to take the exam you do not need to hand this in, however i would pass this anyway.

GRADE: PASS
