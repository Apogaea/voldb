describe("Shift.claimUrl", function() {
  it("should be the right url", function() {
    var shift = new app.Shift({id: 3});
    chai.expect(shift.claimUrl()).to.equal("/api/v2/shifts/3/claim/");
  });
});
