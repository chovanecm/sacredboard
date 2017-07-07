/*global QUnit*/ //for eslint to ignore missing QUnit


define(["command"],
    /**
     *
     * @param {CommandQueue} CommandQueue - CommandQueue class.
     */
    function (CommandQueue) {
        "use strict";
        QUnit.module("CommandQueue");

        QUnit.test("Test commandQueue",
            function (assert) {
                var queue = new CommandQueue();
                var value = 0;
                // prepare increment the value by one
                function f1() {
                    value = 10;
                }
                assert.equal(value, 0);
                queue.addCommand(f1);
                assert.equal(value, 0);

                function f2() {
                    value++;
                }

                queue.addCommand(f2);
                assert.equal(value, 0);

                queue.runCommands();
                assert.equal(value, 11, "Commands should set the value to 10 and increment it by 1 to 11.");

                queue.runCommands();
                assert.equal(value, 11, "Commands shouldn't run again.");
            });
    });