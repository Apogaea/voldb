describe("GridCells.collumnDenominators", function() {
    var generateCells = function() {
        var cells = [];
        for (var i = 0, length = arguments.length; i < length; i++) {
            var columnLength = arguments[i];
            cell = {
                "shifts": [],
                "open_on_right": false,
                "open_on_left": false,
                "end_time": "2014-06-05T00:00:00",
                "roles": [],
                "start_time": "2014-06-06T00:00:00",
                "is_empty": true,
                "columns": columnLength,
                "shift_minutes": columnLength
            };
            cells.push(cell);
        }
        return cells;
    };

    it("A row whose columns are all 60 should have denominators 1, 60, 2, 30, 3, 20, 4, 15, 5, 12, 6, 10", function() {
        var rows = new app.GridCells(generateCells(60, 60, 60));
        var denominators = rows.columnDenominators();
        var expected = [1, 60, 2, 30, 3, 20, 4, 15, 5, 12, 6, 10];
        expect(_.intersection(expected, denominators)).toEqual(expected);
        expect(_.isEmpty(_.difference(expected, denominators))).toBe(true);
    });

    it("A row whose columns are all 30 and 60 should have denominators 1, 30, 2, 15, 3, 10, 5, 6", function() {
        var rows = new app.GridCells(generateCells(30, 60, 30, 60));
        var denominators = rows.columnDenominators();
        var expected = [1, 30, 2, 15, 3, 10, 5, 6];
        expect(denominators).toEqual(expected);
        expect(_.intersection(expected, denominators)).toEqual(expected);
        expect(_.isEmpty(_.difference(expected, denominators))).toBe(true);
    });

    it("A row whose columns 15, 30 60 should have denominators 1, 15, 3, 5", function() {
        var rows = new app.GridCells(generateCells(30, 60, 30, 15, 15, 60));
        var denominators = rows.columnDenominators();
        var expected = [1, 15, 3, 5];
        expect(denominators).toEqual(expected);
        expect(_.intersection(expected, denominators)).toEqual(expected);
        expect(_.isEmpty(_.difference(expected, denominators))).toBe(true);
    });
});
