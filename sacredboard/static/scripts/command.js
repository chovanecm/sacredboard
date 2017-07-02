/**
 * @module
 */
define([], function() {
    "use strict";
    /**
     * A Command queue can collect functions and execute them later.
     *
     * @alias module:command
     */
    class CommandQueue {
        constructor() {
            this.commandQueue = [];
        }

        /**
         * Add a new command to the command queue.
         *
         * @param {function} command - The function to be called.
         */
        addCommand(command) {
            this.commandQueue.push(command);
        }

        /**
         * Run all commands in the queue and empty the queue.
         */
        runCommands() {
            var oldQueue = this.commandQueue;
            this.commandQueue = [];
            oldQueue.forEach(function (command) {
               command();
            });
        }
    }
    return CommandQueue;
});