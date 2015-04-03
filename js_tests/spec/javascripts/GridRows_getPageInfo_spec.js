describe("GridRows.getPageInfo", function() {
    var rows = [
        {
            "date": "2014-06-05",
            "length": 1440,
            "cells": [
                {
                    "shifts": [],
                    "open_on_right": false,
                    "open_on_left": false,
                    "end_time": "2014-06-05T00:00:00",
                    "roles": [],
                    "start_time": "2014-06-06T00:00:00",
                    "is_empty": true,
                    "columns": 1440,
                    "shift_minutes": 1440
                }
            ]
        },
        {
            "date": "2014-06-06",
            "length": 1440,
            "cells": [
                {
                    "shifts": [],
                    "open_on_right": false,
                    "open_on_left": false,
                    "end_time": "2014-06-06T00:00:00",
                    "roles": [],
                    "start_time": "2014-06-07T00:00:00",
                    "is_empty": true,
                    "columns": 1440,
                    "shift_minutes": 1440
                }
            ]
        },
        {
            "date": "2014-06-07",
            "length": 1440,
            "cells": [
                {
                    "shifts": [],
                    "open_on_right": false,
                    "open_on_left": false,
                    "end_time": "2014-06-07T00:00:00",
                    "roles": [],
                    "start_time": "2014-06-08T00:00:00",
                    "is_empty": true,
                    "columns": 1440,
                    "shift_minutes": 1440
                }
            ]
        },
        {
            "date": "2014-06-06",
            "length": 1440,
            "cells": [
                {
                    "shifts": [],
                    "open_on_right": false,
                    "open_on_left": false,
                    "end_time": "2014-06-06T00:00:00",
                    "roles": [],
                    "start_time": "2014-06-07T00:00:00",
                    "is_empty": true,
                    "columns": 1440,
                    "shift_minutes": 1440
                }
            ]
        },
        {
            "date": "2014-06-09",
            "length": 1440,
            "cells": [
                {
                    "shifts": [],
                    "open_on_right": false,
                    "open_on_left": false,
                    "end_time": "2014-06-09T00:00:00",
                    "roles": [],
                    "start_time": "2014-06-10T00:00:00",
                    "is_empty": true,
                    "columns": 1440,
                    "shift_minutes": 1440
                }
            ]
        }
    ];

    var d1 = moment("2014-06-05");
    var d2 = moment("2014-06-06");
    var d3 = moment("2014-06-07");
    var d4 = moment("2014-06-09");

    it("It should have 4 dates, the 5th, 6th, 7th, and 9th", function() {
        var gridData = new app.GridRows(rows);
        expect(gridData.getPageInfo().dates.length).toEqual(4);
    });

    it("It should have the 5th, 6th, 7th, and 9th as dates in order", function() {
        var gridData = new app.GridRows(rows);
        var dates = gridData.getPageInfo().dates;
        expect(dates[0].isSame(d1)).toBe(true);
        expect(dates[1].isSame(d2)).toBe(true);
        expect(dates[2].isSame(d3)).toBe(true);
        expect(dates[3].isSame(d4)).toBe(true);
    });
});
