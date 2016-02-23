describe("GridPageInfo.hasNextPage and GridPageInfo.hasPreviousPage", function() {
  var d1 = moment("2015-01-01");
  var d2 = moment("2015-01-02");
  var d3 = moment("2015-01-03");
  var d4 = moment("2015-01-04");
  var dates = [d1, d2, d3, d4];

  it("should have a next page on pages 1, 2, and 3", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(1);
    chai.expect(pageInfo.hasNextPage()).to.be.true;
    pageInfo.selectPage(2);
    chai.expect(pageInfo.hasNextPage()).to.be.true;
    pageInfo.selectPage(3);
    chai.expect(pageInfo.hasNextPage()).to.be.true;
  });

  it("should not a next page on page 4", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(4);
    chai.expect(pageInfo.hasNextPage()).to.be.false;
  });

  it("should have a previous page on pages 2, 3, and 4", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(2);
    chai.expect(pageInfo.hasPreviousPage()).to.be.true;
    pageInfo.selectPage(3);
    chai.expect(pageInfo.hasPreviousPage()).to.be.true;
    pageInfo.selectPage(4);
    chai.expect(pageInfo.hasPreviousPage()).to.be.true;
  });

  it("should not a previous page on page 1", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(1);
    chai.expect(pageInfo.hasPreviousPage()).to.be.false;
  });
});
