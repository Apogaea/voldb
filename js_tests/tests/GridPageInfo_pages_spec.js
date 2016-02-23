describe("GridPageInfo.pages", function() {
  var d1 = moment("2015-01-01");
  var d2 = moment("2015-01-02");
  var d3 = moment("2015-01-03");
  var d4 = moment("2015-01-04");
  var dates = [d1, d2, d3, d4];

  it("should have 4 pages", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    chai.expect(pageInfo.pages().length).to.equal(4);
  });

  it("each page should have a 1-based index", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    var pages = pageInfo.pages();
    chai.expect(pages[0].pageNumber).to.equal(1);
    chai.expect(pages[1].pageNumber).to.equal(2);
    chai.expect(pages[2].pageNumber).to.equal(3);
    chai.expect(pages[3].pageNumber).to.equal(4);
  });

  it("only the selected page should be active", function() {
    var pageInfo = new app.GridPageInfo({dates: dates});
    pageInfo.selectPage(3);
    var pages = pageInfo.pages();
    chai.expect(pages[0].isActive).to.be.false;
    chai.expect(pages[1].isActive).to.be.false;
    chai.expect(pages[2].isActive).to.be.true;
    chai.expect(pages[3].isActive).to.be.false;
  });
});
