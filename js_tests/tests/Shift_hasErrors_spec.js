describe("Shift.hasErrors", function() {
  it("should not have errors if unpopulated", function() {
    var shift = new app.Shift();
    chai.expect(shift.hasErrors()).to.be.false;
  });

  it("should not have errors if empty array", function() {
    var shift = new app.Shift({claimErrors: []});
    chai.expect(shift.hasErrors()).to.be.false;
  });

  it("should have errors if non-empty array", function() {
    var shift = new app.Shift({claimErrors: ["Some error"]});
    chai.expect(shift.hasErrors()).to.be.true;
  });
});
