_.mixin({
    /*
     *  Allows for chaining an intersection call.
     */
    applyIntesection: function(arrays) {
        return _.intersection.apply(_, arrays);
    }
});
