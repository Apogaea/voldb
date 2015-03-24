describe("GridPageInfo.pages", function() {
  var d1 = moment("2015-01-01");
  var d2 = moment("2015-01-02");
  var d3 = moment("2015-01-03");
  var d4 = moment("2015-01-04");
  var dates = [d1, d2, d3, d4];

  it("should have 4 pages", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    expect(pageInfo.pages().length).toEqual(4);
  });

  it("each page should have a 1-based index", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    var pages = pageInfo.pages();
    expect(pages[0].pageNumber).toEqual(1);
    expect(pages[1].pageNumber).toEqual(2);
    expect(pages[2].pageNumber).toEqual(3);
    expect(pages[3].pageNumber).toEqual(4);
  });

  it("only the selected page should be active", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(3);
    var pages = pageInfo.pages();
    expect(pages[0].isActive).toBe(false);
    expect(pages[1].isActive).toBe(false);
    expect(pages[2].isActive).toBe(true);
    expect(pages[3].isActive).toBe(false);
  });
});
