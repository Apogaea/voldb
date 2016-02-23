describe("Role.isHydrated", function() {
  var d1 = moment("2015-01-01");
  var d2 = moment("2015-01-02");
  var d3 = moment("2015-01-03");
  var d4 = moment("2015-01-04");
  var dates = [d1, d2, d3, d4];

  it("should select the first date when selecting page 1.", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(1);
    chai.expect(pageInfo.activePage()).to.equal(1);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d1);
  });

  it("should select the second date when selecting page 2.", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(2);
    chai.expect(pageInfo.activePage()).to.equal(2);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d2);
  });

  it("should select the third date when selecting page 3.", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(3);
    chai.expect(pageInfo.activePage()).to.equal(3);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d3);
  });

  it("should select the fourth date when selecting page 4.", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(4);
    chai.expect(pageInfo.activePage()).to.equal(4);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d4);
  });

  it("should gracefully handle selection of dates below the allowed range", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(0);
    chai.expect(pageInfo.activePage()).to.equal(1);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d1);
    pageInfo.selectPage(-1);
    chai.expect(pageInfo.activePage()).to.equal(1);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d1);
  });

  it("should gracefully handle selection of dates above the allowed range", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(20);
    chai.expect(pageInfo.activePage()).to.equal(4);
    chai.expect(pageInfo.get("selectedDate")).to.equal(d4);
  });
});
