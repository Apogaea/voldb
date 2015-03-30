describe("Shift.claimUrl", function() {
  it("should be the right url", function() {
    var shift = new app.Shift({id: 3});
    expect(shift.claimUrl()).toEqual("/api/v2/shifts/3/claim/");
  });
});
