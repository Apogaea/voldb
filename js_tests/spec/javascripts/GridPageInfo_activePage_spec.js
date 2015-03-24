describe("Role.isHydrated", function() {
  var d1 = moment("2015-01-01");
  var d2 = moment("2015-01-02");
  var d3 = moment("2015-01-03");
  var d4 = moment("2015-01-04");
  var dates = [d1, d2, d3, d4];

  it("should start on page 1.", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    expect(pageInfo.get("selectedDate")).toBe(null);
    expect(pageInfo.activePage()).toEqual(1);
  });

  it("should start be on page 1 if first date selected", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.set("selectedDate", d1);
    expect(pageInfo.activePage()).toEqual(1);
  });

  it("should start be on page 2 if second date selected", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.set("selectedDate", d2);
    expect(pageInfo.activePage()).toEqual(2);
  });

  it("should start be on page 3 if third date selected", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.set("selectedDate", d3);
    expect(pageInfo.activePage()).toEqual(3);
  });

  it("should start be on page 4 if fourth date selected", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.set("selectedDate", d4);
    expect(pageInfo.activePage()).toEqual(4);
  });
});
