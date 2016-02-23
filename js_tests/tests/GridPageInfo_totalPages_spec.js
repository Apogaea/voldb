describe("GridPageInfo.totalPages", function() {
  var d1 = moment("2015-01-01");
  var d2 = moment("2015-01-02");
  var d3 = moment("2015-01-03");
  var d4 = moment("2015-01-04");
  var dates = [d1, d2, d3, d4];

  it("should start on page 1.", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    chai.expect(pageInfo.totalPages()).to.equal(4);
  });
});
